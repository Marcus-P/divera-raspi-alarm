# Vollständige Installation und Inbetriebnahme

**Dokumentationsstand: 0.1.0**

Diese Anleitung führt von einer leeren microSD-Karte bis zur geprüften Inbetriebnahme.

> **Stand:** Die Softwareinstallation ist vorbereitet. Schritte, die reale Hardware, den konkreten Rauchwarnmelder oder das reale DIVERA-Konto voraussetzen, werden bei der ersten Inbetriebnahme verifiziert und anschließend mit den bestätigten Details ergänzt.

## 1. Voraussetzungen

### Hardware

- Raspberry Pi 4 Model B
- SanDisk High Endurance microSDXC 128 GB oder vergleichbarer Endurance-Datenträger
- geeignetes Raspberry-Pi-Netzteil
- Monitor und HDMI-Verbindung
- kabelgebundene Ethernet-Verbindung zum Router
- SONOFF ZBDongle-P (CC2652P)
- kurze USB-Verlängerung für den Zigbee-Dongle empfohlen
- kompatible frient/Develco Zigbee-Rauchwarnmelder
- vorhandener PIR-Bewegungsmelder

### PIR-Anschluss der bekannten Installation

| Leitung | Physischer Pin | Funktion |
| --- | ---: | --- |
| grau | 2 | +5 V |
| schwarz | 6 | GND |
| weiß | 16 | BCM GPIO23 |

**Achtung:** Raspberry-Pi-GPIO ist nicht 5-V-tolerant. Diese Zuordnung dokumentiert die bekannte vorhandene Installation. Bei einem anderen PIR muss dessen Ausgangsspannung und Schnittstelle vor Anschluss geprüft werden.

## 2. Raspberry Pi OS installieren

Mit Raspberry Pi Imager das zum Installationszeitpunkt aktuelle unterstützte **Raspberry Pi OS 64-bit Desktop** installieren.

Im Imager:

- eigenen Administrator-Benutzer und ein starkes Passwort setzen
- SSH aktivieren
- Zeitzone `Europe/Berlin` setzen
- kabelgebundenes Netzwerk verwenden; WLAN ist für dieses Projekt nicht erforderlich
- keine Projekt-Secrets im Imager hinterlegen

Die alte SD-Karte sollte bis zur abgeschlossenen Inbetriebnahme unverändert als Rückfallmöglichkeit aufbewahrt werden.

## 3. Erster Start

SD-Karte einsetzen, Ethernet und Monitor anschließen und den Raspberry Pi starten. Prüfen, dass Internetzugang besteht.

Der SONOFF ZBDongle-P darf bereits angeschlossen sein, kann aber auch später eingesteckt werden.

## 4. Projekt installieren

Das Repository ist öffentlich. Es wird kein GitHub-Token benötigt.

```bash
git clone --depth 1 --branch develop https://github.com/Marcus-P/divera-raspi-alarm.git /tmp/divera-raspi-alarm
sudo bash /tmp/divera-raspi-alarm/installer/bootstrap-public.sh
```

Die Bootstrap-Routine legt bereits die erste Installation versioniert unter `/opt/divera-raspi-alarm/releases/<Version>/` ab und setzt `/opt/divera-raspi-alarm/current` atomar darauf. Damit verwendet bereits die Erstinstallation denselben Rollback-Pfad wie spätere Updates.\n\nDer Installer:

1. prüft 64-Bit-ARM
2. installiert die Systempakete
3. richtet den lokalen Mosquitto-Broker ein
4. installiert die festgelegte Zigbee2MQTT-Version
5. richtet den lokalen Administrationsdienst ein
6. richtet den Alarmworker ein
7. installiert Dongle-Hotplug-Erkennung
8. richtet Kiosk und PIR-Displaysteuerung ein
9. begrenzt persistente Logs
10. aktiviert die Healthchecks
11. erzeugt nur verschlüsselte persistente Credential-Speicher
12. führt abschließend einen Selbsttest aus

Ein Fehler beendet die Installation. Nur ein bestandener Selbsttest gilt als erfolgreiche Softwareinstallation.

## 5. Neustart

Nach bestandenem Selbsttest:

```bash
sudo reboot
```

Der grafische Desktop startet automatisch. Solange noch keine DIVERA-Kiosk-URL konfiguriert ist, erscheint die lokale Administration. Später ist DIVERA Tab 1 und die Administration Tab 2.

## 6. SONOFF ZBDongle-P

Den ZBDongle-P möglichst über eine kurze USB-Verlängerung anschließen.

Das System sucht unter `/dev/serial/by-id/` nach dem Adapter und verwendet die stabile Geräteidentität statt `ttyUSB0`. Der Adaptertyp ist `zstack`.

Beim Einstecken wird die Erkennung automatisch ausgelöst, die Zigbee2MQTT-Konfiguration erzeugt und Zigbee2MQTT gestartet beziehungsweise neu gestartet.

Im Web-UI prüfen:

- Dongle erkannt
- Adapter `zstack`
- Zigbee2MQTT aktiv

## 7. DIVERA-Zugang einrichten

DIVERA wird mit getrennten Zugangsdaten nach dem Prinzip der minimalen Rechte betrieben: einem Alarm-Access-Key für Alarmierungen/Mitteilungen und, sofern für die Personen-/Statusabfrage erforderlich, einem dedizierten Systemnutzer-Key. Beide dürfen niemals persistent im Klartext gespeichert werden. Die endgültige Eingabe erfolgt über die Administrationsoberfläche beziehungsweise den dafür vorgesehenen Credential-Helfer.

Persistiert wird ausschließlich ein von systemd verschlüsseltes Credential unter `/etc/credstore.encrypted/`. Zur Laufzeit erhält der jeweilige Dienst den entschlüsselten Wert über sein flüchtiges systemd-Credential-Verzeichnis.

Nach einem Neustart ist **keine erneute Passworteingabe** erforderlich.

Die Schlüssel selbst gehören niemals in Git, `.env`, TOML, Shell-Skripte oder Dokumentation.

## 8. Testmodus und Testempfänger

Der Testmodus ist nach Installation aktiv.

Vor jedem Alarmtest:

1. DIVERA-Verbindung prüfen
2. Personenliste laden
3. einen oder mehrere konkrete Testempfänger auswählen
4. kontrollieren, dass der Testmodus weiterhin sichtbar aktiv ist

Ohne gültige Testempfänger muss das System den Versand verweigern.

Der Produktivmodus bleibt während der Erstinbetriebnahme gesperrt.

## 9. Rauchwarnmelder koppeln

Unter **Rauchmelder / Zigbee** das zeitlich begrenzte Pairing öffnen und den Rauchwarnmelder nach dessen Herstellerverfahren in den Pairing-Modus bringen.

Danach:

- verständlichen Gerätenamen vergeben
- Raum zuordnen
- Erreichbarkeit prüfen
- Batterie-/Batterie-low-Zustand prüfen
- Fehlerstatus prüfen
- Last-seen prüfen

**Hardware-Abnahmepunkt:** Bei der ersten realen Inbetriebnahme werden die tatsächlichen MQTT-Payloads des gekauften Geräts für `smoke`, `test`, `battery_low`, `fault` und Verfügbarkeit aufgezeichnet und gegen die Alarmklassifikation geprüft. Bis dahin wird die Produktivalarmierung nicht freigegeben.

## 10. PIR und Bildschirm prüfen

Der Pi bleibt eingeschaltet.

Prüfen:

1. nach eingestellter Leerlaufzeit schaltet der Monitor ab
2. Bewegung am PIR schaltet den Monitor wieder ein
3. DIVERA/Kiosk bleibt dabei erhalten
4. ein PIR-Fehler beeinträchtigt den Alarmworker nicht

## 11. Geplanten Systemtest konfigurieren

Standard:

- aktiviert
- Sonntag
- 12:00 Uhr
- Kennzeichnung `SYSTEMTEST – KEIN EINSATZ`

Wochentage sind einzeln auswählbar; die gemeinsame Uhrzeit steht in 15-Minuten-Schritten zur Verfügung.

Testempfänger ausdrücklich festlegen.

## 12. DIVERA-Produktivrouting abnehmen

Dieser Schritt erfolgt erst am realen DIVERA-Konto.

Zu validieren sind:

- tatsächliche Personen-/Relation-IDs
- tatsächlich verwendete Bereitschafts-/Statuswerte
- gewünschte Empfängerlogik der Feuerwehr
- Verhalten bei nicht erreichbarer DIVERA-API
- Verhalten bei veralteten oder nicht auflösbaren Statusinformationen

Es werden keine Status-IDs geraten oder fest im Projekt angenommen.

Erst nach erfolgreichem Test wird der Produktivmodus bewusst freigegeben.

## 13. End-to-End-Abnahmetest

Vor Produktivbetrieb mindestens prüfen:

- Neustart ohne Benutzereingriff
- Kiosk startet selbstständig
- DIVERA als erster Tab
- lokale Administration als zweiter Tab
- PIR Display-Aus/Ein
- Dongle nach Neustart erkannt
- alle Rauchmelder erreichbar
- Batterie-/Fehlerzustände sichtbar
- Melder-Selbsttest erzeugt **keinen** echten Feueralarm
- kontrolliertes Rauchereignis wird korrekt klassifiziert
- Testmodus begrenzt Empfänger tatsächlich
- technischer Fehler wird nicht als Feueralarm behandelt
- geplanter Systemtest erreicht nur konfigurierte Testempfänger
- Dienstabsturz wird automatisch wiederhergestellt
- Loggrößen bleiben begrenzt
- Neustart verlangt keine erneute Secret-Eingabe

## 14. Updates

Nach der Erstinstallation erfolgen Updates über **System → Updates** aus stabilen, unveränderlichen GitHub Releases, nicht über manuelles `git pull`. Vor dem ersten stabilen Release muss in den Repository-Einstellungen Release-Immutability aktiviert sein.

Updates müssen abwärtskompatibel sein, bestehende Daten automatisch migrieren und Rollback erlauben. Details siehe [UPDATES.md](UPDATES.md).

## 15. Noch nicht vorab verifizierbare Punkte

Folgende Punkte können erst mit der gelieferten Hardware beziehungsweise dem realen Konto endgültig bestätigt werden:

- konkrete `/dev/serial/by-id`-Kennung des gelieferten ZBDongle-P
- reales MQTT-Verhalten des gekauften Rauchwarnmelders
- reales PIR-/Monitor-Verhalten unter dem installierten Raspberry Pi OS
- DIVERA-Status-/Empfängerabbildung
- vollständiger echter End-to-End-Alarmtest

Diese Punkte sind Bestandteil der Inbetriebnahme und keine Annahmen im Produktionscode.
