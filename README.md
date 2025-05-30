# Water Level Monitor

Ett användarvänligt system för övervakning av vattennivåer i realtid. Systemet är designat för att ge visuell feedback, statusindikeringar och historisk analys av nivådata från flera sensorer.

## Dashboard Vy

När applikationen startar visas en översikt:

- Alla aktiva sensorer visas med färg, status och aktuell vattennivå i procent.
- Klicka på en sensor för att visa mer detaljer.
- Klicka på `+ Add Sensor` för att lägga till fler enheter (max 12).
- `Settings` används för att justera systeminställningar.

### Sensor-kort

Varje sensor representeras av ett kort med följande information:

| Sensor | Tank           | Status   | Färg  | Nivå   |
|--------|----------------|----------|-------|--------|
| 1      | Main Tank      | Critical | Rosa  | 86.7%  |
| 2      | Reserve Tank   | Normal   | Blå   | 74.5%  |
| 3      | Overflow Tank  | Warning  | Gul   | 76.6%  |

#### Färgkoder för status
- 🔴 **Röd** = Farligt hög nivå
- 🟡 **Gul** = Varningsnivå
- 🔵 **Blå** = Normal nivå


## Sensor Detail-sida

Klickar man på ett sensor-kort öppnas detaljsidan som visar:

- Status (inkl. färgkod)
- Nuvarande vattennivå
- Batteristatus
- Tidigare nivåer (senaste 7 dagar)

### Vattennivå-historik (diagram)
- Interaktivt diagram som uppdateras automatiskt
- Färgade gränser för:
  - 🟡 Warning Level: 75%
  - 🔴 Critical Level: 85%


## Inställningar

### 1. Alarm Settings
- `Warning Level (%)`: Tröskel för varning (t.ex. 75%)
- `Critical Level (%)`: Tröskel för kritiskt larm (t.ex. 85%)

### 2. General Settings
- `Data Update Interval`: Exempelvis var 15:e minut
- `Display Settings`: Möjlighet till helskärmsläge

### 3. Sensor Settings
- Aktivera/inaktivera individuell sensor
- `Max Physical Level`: Maxhöjd i cm (t.ex. 100 cm)
- `Offset`: Kalibrering av sensoravläsning
- Kalibreringsknapp för manuell justering


## Exportfunktion

Klicka på `Export CSV` för att:

- Spara aktuell systemdata i CSV-format
- Perfekt för rapporter, felsökning eller analys


## Max antal sensorer: 12

Varje sensor har en unik visuell identitet och kalibreringsmöjligheter.
