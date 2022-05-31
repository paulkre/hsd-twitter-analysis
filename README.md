# HSD Twitter Analyse

Twitter Analyse der Accounts der Hochschule Düsseldorf und ihrer Konkurenz.

## Setup

Kopiere die Datei `sample.env` zu `.env` und trage dort die Zugangsdaten deines Twitter Developer Accounts ein.

## Follower eines Nutzers herunterladen

Du kannst die Follower eines Nutzers herunterladen. Die Daten werden unter `data/followers/<username>.csv` gespeichert. Führe dazu den folgenden Befehl aus:

```
python get_followers.py <username>
```

## Follower der Nutzer in einer Liste herunterladen

Du kannst auch die Follower aller Nutzer in einer CSV Datei herunterladen. Dabei kannst du optional einen Start-Index definieren, falls du ab einer bestimmten Zeile in der CSV Datei mit dem Download beginnen möchtest. Die Daten werden in dem Ordner `data/followers/cache/<input_filename>/<follower_id>_<user_id>.csv` zwischengespeichert und am Ende unter `data/followers/<input_filename>_lvl2.csv` zusammengefasst. Führe dazu den folgenden Befehl aus:

```
python get_follower_followers.py <data.csv> [start_index]
```
