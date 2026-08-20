/**
 * Drie-emmer-mechaniek van de routeverkenner (laag 1).
 *
 * Per route (hoofdstuk-III-eindpunt) draaien we de engine twee keer:
 *  - optimistisch: onbekende feiten krijgen hun 'gunstige' waarde
 *    (+ kandidaat-retries voor parameters met conflicterende eisen);
 *  - pessimistisch: onbekende feiten krijgen hun 'ongunstige' waarde.
 *
 * optimistisch false  → uitgesloten — maar alleen 'bewijsbaar' als de keten
 *                       geen ambigu-geanalyseerde parameters bevat; anders
 *                       blijft de route in 'mogelijk' met een onzeker-vlag.
 * pessimistisch true  → voldoet al met de gegeven antwoorden.
 * anders              → mogelijk, mits …
 *
 * De polariteitsdata komt uit vragenflow.json (tools/build_vragenflow.py).
 */

const GATE_ARTIKELEN = ['1', '3', '4', '5', '6', '8', '9', 'Bijlage I'];
const MAX_RETRIES_PER_ROUTE = 12;

export function maakVerkenner({ engine, lawId, vragenflow, routekaart }) {
  const artikelen = vragenflow.artikelen;
  const gates = GATE_ARTIKELEN.filter((g) => g in artikelen);

  function ketens(target) {
    return [...gates, target];
  }

  function basisToewijzing(target, modus, antwoorden) {
    const params = {};
    const volgorde = [
      ...Object.keys(artikelen).filter((n) => !gates.includes(n) && n !== target),
      ...gates,
      target,
    ];
    for (const n of volgorde) {
      if (!(n in artikelen)) continue;
      for (const [p, spec] of Object.entries(artikelen[n].params)) {
        params[p] = spec.ambigu
          ? spec.neutraal
          : spec[modus === 'opt' ? 'gunstig' : 'ongunstig'];
      }
    }
    Object.assign(params, antwoorden);
    for (const k of Object.keys(params)) if (params[k] === null) delete params[k];
    return params;
  }

  function draai(endpoint, params) {
    try {
      const res = engine.execute(lawId, endpoint, params, '2024-06-01');
      return { waarde: res.outputs?.[endpoint], fout: null };
    } catch (e) {
      return { waarde: undefined, fout: String(e) };
    }
  }

  function optimistisch(target, antwoorden) {
    const endpoint = artikelen[target].endpoint;
    const basis = basisToewijzing(target, 'opt', antwoorden);
    let r = draai(endpoint, basis);
    if (r.waarde === true) return { levend: true };
    let pogingen = 0;
    let ambiguGeprobeerd = 0;
    let ambiguTotaal = 0;
    for (const n of ketens(target)) {
      if (!(n in artikelen)) continue;
      for (const [p, spec] of Object.entries(artikelen[n].params)) {
        if (p in antwoorden) continue;
        // conflicterende gunstig-kandidaten: alternatieven proberen
        for (const kand of (spec.gunstig_kandidaten ?? []).slice(1)) {
          if (pogingen++ >= MAX_RETRIES_PER_ROUTE) break;
          const v = draai(endpoint, { ...basis, [p]: kand });
          if (v.waarde === true) return { levend: true };
        }
        // ambigu geanalyseerde booleans: de niet-neutrale kant proberen —
        // redt een enkele flip de route, dan is de ambiguïteit beslissend
        // en is 'mogelijk' het eerlijke oordeel
        if (spec.ambigu) {
          ambiguTotaal++;
          const probes = [];
          if (typeof spec.neutraal === 'boolean') probes.push(!spec.neutraal);
          else if (spec.neutraal === '') {
            probes.push(...(vragenflow.vragen[p]?.opties ?? []).slice(0, 6));
          } else if (typeof spec.neutraal === 'number') {
            probes.push(1e15);
          }
          for (const probe of probes) {
            if (pogingen >= MAX_RETRIES_PER_ROUTE) break;
            pogingen++;
            ambiguGeprobeerd++;
            const v = draai(endpoint, { ...basis, [p]: probe });
            if (v.waarde === true) return { levend: true, doorAmbigu: true };
          }
        }
      }
    }
    // niet te redden met enkelvoudige variaties → uitgesloten; 'indicatief'
    // wanneer er ambiguïteit was die we niet uitputtend konden verkennen
    return {
      levend: false,
      fout: r.fout,
      indicatief: ambiguTotaal > ambiguGeprobeerd || ambiguGeprobeerd > 0,
    };
  }

  // Routes die al zonder enig antwoord optimistisch vastlopen zijn
  // analyse-artefacten (IF-structuren die de polariteits-analyse niet
  // doorgrondt), geen juridisch oordeel: die blijven permanent 'mogelijk ·
  // analyse onvolledig'. Alleen routes die door ántwoorden sterven zijn
  // werkelijk uitgesloten.
  let analyseDood = null;

  function bepaalAnalyseDood() {
    if (analyseDood) return analyseDood;
    analyseDood = new Set();
    for (const route of routekaart.routes) {
      const n = route.artikel;
      if (!(n in artikelen)) continue;
      const opt = optimistisch(n, {});
      if (!opt.levend) analyseDood.add(n);
    }
    return analyseDood;
  }

  /** Beoordeel alle routes; antwoorden = { paramnaam: waarde }. */
  function beoordeel(antwoorden) {
    const uitgesloten = [];
    const voldoet = [];
    const mogelijk = [];
    const artefacten = bepaalAnalyseDood();
    for (const route of routekaart.routes) {
      const n = route.artikel;
      if (!(n in artikelen)) continue;
      const endpoint = artikelen[n].endpoint;
      if (artefacten.has(n)) {
        mogelijk.push({ route, status: 'mogelijk_onzeker' });
        continue;
      }
      const opt = optimistisch(n, antwoorden);
      if (!opt.levend) {
        if (opt.fout) {
          // engine-fout is geen juridisch oordeel: route blijft open, gemarkeerd
          mogelijk.push({ route, status: 'mogelijk_onzeker', fout: opt.fout });
        } else {
          uitgesloten.push({
            route,
            status: 'uitgesloten',
            indicatief: !!opt.indicatief,
          });
        }
        continue;
      }
      const pess = draai(endpoint, basisToewijzing(n, 'pess', antwoorden));
      if (pess.waarde === true) {
        voldoet.push({ route, status: 'voldoet' });
      } else {
        mogelijk.push({ route, status: 'mogelijk', fout: pess.fout });
      }
    }
    return { uitgesloten, voldoet, mogelijk };
  }

  /** Volgende vraag: de nog onbeantwoorde parameter die de meeste
   *  nog-levende routes raakt (gate-parameters wegen mee voor alle routes). */
  function volgendeVragen(antwoorden, oordeel, max = 8) {
    const levendeRoutes = [...oordeel.mogelijk, ...oordeel.voldoet].map(
      (x) => x.route.artikel,
    );
    const telling = new Map();
    const raakt = (p) => {
      const meta = vragenflow.vragen[p];
      if (!meta) return 0;
      const inGate = meta.artikelen.some((a) => gates.includes(a));
      if (inGate) return levendeRoutes.length;
      return meta.artikelen.filter((a) => levendeRoutes.includes(a)).length;
    };
    for (const [p, meta] of Object.entries(vragenflow.vragen)) {
      if (p in antwoorden) continue;
      const n = raakt(p, meta);
      if (n > 0) telling.set(p, n);
    }
    return [...telling.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, max)
      .map(([p, n]) => ({ param: p, raaktRoutes: n, ...vragenflow.vragen[p] }));
  }

  /** Uitleg voor één route onder de huidige antwoorden (optimistische run). */
  function uitleg(target, antwoorden) {
    const endpoint = artikelen[target].endpoint;
    const params = basisToewijzing(target, 'opt', antwoorden);
    try {
      const res = engine.executeWithTrace(lawId, endpoint, params, '2024-06-01');
      return { trace: res.trace_text ?? res.trace ?? null, outputs: res.outputs };
    } catch (e) {
      return { trace: null, fout: String(e) };
    }
  }

  return { beoordeel, volgendeVragen, uitleg };
}
