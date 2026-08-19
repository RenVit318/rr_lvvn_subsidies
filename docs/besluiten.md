# Dossierbesluiten — subsidieroutes onder de LVV

Logboek van de richtinggevende besluiten voor dit dossier. Elk besluit staat er
met zijn reden; wat hier staat is leidend totdat een later besluit het expliciet
herroept.

## Het idee

Beleidsmedewerkers met een staatssteun-idee moeten kunnen verkennen welke
artikelen van een vrijstellingsverordening een route bieden. Het instrument
daarvoor: modelleer per artikel de toepasselijkheidsvoorwaarden
(steuncategorie, sector, begunstigde, drempels, uitsluitingen) plus de gemene
bepalingen van hoofdstuk I, en draai alle artikel-endpoints tegen een deels
ingevuld maatregelprofiel. De uitkomst valt in drie emmers: **uitgesloten**
(met de reden uit de trace), **mogelijk, mits …** (met de openstaande
vereisten als checklist) en **onbekend** (ontbrekende informatie — tegelijk de
volgende vraag aan de beleidsmedewerker).

## Besluiten (11 augustus 2026)

1. **LVV eerst.** De eerste desk-cyclus richt zich op de
   Landbouwvrijstellingsverordening (Verordening (EU) 2022/2472). De AGVV
   volgt in een latere cyclus; de hoofdstuk-I-systematiek die we voor de LVV
   bouwen is daar herbruikbaar. De-minimis (landbouw) blijft voorlopig buiten
   scope.

2. **Breedte vóór diepte.** Eerst alle artikelen verbatim in het corpus, met
   per artikel alléén de toepasselijkheidsvoorwaarden machine-leesbaar. Het
   filter werkt dan over de hele verordening; volledige berekeningen
   (steunintensiteiten e.d.) verdiepen we daarna per artikel.

3. **Corpus vóór productvorm.** De vorm van het filter (PoC-portaal,
   headless beslis-service, in-editor) kiezen we pas als het corpus staat.

4. **Het oude experimentcorpus is referentie, geen startpunt.** De AGVV/LVV-
   modellen uit `regelrecht-mvp-experimentfase2` zijn machinaal vertaald en
   nooit geverifieerd. Ze dienen alleen nog als inventaris: welke artikelen,
   welke endpoints, welke testvectors. Er wordt niets uit overgenomen.

5. **De authentieke Nederlandse taalversie is de bron.** EUR-Lex publiceert de
   officiële geconsolideerde NL-tekst (Nederlands is een authentieke taal van
   EU-recht). De `text:`-velden spiegelen die tekst verbatim, inclusief
   eventuele errata; er is geen vertaalstap. Elke versie wordt verankerd met
   CELEX-nummer van de consolidatie en ELI.

6. **Eén model, geen aparte verkennings-ontologie.** De betekenis van een term
   wordt bepaald door de vraag *wie hem afleidt*, niet door wie het model
   gebruikt. Leidt de verordening een begrip zelf af (zoals kmo via bijlage I),
   dan is het een afgeleide knoop — ook als het filter er in de praktijk stopt
   en de mens laat antwoorden. Het verschil tussen verkenning (filter) en
   uitvoering is een verschil in *evaluatiegrens*, nooit in termsemantiek.
   Breedte-eerst laat afleidbare termen tijdelijk aan de grens liggen: dat is
   een gemarkeerd gat ("nog niet afgeleid"), nooit een herdefinitie tot invoer.

7. **Vocabulaire-mapping is productlaag.** De brug van beleidstaal ("stallen
   verduurzamen") naar verordeningscategorieën ("investeringssteun, art. 14")
   staat niet in de wettekst en hoort dus niet in het model. Hetzelfde geldt
   voor vraagvolgorde en omgang met onbekenden: querymodus, geen modellering.

8. **Considerans is duiding, geen norm.** De overwegingen van de verordening
   zijn het EU-analogon van de toelichting: ze mogen interpretatie
   ondersteunen, maar nooit de grondslag van een regel in `machine_readable`
   zijn.

9. **Zekerheid komt uit desk-cycli, niet alleen uit de pijplijn.** De
   verrijkingspijplijn van de editor borgt letter-traceerbaarheid
   (reverse-validate) en untranslatables, maar niet de concept-hygiëne
   (wie-leidt-af, valse vrienden, wees-parameters). Die borging draait als
   aparte desk-audits over het corpus heen. De modelleerconventies van dit
   dossier worden in deze repo vastgelegd zodat ze meereizen naar elke
   verrijkingsrun.

## Verhouding tot regelrecht

Dit dossier is geen bestaand spoor van regelrecht maar een nieuw soort spoor:
van uitvoering van vastgesteld recht jegens een burger (run-time) naar toetsing
van een voorgenomen maatregel aan hoger recht (design-time). Het steunt wel
volledig op de bestaande machinerie — lex superior kent de EU-lagen al, en het
`open_terms`/`implements`-patroon is precies hoe een latere subsidieregeling
zich aan een LVV-artikel zou hechten. Het convergentiepunt: zodra een idee een
regeling wordt, wordt die regeling een gewoon NL-instrument in het corpus met
verwijzingen omhoog naar zijn LVV-grondslag, en bedienen hetzelfde model en
dezelfde engine zowel de ontwerpvraag ("mag dit?") als de uitvoeringsvraag
("krijgt deze aanvrager steun?").
