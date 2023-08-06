<a href="Development.en.md"><img src="images/en.svg" valign="top" align="right"/></a>
<a href="Development.de.md"><img src="images/de.svg" valign="top" align="right"/></a>
<!--[![Version][version-badge]][version-url]-->
[![License][license-badge]][license-url]
<!--
[![Bugs][bugs-badge]][bugs-url]
-->

[![Logo][logo]][project-url]

### Einrichtung der Entwicklungsumgebung

##

[![ggshield][ggshield]][ggshield-url]
### GitGuardian Shield einrichten (falls gewünscht)

Um die Überprüfungen von [GitGuardian][ggshield-url] zu verwenden, benötigst 
du zunächst ein kostenloses Konto. Der Link im vorherigen Satz führt dich d
irekt auf die Startseite und nutze dann den ```Start for free``` - Button. 
Nachdem du dein Konto eingerichtet hast, kannst du über ```API``` / 
```Personal access tokens``` die benötigten persönlichen Zugangstoken erzeugen 
lassen. Nach dem Drücken von ```Create token``` gib deinem Token einen Namen,  
damit du später ekennen kannst, wofür du es verwendet hast und nimm dann die 
folgenden Einstellungen vor:

- ```Expires:``` Für das Token, das du in deiner Entwicklungsumgebung einsetzen
möchtest, empfehle ich eine Ablauffrist von 6 Monaten bis max. 1 Jahr. Für das
Token, das du auf GitHub verwenden möchtest, empfehle ich max. 6 Monate.
- ```Scope:``` Bitte nur ```scan``` auswählen.

Nachdem du den ```Create token```-Button gedrückt hast, wird dir dein neues 
Zugangstoken angezeigt (etwas unauffällig ganz oben, grün hinterlegt). Kopier 
es in eine Datei oder in deinen Passwort-Manager. Du wirst es nie wieder sehen. 
Nachdem du die beiden Token erzeugt hast, müssen sie "nur noch" an den richtigen 
Stellen hinterlegt werden, um dann zum Abschluss GitGuardian als GitHub App zu 
aktivieren.

#### Integration von GitGuardian in die pre-commit Überprüfungen

Die eigentliche Integration von GitGuardian in die pre-commit Überprüfungen hat
dieses Blueprint bereits für dich vorgenommen. Du musst allerdings noch dein 
Zugangstoken an geeigneter Stelle hinterlegen und bei der Vorbereitung des 
virtuellen Python-Environment GitGuardian installieren. Die Details für die
Installation erfährst du im Abschnitt 
**Vorbereitung des virtuellen Python-Environments**. Hier bleiben wir erst
einmal bei den geeigneten Stellen für deine Zugangstoken.

Du kannst dein Token entweder in der Umgebungsvariablen ```GITGUARDIAN_API_KEY```
speichern (z.B. indem des es in ```~/.bashrc``` exportierst) oder es in die 
Konfigurationsdatei von GitGuardian ```~/.gitguardian.yml``` eintragen (meine
bevorzugte Variante). Bei der zweiten Variante hast du den Vorteil, dass du
GitGuardian an der gleichen Stelle an deine persönlichen Bedürfnisse anpassen
kannst (siehe GitGuardian-Dokumentation) und, obwohl es in der Dokumentation
nicht zu finden ist, hier auch **dein Zugangstoken** hinterlegen kannst. 
(Ich liebe es, wenn die Docus das Wichtigste verschweigen.) Deine 
Konfigurationsdatei könnte dann in etwa so aussehen:

```
api-key: <Dein gerade erzeugtes persönliches Zugriffstoken>
...
# weitere persönliche Einstellungen
```

#### Integration von GitGuardian in die GitHub-Workflows

Als erstes solltest du deine Repositories schon mal vorbereiten. Dazu musst du
für jedes Repository in die Einstellungen (```Settings```) gehen. Dort findest
du unter ```Secrets``` den Punkt ```Actions```. Nutze den 
```New repository secret``` - Button. Dort kannst du dann dein zweites 
persönliches Zugriffstoken eintragen. Bei ```Name``` musst du den Namen 
**GITGUARDIAN_API_KEY** verwenden und bei ```Value``` dein Token. Fertig!

Abschliessend muss GitGuardian dann noch als GitHub-App aktiviert werden (zu 
finden unter deinen Konto-Settings / Applications). Der Vorgang muss allerdings 
**auf GitGuardian** eingeleitet werden. Dazu gehst du im [Dashboard][gg-dash] auf 
```INTEGRATIONS```. Unter *VCS Integrations* findest du GitHub und dort musst
du dann nur noch den ```Install``` - Button drücken und die Einstellungen 
vornehmen. Damit hast du es dann geschafft.

##

[![python][python]][python-url]
### Vorbereitung des virtuellen Python-Environments

Damit in Visual Studio Code (meine favorisierte IDE) die Umschaltung zwischen 
unterschiedlichen virtuellen Python-Environments funktioniert, müssen alle 
VENVs unterhalb einen *zentralen" Sammelverzeichnisses liegen. Ich habe mich
für ```~/.venv``` entschieden. Falls du einen anderen Ort favorisisierst, musst
du die Skript-Datei ```script/run-in-env``` an deine Konfiguration anpassen. 
Ungefähr in der Mitte des Skripts findest du eine for-Schleife 
```for venv in venv .venv . **~/.venv**; do```. Dort musst du dann statt des 
hervorgehobenen zentralen VENV-Verzeichnis in meiner Konfiguration dein zentrales
VENV-Verzeichnis eintragen.

Falls du noch kein zentrales Verzeichnis hast, unter dem du alle VENVs 
"gesammelt" hast, lege bitte ein neues an. Du brauchst Schreibrechte in diesem 
Ordner, also kann es irgendwo in deinem Homeverzeichnis liegen.

Da Home Assistant mit aktuelle mit Python 3.9 entwickelt wird, stell bitte 
sicher, das du einen passenden Python-Interpreter installiert hast. Prüfen 
kannst du es mit ```python3.9 --version```. Wenn Python eine Versionsnummer 
anzeigt (in meinem Fall Python 3.9.5) kannst du fortfahren.

Wechsle bitte in dein neu angelegtes / vorhandenes zentrales VENV-Verzeichnis. 
Dort gib dann ```python3.9 -m venv 3.9``` ein. Damit wird ein neues virtuelles
Verzeichnis für deine Entwicklung einer Home Assistant Integration angelegt. 
Tipp: Ich habe mit in der ~/.bash_aliases einen Alias für 
```source ~/.venv/3.9/bin/activate``` definiert, so dass ich nur noch *p3.9*
aufrufen muss, wenn ich mit diesem virtuellen Environment arbeiten möchte.

Falls du deine Integration direkt auf deinem Rechner testen möchtest (z.B. in 
einem Docker-Container), dann empfehle ich dir, dafür ein zweites virtuelles 
Environment anzulegen, da Home Assistent alle Bibliotheken, die es verwendet, 
auf eine feste Version pinnt und so Updates für viele Libraries, die du mit 
pip installierst, von Home Assistant beim nächsten Start wieder rückgängig 
gemacht werden. Ich habe meine zweite virtuelle Python-Umgebung *ha-dev* 
genannt, aber auch hier kannst deiner Fantasie wieder freien Lauf lassen, und 
einen anderen Namen nehmen, falls gewünscht.

Nachdem das/die virtuellen Environment existieren, musst du eventuell noch die 
Datei ```.python-version``` anpassen. Dort wird der Name des virtuellen 
Environments eingetragen, das du für die Entwicklung deiner Integration 
verwenden möchtest.

#### Installation der benötigten Komponenten für pre-commit - Überprüfungen

Da Python leider nicht kompiliert wird, werden syntaktische Fehler ja leider 
erst erkannt, wenn der Code ausgeführt werden soll. Um während der Entwicklung 
bereits auf tatsächliche oder zumindest potentielle Fehler hingewiesen zu 
werden, benötigen wir noch einige Tools. Einige sind von Home Assistant bzw. 
von der Home Assistant Community (HACS) vorgeschrieben, einige hielt ich "nur" 
für sinnvoll und habe sie mit aufgenommen.

Bevor du mit der Installation der Installation der Komponenten beginnst, musst 
du allerdings zuerst dein virtuelles Environment mit 
```source ~/.venv/3.9/bin/activate``` oder deinem entsprchendem Alias 
aktivieren. Vermutlich wirst du schon wissen, das sich der Prompt ändert und 
du vor deinem Namen in Klammern das aktivierte virtuelle Environment angezeigt 
bekommst.

Anfangen möchte ich mit meiner ersten Empfehlung aus der ReadMe: Der 
Installation von GitGuardian Shield. Wer sich gegen die Überprüfung mit 
GGShield entschieden hat, kann diesen Schritt überspringen.

Um den GitGuardian Shield zu installieren, gib bitte den folgenden Befehl in 
einem Terminal:

```
pip install -U ggshield
```

Bei den restlichen Komponenten werde ich jeweils angebeben, ob sie von Home 
Assistant oder der HACS vorgeschlagen (also optional) oder fest vorgeschrieben 
sind, damit du selbst entscheiden kannst, welche Überprüfungen du ggf. 
weglassen oder gegen eine aus deiner Sicht bessere Variante der Überprüfung 
austauschen möchtest.

- pre-commit (Führt sämtliche Tests aus, bevor ein Commit zugelassen wird). 
Von Home Assistant vorgeschrieben:<br/>
Installation: ```pip install -U pre-commit```.
- Black (Quelltext Formatierer): Von Home Assistant und HACS vorgeschrieben. 
Installation: ```pip install -U black```.
- ISort (Sortierung der Imports): Von Home Assistant und HACS vorgeschrieben. 
Installation ```pip install -U isort```.
- PyLint (Python Linter): Von Home Assistant vorgeschrieben. 
Installation ```pip install -U pylint```.
- Prettier (Python Linter): Von Home Assistant empfohlen. 
Installatin ```pip install -U prettier```.
- MyPy (Python Linter): Von Home Assistant empfohlen. 
Installation ```pip install -U mypy```.
- Flake8 (Python Linter): Von Home Assistant empfohlen. 
Installation ```pip install -U flake8```.
- Bandit (Python Linter): Von Home Assistant empfohlen. 
Installation ```pip install -U bandit```.
- YAMLint (YAML Linter): Von Home Assistant empfohlen. 
Installation ```pip install -U yamllint```.
- Typos (Rechtschreibprüfung (nur englisch)): Von mir empfohlen. 
Installation folgt später.
- CodeSpell (Rechtschreibprüfung (nur englisch)): Von Home Assistant empfohlen. 
Installation ```pip install -U codespell```.
- PyTest (Überprüfung der Implementierung mit Test-Klassen / -Funktionen): 
Von Home Assistant empfohlen, von mir dringend empfohlen.<br/>
Installation: ```pip install -U pytest```.

#### Installation von Typos

Typos findest in den GitHub-Repositores von *crate-ci*. Der Aufwand es zu 
installieren ist zwar etwas höher als bei CodeSpell, dass von Home Assistant 
favorisiert wird, aber es ist nach meiner Erfahrung deutlich besser in der 
Erkennung (weniger falsch-negative Erkennungen) und ist deutlich besser zu 
konfigurieren. Ich habe mir fast die Finger gebrochen, um CodeSpell davon zu 
überzeugen, die deutschen Versionen meiner Texte zu ignorieren und mit Typos 
war es ein Klacks. Dort kannst du (änlich wie bei den .gitignore Dateien) 
*.ignore* - Dateien anlegen und relativ einfach eintragen, welche Dateien nicht 
überprüft werden sollen. Du braucht aus den [Releases][crate-ci] das passende 
binäre Archiv für dein Betriebssystem. Darin findest du eine Datei mit dem 
Namen ```typos```.  Die musst du in ein Verzeichnis kopieren, das sich im 
**$PATH** befindet (ich habe mich für .local/bin etschieden). Fertig!

##

[![vscode][vscode]][vscode]
### Konfiguration von Visual Studio Code

Zunächst brauchst du ein paar Erweiterungen, um die volle Unterstüzung der IDE 
für die Python Entwicklung zu erhalten. Dies sind:

- **Python** von Microsoft, 
- **Pylance** von Microsoft und ggf. 
- **Remote - Containers** von Microsoft, falls du deine Integration auf deinem 
Entwicklungs-Rechner testen möchtest. 

Nachdem du die Erweiterungen installiert hast, solltest du Visual Studio Code 
neu starten.

Anschließend musst du VS-Code sagen, wo dein zentrales VENV-Verzeichnis liegt. 
Dazu sucht du am Besten in den Einstellungen nach *venv*. Falls du nur ein 
zentrales VENV-Verzeichnis hast, kannst du es direkt bei *"Python > **Venv Path**"* 
eintragen. Solltest du mehrere haben, musst du dich dort für eines entscheiden 
(ich empfehle das zu nehmen, in dem sich dein virtuelle Environment für die 
Entwicklung deiner Integration befindent). Die weiteren zentralen 
VENV-Verzeichnisse kannst du bei *"Python > **Venv Folders**"* eintragen. 

Ich habe es bisher nicht geschafft VS-Code beizubringen, die verwendeten 
Erweiterungen und Tools aus dem virtuellen Environment zu verwenden, ausser 
wenn ich das Environment vorhor (z.B. in einem Shell Skript aktiviere). Falls 
du eine Lösung für dieses Problemchen kennt, wäre ich froh und dankbar, wenn du 
dein Wissen mit mir teilst. Im Moment werden die Tools deshalb über ein Shell 
Skript ```(script/run-in-env.sh)``` gestartet, das das richtige Environment vor 
der Ausführung des Tools aktiviert.

Wenn du nun eine .py-Datei öffnest oder anlegst, wird dich VS-Code fragen,
welche Python-Version für die Python-Entwicklung in diesem Projekt verwendet 
werden soll. Wähl bitte das virtuelle Environment, das du für die Entwicklung
deiner Integration angelegt hast. Falls VS-Code dich nicht von selbst "befragt", 
kannst du unten rechts in der Statuszeile über "Sprachmodus auswählen" die 
Auswahl des richtigen Python-Interpreters auch selbst starten.

Danach solltest du in den Einstellungen nach *black* suchen und unter 
*"Python > Formatting: **Provider**"* **black** auswählen, da Home Assistant 
die Code-Formatierung mit Black vorschreibt.

Ggf. solltest du dann noch Pylance (Microsofts Python Language Server), der 
für die Erkennung von Problemen und IntelliSense zuständig ist, an deine 
Bedürfnisse anpassen. Dann hast du es endlich geschafft.

Bleibt mir nur zu hoffen, das ich nichts Wichtiges vergessen habe und dir viel 
Spaß und Erfolg bei der Programmierung deiner Integration zu wünschen.

[license-badge]: images/license.de.svg
[license-url]: ../COPYRIGHT.de.md
[logo]: images/logo.svg
[project-url]: https://github.com/nixe64/The-Next-Generation

[version-badge]: images/version.svg
[version-url]: https://github.com/nixe64/Home-Assistant-Blueprint/releases

[ggshield]: images/gg-logo.svg
[ggshield-url]: https://www.gitguardian.com/
[gg-dash]: https://dashboard.gitguardian.com/
[python]: images/python-logo.svg
[python-url]: https://www.python.org/
[crate-ci]: https://github.com/crate-ci/typos/releases
[vscode]: images/vscode.svg