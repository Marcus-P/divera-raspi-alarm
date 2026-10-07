# Anwenderdokumentation

**Dokumentationsstand: 0.1.0**

Diese Anleitung beschreibt den normalen Betrieb des DIVERA Raspberry Alarm Systems. Für Installation und technische Inbetriebnahme siehe [INSTALLATION.md](INSTALLATION.md).

> Das System ergänzt die lokale Alarmierung der Rauchwarnmelder. Die lokale Sirene des Rauchwarnmelders arbeitet unabhängig vom Raspberry Pi, Netzwerk und DIVERA.

## 1. Normalbetrieb

Nach dem Einschalten startet der Raspberry Pi selbstständig. Chromium öffnet DIVERA im Vollbild. Der Raspberry Pi bleibt dauerhaft eingeschaltet.

Der Bildschirm darf bei Inaktivität abschalten. Erkennt der angeschlossene Bewegungsmelder eine Bewegung, wird der Bildschirm wieder eingeschaltet. Der Bewegungsmelder schaltet nicht den Raspberry Pi selbst ein oder aus.

## 2. Administration öffnen

Im Kiosk laufen zwei Tabs:

1. DIVERA
2. lokale Administration

Mit **Strg+Tab** wird zwischen beiden Tabs gewechselt. Im normalen Betrieb ist DIVERA der sichtbare erste Tab.

Die Administration ist in folgende Bereiche gegliedert:

- **Übersicht** – Gesamtzustand des Systems
- **DIVERA & Routing** – Verbindung, Testmodus und Empfänger
- **Rauchmelder / Zigbee** – Rauchmelder, Batterie, Fehler und Pairing
- **Geplante Tests** – automatische Systemtests
- **Anzeige / Kiosk** – Bildschirm und Bewegungsmelder
- **System / Administration** – Dienste, Diagnose, Version und Updates

Referenzansichten befinden sich in [UI.md](UI.md).

## 3. Zustände auf der Übersicht

Ein gesunder Normalzustand bedeutet insbesondere:

- Mosquitto läuft
- Zigbee2MQTT läuft
- SONOFF ZBDongle-P ist erkannt
- konfigurierte Rauchmelder sind erreichbar
- keine Batterie-Warnung
- kein Gerätefehler
- Alarmdienst läuft
- Internet/DIVERA ist erreichbar
- Kiosk läuft

Ein technischer Fehler ist **kein Feueralarm**. Batterie-, Geräte- oder Verbindungsprobleme werden getrennt als DIVERA-Mitteilung behandelt und nicht als Einsatzalarm.

## 4. Testmodus

Nach einer Neuinstallation und während Inbetriebnahmearbeiten ist der Testmodus aktiv.

Solange der Testmodus aktiv ist, dürfen Alarmereignisse ausschließlich an die ausdrücklich ausgewählten Testempfänger gesendet werden. Können diese Empfänger nicht sicher bestimmt werden, wird kein DIVERA-Alarm versendet.

Der Testmodus wird nicht durch Neustart oder Softwareupdate automatisch deaktiviert.

Die Umschaltung in den Produktivbetrieb erfolgt erst nach abgeschlossener Inbetriebnahme und bestätigter Empfängerzuordnung.

## 5. Rauchmelder hinzufügen

Das Pairing wird über **Rauchmelder / Zigbee** gestartet. Die Freigabe ist zeitlich begrenzt und wird anschließend automatisch wieder geschlossen.

Nach dem Pairing erhält jeder Melder einen verständlichen Namen entsprechend seinem Montageort, zum Beispiel `rauchmelder_flur`.

Nach jeder Neueinrichtung sind mindestens zu prüfen:

- Erreichbarkeit
- Gerätename und Raum
- Batterie-/Batterie-low-Anzeige
- Fehlerstatus
- letzter Kontakt
- Testfunktion

Die genaue Bedienfolge am gekauften Rauchmelder wird nach der ersten Hardware-Inbetriebnahme anhand des realen Geräts ergänzt.

## 6. Batterie und technische Fehler

`battery_low` ist eine technische Warnung und darf keinen Feueralarm erzeugen. Gleiches gilt für Gerätefehler und länger nicht erreichbare Melder.

Bei einer technischen Warnung ist die Ursache zeitnah zu prüfen. Wiederholte identische Fehler sollen vom System zusammengefasst werden, damit keine Meldungsflut entsteht.

## 7. Geplante Systemtests

Unter **Geplante Tests** kann der automatische Test ein- oder ausgeschaltet werden.

Auswählbar sind Montag bis Sonntag unabhängig voneinander. Für alle gewählten Tage gilt eine gemeinsame Uhrzeit in 15-Minuten-Schritten. Standard ist **Sonntag, 12:00 Uhr**.

Der automatische Test ist als **SYSTEMTEST – KEIN EINSATZ** gekennzeichnet.

Er prüft die elektronische Verarbeitungskette ab MQTT bis DIVERA. Er ersetzt **nicht** die physische Prüfung von Rauchsensor, Sirene oder Zigbee-Funkstrecke des Melders.

## 8. Softwareupdates

Unter **System → Updates** werden installierte und verfügbare stabile Versionen samt Release Notes angezeigt. Die Installation erfordert eine ausdrückliche Bestätigung.

Updates stammen ausschließlich aus veröffentlichten GitHub Releases. Entwicklungsstände aus `develop` werden produktiven Geräten nicht als normales Update angeboten.

Vor der Aktivierung einer neuen Version wird deren Integrität geprüft. Die vorherige Version bleibt für ein Rollback erhalten. Schlägt der Healthcheck nach einem Update fehl, wird auf die vorherige Version zurückgeschaltet.

Updates dürfen bestehende Konfiguration, gekoppelte Zigbee-Geräte oder verschlüsselte Zugangsdaten nicht löschen und keine manuelle Neueinrichtung verlangen.

## 9. Neustart und Stromausfall

Nach Stromausfall oder Neustart soll das System ohne Benutzereingriff wieder hochfahren. Für die gespeicherten verschlüsselten Credentials ist keine Passworteingabe beim Boot erforderlich.

DIVERA wird wieder als erster sichtbarer Kiosk-Tab geöffnet.

## 10. Was Anwender nicht tun sollten

Nicht erforderlich und im Normalbetrieb zu vermeiden sind:

- manuelles Bearbeiten von Dateien unter `/etc` oder `/var/lib`
- `git pull` als Updateverfahren
- Löschen des Zigbee2MQTT-Datenverzeichnisses
- Neuinstallation zur Behebung normaler Softwareprobleme
- Speicherung von DIVERA-Schlüsseln in Textdateien
- dauerhafte Freigabe des Zigbee-Pairings

## 11. Wenn etwas nicht funktioniert

Zuerst **Übersicht** und anschließend **System / Administration** prüfen. Dort sollen Dienstzustände und die letzten begrenzten Diagnoseinformationen sichtbar sein.

Bei einem ausgefallenen Dienst versucht das System zunächst einen gezielten Neustart. Ein später aktivierter Watchdog kann bei wiederholt fehlgeschlagener Wiederherstellung den Raspberry Pi neu starten.

Die lokale Sirene eines Rauchwarnmelders bleibt von diesen Softwarefunktionen unabhängig.
