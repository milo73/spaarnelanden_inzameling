# Spaarnelanden Inzameling Container Monitor

## Overzicht

Dit Python-script is ontworpen om de status van uw Spaarnelanden afvalcontainer te monitoren. Het haalt gegevens op van de Spaarnelanden website en geeft informatie weer zoals de vullingsgraad, laatste ledigingsdatum en andere relevante details van uw specifieke container.

## Functies

- Periodiek ophalen van containergegevens van de Spaarnelanden website
- Weergave van de vullingsgraad en status van de container
- Caching van gegevens om onnodige netwerkverzoeken te verminderen
- Configureerbaar via omgevingsvariabelen
- Uitgebreide foutafhandeling en logging

## Vereisten

- Python 3.7 of hoger
- pip (Python package installer)

## Installatie

1. Clone deze repository of download de scripbestanden naar uw lokale machine.

2. Navigeer naar de projectmap in uw terminal.

3. Installeer de vereiste Python-bibliotheken:

   ```
   pip install gazpacho requests python-dotenv
   ```

## Configuratie

1. Maak een bestand met de naam `.env` aan in dezelfde map als het script.

2. Voeg de volgende inhoud toe aan het `.env` bestand:

   ```
   CONTAINER_NUMBER=uw_container_nummer
   UPDATE_INTERVAL=10
   ```

   Vervang `uw_container_nummer` door het nummer van uw Spaarnelanden container. U kunt het update-interval (in minuten) aanpassen door de waarde van `UPDATE_INTERVAL` te wijzigen.

## Gebruik

1. Open een terminal en navigeer naar de map waarin het script zich bevindt.

2. Voer het script uit met het volgende commando:

   ```
   python spaarnelanden_inzameling.py
   ```

3. Het script zal beginnen met het ophalen en weergeven van de containergegevens. Het zal dit proces herhalen volgens het ingestelde interval.

4. Om het programma te stoppen, drukt u op `Ctrl+C` in de terminal.

## Uitvoer

Het script geeft de volgende informatie weer voor uw container:

- Vullingsgraad (in percentage)
- Status (bijv. "Ingepland", "Niet ingepland vandaag")
- Type afval (bijv. Papier, Plastic, Glas)
- Datum laatste lediging
- Of de container buiten gebruik is
- Of de container vandaag is geleegd
- Tijdstip van de laatste gegevenscontrole

## Foutafhandeling en Logging

- Het script logt informatie, waarschuwingen en fouten naar de console.
- Bij netwerkfouten of problemen met gegevensverwerking worden foutmeldingen gelogd.
- Als uw containernummer niet wordt gevonden, wordt een waarschuwing gelogd.

## Aanpassen

U kunt het script aanpassen aan uw behoeften:

- Wijzig de `cache_duration` in de `ContainerDataFetcher` klasse om de cache-duur aan te passen.
- Pas de logging-instellingen aan in de `logging.basicConfig()` aanroep voor meer of minder gedetailleerde logs.
- Voeg extra velden toe aan de `ContainerData` klasse als u meer informatie wilt opslaan of weergeven.

## Bijdragen

Bijdragen aan dit project zijn welkom! Als u een bug vindt of een verbetering voorstelt, open dan een issue of dien een pull request in.

## Disclaimer

Dit script is niet officieel geassocieerd met of ondersteund door Spaarnelanden. Het is een onafhankelijk hulpmiddel dat openbaar beschikbare gegevens gebruikt. Gebruik het op eigen risico en verantwoordelijkheid.

## Licentie

Dit project is gelicentieerd onder de MIT-licentie. Zie het `LICENSE` bestand voor details.
