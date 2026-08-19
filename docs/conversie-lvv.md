# Conversieverantwoording — LVV geconsolideerd 13-12-2023

Hoe `regulation/eu/eu_verordening/landbouwvrijstellingsverordening/2023-12-13.yaml`
tot stand kwam. De conversie is **deterministisch** (script, geen LLM in de
tekstverwerking): `tools/convert_lvv.py`, draaiend op de tekstextractie
(`pdftotext -layout`) van `docs/CELEX_02022R2472-20231213_NL_TXT.pdf` — de
officiële geconsolideerde Nederlandse taalversie van EUR-Lex.

Aanleiding: de verrijkingspijplijn van de editor liep vast op de omvang van het
document (tokenlimiet bij de LLM-conversie). Deterministisch converteren is
voor dit brondocument sowieso de betere route: verbatim by construction.

## Versie-anker

| veld | waarde |
|---|---|
| CELEX | `02022R2472-20231213` |
| ELI | `http://data.europa.eu/eli/reg/2022/2472/2023-12-13` |
| geconsolideerde wijzigingen | M1: Verordening (EU) 2023/2607 (22-11-2023) |
| `publication_date` | 2022-12-21 (PB L 327, publicatie basisverordening) |
| `valid_from` | 2023-12-13 (consolidatiedatum) |
| `valid_to` | 2029-12-31 (artikel 64: "van toepassing … tot en met 31 december 2029") |

Let op: EUR-Lex merkt de geconsolideerde tekst aan als "louter ter informatie
en juridisch niet bindend"; authentiek zijn de in het Publicatieblad
gepubliceerde besluiten. Wij spiegelen de consolidatie omdat die de geldende
tekst als één geheel weergeeft; bij twijfel is het Publicatieblad leidend.

## Bewerkingsregels (de enige afwijkingen van de ruwe extractie)

1. **Paginakoppen** (`02022R2472 — NL — 13.12.2023 — 001.001 — <p>`) en
   paginascheidingen verwijderd.
2. **Consolidatie-apparaat** (`►B`, `►M1`, `◄`) verwijderd; de gewijzigde
   tekst zelf blijft uiteraard staan (raakt alleen artikel 28, leden 3 en 4).
3. **Afbrekingen** (zachte koppeltekens over regeleinden, 922 stuks)
   teruggevoegd tot hele woorden.
4. **Regelhervloei**: omgebroken regels zijn samengevoegd tot logische regels;
   leden (`1.`), letters (`a)`), romeinen (`i)`) en gedachtestreepjes behouden
   hun eigen regel. Bijlagen zijn **niet** hervloeid (tabellen/formulieren),
   alleen geschoond.
5. **Voetnoten** (45 stuks, doorlopend genummerd): de voetnoottekst is van de
   paginavoet verplaatst naar het einde van het artikel waarin de verwijzing
   staat. De tekst zelf is verbatim; alleen de positie is een keuze, omdat
   paginapositie in YAML betekenisloos is. Alle 45 zijn geplaatst.
6. **Artikeltitels** staan als vetgedrukte eerste regel in `text:` (dezelfde
   conventie als de BWB-harvester). Artikel 64 heeft in de bron geen titel.
7. **Hoofdstukken** (I–IV): het schema kent geen hoofdstukveld; de hoofdstuk-
   grenzen staan als YAML-commentaar boven het eerste artikel van elk
   hoofdstuk. Hoofdstuk-lidmaatschap is juridisch relevant (artikel 3 eist
   "alle voorwaarden van hoofdstuk I") en moet bij de verrijking expliciet
   gemodelleerd worden — niet uit het commentaar afgeleid.
8. **Bijlagen I–III** zijn artikelen met nummer `Bijlage I/II/III`. Bijlage I
   (kmo-definitie) bevat eigen artikelen 1–6; die zijn onderdeel van de
   bijlagetekst, niet van de hoofdartikelen.
9. **Considerans**: de geconsolideerde versie bevat geen overwegingen; er is
   dus ook niets als `preamble` opgenomen. Wie de considerans nodig heeft
   (duiding, nooit norm — besluit 8) raadpleegt de basisverordening
   (`docs/CELEX_32022R2472_NL_TXT.pdf`).

## Controles

- Schema-validatie: groen op v0.5.6 (`just validate` in de regelrecht-repo).
- Artikelen 1–64 aaneengesloten, geen gaten; 3 bijlagen.
- Alle 45 voetnoten geplaatst (doorlopende nummering als ingebouwde controle).
- M1-passage (artikel 28) aanwezig, apparaat verwijderd.
- Steekproeven: artikel 1 (toepassingsgebied), artikel 4 (aanmeldingsdrempels,
  bedragen intact), artikel 64 (slot), einde bijlage III.

## Padkeuze

`regulation/eu/eu_verordening/…` — bewust `eu/` en niet `nl/`: de
jurisdictie-laag in het pad hoort de werkelijkheid te volgen. De
corpus-conventie in regelrecht is vandaag `regulation/nl/…` (zie
`docs/rfc-dekkingsanalyse.md`, blokkade 2); dit dossier kaart de
generalisatie aan in plaats van eromheen te werken.
