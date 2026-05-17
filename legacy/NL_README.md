# Agent & Coach Feedback Applicatie

## Overzicht
De Agent en Coach Feedback Applicatie is een Tkinter-gebaseerde desktoptool, ontwikkeld in Jupyter Notebook. Het biedt een gebruiksvriendelijke interface die samenwerking tussen agents en coaches ondersteunt. Functionaliteiten omvatten het bekijken van feedback, genereren van rapporten en beheren van accounts.

## Details over de creatie van de applicatie

1. **Programmeertaal Python**:
   - De applicatie is volledig gebouwd in Python, gekozen vanwege de eenvoud, leesbaarheid en uitgebreide standaardbibliotheek.

2. **GUI-framework Tkinter**:
   - Een ingebouwde Python-bibliotheek gebruikt voor het ontwerpen van de grafische interface, waaronder:
     - Frames: Voor schermindelingen zoals login, hoofdmenu en feedbackschermen.
     - Widgets: Knoppen, labels, invoervelden, dropdowns en lijstweergaven voor gebruikersinteractie.
     - Event Loop (`mainloop`): Zorgt ervoor dat de app responsief blijft.

3. **Bibliotheken en standaardmodules**:
   - **tkinter**: Voor de GUI-interface.
   - **csv**: Voor het lezen en schrijven van tabulaire gegevens naar/van `data.csv`.
   - **datetime**: Voor het verwerken van tijdstempels, datumfilters en rapportgeneratie.
   - **logging**: Voor foutopsporing en waarschuwingsberichten.
   - **time**: Voor het genereren van unieke ID's (op basis van tijdstempels).

4. **Databeheer**:
   - **CSV-bestanden**: Gegevens worden opgeslagen en beheerd in `data.csv`.
     - Gegevens omvatten:
       - **Gebruikers**: Gebruikersnaam, wachtwoord en rol (Agent of Coach).
       - **Feedback**: Feedback-ID, agent, feedbacktekst, status en tijdstempels.
   - Rapporten worden geëxporteerd als nieuwe CSV-bestanden naar de map `src`.

5. **Applicatiestructuur**:
   - **Objectgeoriënteerd Ontwerp**:
     - **App**: Beheert de applicatie, initialiseert de GUI en regelt navigatie tussen schermen.
     - **Schermklassen** (bijv. `LoginScreen`, `AgentMainMenu`, `CoachMainMenu`): Bevatten de layout en functionaliteit van elk scherm.
     - **Hulpmiddelenklassen** (bijv. `ReportGenerator`): Handelt specifieke taken zoals rapportgeneratie.
   - **Event-Driven Programming**: Het Tkinter-eventsysteem reageert op gebruikersacties zoals knopklikken en invoer.

6. **Ontwikkeltools**:
   - Jupyter Notebook: De app is ontwikkeld in een Jupyter Notebook, zoals vereist in de opdracht.

7. **Stijl en gebruikerservaring**:
   - **Consistente stijl**: Gebruik van vooraf gedefinieerde kleuren, lettertypen en lay-outconfiguraties.
   - **Responsive layout**: Grid-gebaseerde layouts passen componenten dynamisch aan.

8. **Belangrijkste functies**:
   - Rolgebaseerde toegang: Agents en Coaches hebben specifieke interfaces.
   - Gegevenspersistentie: Alle wijzigingen (nieuwe feedback, updates, rapporten) worden opgeslagen in `data.csv`.
   - Rapportgeneratie: Coaches kunnen prestatie-overzichten genereren en exporteren.
   - Profielbeheer: Gebruikers kunnen hun wachtwoord wijzigen.

9. **Beperkingen**:
   - Geen versleuteling voor wachtwoorden in het CSV-bestand.
   - Beperkte schaalbaarheid, omdat CSV-bestanden worden gebruikt in plaats van een database.
   - Geen ondersteuning voor meerdere gebruikers tegelijkertijd.

---

## Installatie en Setup

### Vereisten
1. Python 3.8 of hoger.
2. Jupyter Notebook.
3. Benodigde bibliotheken:
   - tkinter
   - csv
   - logging
   - time
   - datetime

### Installatiestappen
1. **Pak het ZIP-bestand uit**:
   - Download en pak het ZIP-bestand uit in een lokale map.
   - Zorg ervoor dat de map de volgende bestanden bevat:
     - `bp4_app.ipynb`: De Jupyter Notebook met de applicatiecode.
     - `data.csv`: Het gegevensbestand.

2. **Controleer of Python is geïnstalleerd**:
   - Voer in een terminal of opdrachtprompt uit: `python --version`.
   - Indien niet geïnstalleerd, download Python van [python.org](https://www.python.org).

3. **Controleer Jupyter Notebook ondersteuning**:
   - Installeer Jupyter Notebook indien nodig: `pip install notebook`.
   - Verifieer de installatie met: `jupyter --version`.

4. **Open de applicatie in je IDE**:
   - Importeer de map als een nieuw project in je IDE (bijv. PyCharm of VS Code).

5. **Open het Notebook-bestand**:
   - Gebruik de Jupyter Notebook-integratie in je IDE.
   - Open `bp4_app.ipynb`.

6. **Voer alle cellen uit**:
   - Selecteer **Run All** in de Jupyter-interface.
   - Voer de laatste cel uit waarin de app wordt gestart:
     ```
     if __name__ == "__main__":
         app = App()
         app.mainloop()
     ```

7. **Applicatiegebruik**:
   - Gebruik de GUI om door de applicatie te navigeren.
   - Log in als Agent of Coach en voer acties uit.

---

## Gebruik van de applicatie

### Login
1. Selecteer je rol (Agent of Coach).
2. Voer je gebruikersnaam en wachtwoord in:
   - **Agent**: gebruikersnaam `agent1`, wachtwoord `pass123`.
   - **Coach**: gebruikersnaam `coach1`, wachtwoord `pass456`.
3. Klik op "Login" om door te gaan.

### Hoofdmenu voor Agents
1. Beheer profielinstellingen.
2. Bekijk en filter feedback.
3. Log uit.

### Hoofdmenu voor Coaches
1. Beheer profielinstellingen.
2. Maak accounts voor agents of andere coaches.
3. Werk feedbackstatus bij.
4. Voeg feedback toe.
5. Genereer rapporten over prestaties van agents.
6. Log uit.

---

## Bestandsstructuur (na uitpakken van ZIP)
```
LU4/
├── src/
│   ├── bp4_app.ipynb        # Applicatiecode
│   ├── data.csv             # Gegevensbestand
├── Tests/
│   ├── test_app.ipynb       # Testcode
│   ├── data.csv             # Testgegevens
└── README.md                # Documentatie
```

### Gegevensbeheer

#### Gegevensopslag
- Gegevens worden opgeslagen in `data.csv` voor eenvoud.
  - **Gegevenstypen**:
    - **Gebruikers**: Bevat gebruikersnaam, wachtwoord en rol.
    - **Feedback**: Bevat feedback-ID, agent, tekst, status en tijdstempels.

#### Nieuwe gegevens toevoegen
- Coaches en agents kunnen hun wachtwoord wijzigen via het profielscherm; wijzigingen worden automatisch opgeslagen in `data.csv`.
- Coaches kunnen nieuwe accounts toevoegen, feedback geven en de feedbackstatus bijwerken via de applicatie-interface.
- Alle wijzigingen worden automatisch opgeslagen in `data.csv`.

#### Gegenereerde rapporten
- Rapporten worden direct in de applicatie gegenereerd.
- Ze worden geëxporteerd als nieuwe CSV-bestanden naar de `src`-map, waar ze kunnen worden geopend en bekeken.