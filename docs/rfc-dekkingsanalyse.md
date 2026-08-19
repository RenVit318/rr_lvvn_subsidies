# RFC-dekkingsanalyse — wat de regelrecht-RFC's wel en niet borgen voor dit dossier

Peildatum: 11 augustus 2026, tegen de RFC-set in `MinBZK/regelrecht`
(`docs/src/content/rfcs/`). Doel: vaststellen welke aannames van dit dossier al
door een RFC gedekt zijn, welke alleen in skills of methodedocumenten leven, en
welke concrete blokkades er in schema en engine zitten voor het modelleren van
een EU-verordening.

Samengevat: **de normenhiërarchie is goed gedekt; de borgingsdiscipline
nauwelijks.** De RFC-nummers die precies over onze zorgen gaan (026, 027, 028,
031, 033, 034, 035) bestaan, maar zijn gereserveerde stubs zonder vastgesteld
ontwerp.

## 1. Normenhiërarchie en EU-lagen — goed gedekt, Nederlands ingevuld

- **RFC-015 (Engine Policy, Proposed / Not implemented)** rangschikt de lagen
  met `VERDRAG` (0), `EU_VERORDENING` (1) en `EU_RICHTLIJN` (2) boven Grondwet
  en Wet. De levende engine codeert dezelfde rangorde hard
  (`packages/engine/src/priority.rs`), dus lex superior over een EU-laag werkt
  vandaag al.
- **RFC-003 (IoC voor gedelegeerde regelgeving, Accepted / Implemented)** geeft
  de delegatiemechanica (`open_terms`/`implements`) waarmee een latere
  subsidieregeling zich aan een LVV-artikel hecht. Bevat ook de enige
  single-source-of-truth-regel in de hele set: één artikel is het
  delegatiepunt, andere artikelen routeren erdoorheen — maar die regel is
  intra-wet en niet afgedwongen.
- **Nederlands ingevuld:** RFC-015 kent geen EU→nationaal-rij in
  `delegation_rules` en alleen Nederlandse scope-dimensies
  (gemeente/provincie/waterschap); het bevoegdheidsmodel van **RFC-002** kent
  geen Commissie of lidstaat.

## 2. Verrijkingsborging — half gedekt

- **RFC-012 (Untranslatables, Accepted / Implemented)** is de enige harde,
  blokkerende poort: fail-fast standaard, menselijke review via
  `accepted: false`, en het credo "a flagged gap is better than a
  plausible-looking wrong answer." Direct bruikbaar voor dit dossier.
- **RFC-013 (Execution Provenance, Accepted / Implemented)** pint uitvoeringen
  reproduceerbaar vast (receipts met corpus-hashes en per-output-herkomst) —
  nuttig voor de filter-traces, maar zegt niets over of de YAML de letter trouw
  weergeeft.
- **Stubs zonder ontwerp:** reviewersrollen (RFC-027), werkvoorraad van de
  enricher (RFC-026), bouwplan van een verrijking (RFC-033), en de
  letter-vs-toelichting-regel (RFC-030: "een toelichting mag nooit een
  grondslag voor een regel zijn" — één zin, geen ontwerp).

## 3. Conceptidentiteit — feitelijk ongedekt

- Het wie-leidt-af-principe (de betekenis van een term wordt bepaald door wie
  hem afleidt) staat in **geen enkele RFC**; het leeft alleen in de
  `reference-and-concept-hygiene`-skill.
- **RFC-001 §9** bakt de ambiguïteit zelfs in: een interne verwijzing en een
  extern wereldfeit hebben dezelfde YAML-vorm (`source.output` zonder
  `regulation`), dus het schema kan het onderscheid blad-vs-afgeleid niet
  uitdrukken.
- **RFC-023** benoemt producent/consument-mismatch als echt corpusdefect en
  schuift de controle expliciet door ("an engine concern").
- **RFC-034 (Concept-anker, stub)** benoemt het valse-vrienden-probleem
  (`ingezetene` betekent niet overal hetzelfde) in één zin en meldt dat de
  blokkerende poort "alleen in een methodedocument" bestaat.

Consequentie voor dit dossier: de conceptenhygiëne moet uit onze eigen
conventies en desk-audits komen; er is geen vangnet in schema, engine of RFC.

## 4. Open normen — gedekt, maar scheef

- RFC-012's untranslatable is een *uitdrukkingsgat* ("de wet is duidelijk,
  maar de formele taal kan het nog niet uitdrukken") — géén oordeelsgat.
- **Geen enkele RFC zegt dat sommige normen niet berekenbaar gemodelleerd
  mógen worden.** RFC-003's uitgewerkte voorbeeld toont zelfs de omgekeerde
  gewoonte (`redelijk_percentage` met `default: 6`).
- De markeermachinerie (RFC-018, `questioning` + ambiguïteitsvocabulaire)
  waarschuwt bewust in plaats van te falen; RFC-031 (markeringen en open
  normen) is een stub.

Consequentie: het onderscheid oordeel-vs-berekening bewaken we zelf, per
artikel, in de fideliteits-audit.

## 5. Concrete blokkades voor EU-modellering

Vastgesteld tegen schema v0.5.6 en de genoemde RFC's:

1. **`references[].bwb_id` is verplicht** met patroon `^BWBR[0-9]{7}$`, zonder
   CELEX/ELI-alternatief. Een EU-verordening kan zichzelf identificeren
   (top-level `celex_nummer`/`eli`) maar kan in de gestructureerde
   `references` geen ander EU-instrument citeren. Scherpste schema-gat.
2. **De corpusmap-conventie is `regulation/nl/…`**; de generalisatie naar
   `<jurisdiction>` (RFC-022) is Draft. Het oude experiment omzeilde dit met
   `nl/eu_verordening/…` — accepteren of aankaarten.
3. **RFC-020 (`as_of`, statische verwijzingen "zoals dat luidde op …") is niet
   geïmplementeerd**, terwijl EU-verordeningen frequent wijzigen; elke
   kruisverwijzing resolvet nu dynamisch op één globale datum.
4. **RFC-007: `overrides` vuren alleen binnen een contextuele wet** — "when no
   contextual law is set (standalone API call), no overrides apply." Een
   vrijstelling gemodelleerd als override is dus onzichtbaar voor precies de
   losse artikel-queries die het filter doet. Daarom modelleren we
   LVV-artikelen als eigen endpoints (zoals het experiment al deed), niet als
   overrides.
5. **Geen EU-delegatietype:** RFC-003 stap 11 valideert dat de
   `regulatory_layer` van een implementerende regeling het `delegation_type`
   van de open term matcht; een EU-vormig delegatietype is nergens
   gedocumenteerd. Relevant zodra een NL-regeling zich aan de LVV hecht.
6. **Skills met stille degradatie voor EU-recht:** het MvT-onderzoek zoekt
   kamerstukken (vindt voor de LVV niets en slaat over; considerans en
   Commissie-richtsnoeren zitten in geen skill), en de versie-drift-check
   spreekt alleen wetten.overheid.nl — EUR-Lex-versiediscipline is handwerk.

## Wat dit dossier kan teruggeven

De gereserveerde RFC-nummers wachten op precies het bewijsmateriaal dat deze
cyclus oplevert: een werkende conceptenhygiëne-praktijk (→ RFC-034), een
oordeel-vs-berekening-praktijk (→ RFC-031), een expert-controleerbare
verrijkingsprocedure (→ RFC-027), en een CELEX-referentieconventie (→
schemawijziging op `references`). Bevindingen die daarvoor bruikbaar zijn,
loggen we hier met verwijzing naar het RFC-nummer.
