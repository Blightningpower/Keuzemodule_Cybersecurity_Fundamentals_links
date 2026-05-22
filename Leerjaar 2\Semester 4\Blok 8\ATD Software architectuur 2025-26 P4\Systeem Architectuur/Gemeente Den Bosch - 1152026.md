##### **Gemeente Den Bosch - 11/5/2026**



**Wat doet een gemeente?**

*bevoegdheden:*

* lokaal beleid

  * bouw van theater
  * aanleg fietspad
  * bouwen van woningen
* uitvoeren landelijke wetten

  * uitgeven paspoorten en identiteitskaarten

ambtelijke organisatie door gemeentesecretaris



*vijf sectoren:*

* BO (strafafdeling bestuursondersteuning)
* MO (maatschappelijke ontwikkeling)
* D\&B (dienstverlening en bedrijfsvorming)
* SB (stadsbeheer)
* SO (stadsontwikkeling)
* WXL (sector Weener XL, social werkbedrijf)



*dienstverlening en bedrijfsvorming*

ICT:

* DW (digitale werkomgeving)
* INFRA (infrastructuur)
* CIM (concern informatiemanagement)



*informatiemanagement*

SIM MO/WXL (sociale ondersteuning, privacy belangrijk), SIM D\&B, SIM SO/SB

* functioneel beheerders
* projectleiders
* architect
* BI
* sectoriale specialisten

  * GEO (SO/SB)
  * informatiebeheer (D\&B)
  * i-adviseurs (CIM)
  * ICT-strateeg (CIM)



*projectmethodieken*

prince2 = Waterval, geschikt voor lage technische complexiteit en lage veranderlijke Eisen

agile: 

* lean (kwaliteitsverbetering)
* scrum (ontwikkeling)
* Kanban (beheer)



*referentie architecturen*

* NORA (Nederlandse overheid referentie architectuur)
* MARIJ (model architectuur voor de rijksdiensten)
* PETRA (provincie enterprise referentie architectuur)
* WILMA (waterschapsinformatie en logisch model architectuur)
* GEMMA (gemeentelijke modelarchitectuur)
* HORA (hoger onderwijs referentiearchitectuur)



*referentiecomponenten*

GEMMA Online -> alle referentiecomponenten





**Huidige applicatielandschap**

676 applicaties

294 total aantal koppelingen

15 forms in iBurgerzaken

139 forms in iTriplEforms

verschillende wetten over het behouden van en uiteindelijk vernietigen van bepaalde documenten, veel applicaties zijn daar niet voor gemaakt

koppelingen tussen applicaties lastig door wel/niet API, ouder/nieuwer

presentatieslides met diagrammen -> in taal archimate, lijkt deels op uml

financieel system in de verschillende sectoren gelijkgesteld

grootste problem = mensen die niet willen veranderen/wisselen naar andere applicaties





**Ontwikkelingen**

*datagedreven werken*

dataplatform, 3 lagen:

* ruwe data
* gemodelleerde data
* gebruikklare data (geanonimiseert of geabstraheert voor privacy)



*hoe werken wij datagedreven*

* gemeentebreed multidiscipplinair uitvoerend team

  * datavraag tot informatieproduct
  * data government office (DGO)
* vraaggestuurd (use cases)

  * functioneel ontwerp
* samen leren en doen (Scamander)
* één gemeentebreed dataplatform

  * security, privacy \& ethiek
  * landelijk model



*rollen in DET*

* DET coordinator
* domeinanalist
* data-analist
* datascientist
* data-engineer
* data-integratiespecialist
* data-architect



*levering en gebruik van data*

contracten en afspraken worden gemaakt over datalevering, (DLO (dataleveringsovereenkomst) en ILO (informatieleveringsovereenkomst))

letten op risico en misbruik



*soevereiniteit*

opslag data binnen de EER (binnen Europa)

onafhankelijk van niet-Europese overheden

POC 's-hertogenbosch, zaanstad, ede en Amsterdam voor digitale soevereine werkplek



*common ground (dienstverlening)*

modernisering dreigt te stagneren

te veel op processen (processilo's ontstaan) gebaseerd, spaghetti tussen databases op eigen lag, los van processen, servicelaag ertussen

hierdoor geen synchronisatie tussen databases

privacy makkelijker te borgen

inwoner/ondernemer heeft meer regie op persoonsgegevens



5 lagen:

* interactie (kanalen zoals websites, formulieren, post, email)
* processen (proces apart afgehandeld van interactie kanaal)
* connectiviteit
* diensten (api-laag)
* data (data maar één keer opgeslagen. veel bestaande applicaties komen met eigen database waar gegevens naar gekopieerd moeten. dit is foutgevoelig en slecht voor privacy)

standaarden:

interfaces: kanalen (design systems voor cohesie)

processen: business rules

integratie: FSC (federatieve service connectiviteit)

API's: GGM (gemeentelijk gegevens model)

data: registratiesysteem



laag 0: Haven+, infrastructuur laag, kubernetes





