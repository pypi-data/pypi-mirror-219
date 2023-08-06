# Smart Home - Die Nächste Generation

### Lebe lang und in Frieden

Hier kommst sie - die nächste Entwicklungstufe der 
Hausautomation. Sie basiert auf Home Assistent, dem zurecht beliebten zentralen
Steuerungssystem in einem Smart Home oder Smart House. 

Wie Home Assistent ist 
sie ebenfalls als kostenlose und quelloffene Software konzipiert, die in den 
wesentlichen Teilen in Python entwickelt wird und deren Hauptaugenmerk auf 
lokaler Steuerung und Privatspäre liegt. Da ich mich allerdings in der c / 
c++ / c# - Entwicklung mehr zuhause fühle, werden viele unterstützende 
Bibliotheken eher in c++ entwickelt werden. Aus dem gleichen Grund werde ich auch
das eher auf einer "Modulhierarchie" bestehende Grundgerüst auf eine Klassenhierarchie
umstellen (so gut es Python eben zulässt).

Dadurch sollte jedem, der sich mit Klassenhierarchien etwas auskennt aber auch 
"Einsteigern", relativ schnell klar werden, welche Klasse welche Aufgaben übernimmt, 
welche Teile der "Schnittstelle"  von allen benutzt werden dürfen und welche Teile 
nur innerhab der Klasse für die Implementierung der Funktionalität vorhanden sind.


### Installation

Für die Verwendung/Installation von **Smart Home - Die Nächste Generation** wird
Python 3.11.4 oder höher benötigt. Die Installation sollte in ein neues virtuelles
Python-Environment erfolgen. Nach dem Download und der Installation der benötigten
Bibliotheken kann es mit
```
smart-home-tng
```
gestartet werden. Mit 
```
smart-home-tng --help
```
erhälst du eine Übersicht der verfügbaren Parameter/Optionen der Kommandozeile.
Der Ordner mit der Konfiguration für **Smart Home - Die Nächste Generation** befindet
sich unter `~/.config/shc`, wenn er nicht über die Kommandozeile festgelegt wird.

### Danksagungen

Mein Dank gilt allen, die mein Vorhaben unterstützt haben oder noch unterstützen 
werden und die aktiv an der Realisierung mitwirken oder durch neue Sichtweisen 
und Vorschläge für Verbesserungen dazu beitragen oder bereits beigetragen haben, 
meine anfängliche Idee weiter zu verfeinern und abzurunden. Ebenfalls bedanken 
möchte ich mich bei allen, deren Vorarbeit ich für die Realisierung dieses 
Vorhabens verwenden darf. 

Besonders und ausdrücklich möchte ich allerdings meiner Freundin für Ihr 
Verständnis und Ihre Unterstützung danken, ohne die meine Vision nie 
Wirklichkeit wird (weil es oft darauf hinaus läuft, das ich bis spät in der 
Nacht und am Wochenende an der Umsetzung und Verfeinerung meiner Idee sitze 
und deshalb für gemeinsame Aktivitäten weniger Zeit übrig bleibt, als sie 
verdient hätte).

### Lizenz

Veröffentlicht zur freien Verwendung/Modifizierung gemäß den Bedingungen der 
`Allgemeinen Öffentlichen GNU-Lizenz v3`.

Aber "Liebe Liebenden" (wie es Brisko Schneider gesagt hätte), immer daran denken:

**Dies ist freie Software, ohne irgendeine Garantie auf Funktionalität oder 
Verwendbarkeit für einen bestimmten Zweck.** 


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[logo]: images/logo.svg
[project-url]: https://github.com/nixe64/The-Next-Generation/

[license-badge]: images/license.de.svg
[license-url]: ../COPYRIGHT.de.md

[version-badge]: images/version.svg
[version-url]: https://github.com/nixe64/Home-Assistant-Blueprint/releases

[issues-url]: https://github.com/nixe64/Home-Assistant-Blueprint/issues
[bugs-badge]: https://img.shields.io/github/issues/nixe64/Home-Assistant-Blueprint/bug.svg?label=Fehlerberichte&color=informational
[bugs-url]: https://github.com/nixe64/Home-Assistant-Blueprint/issues?utf8=✓&q=is%3Aissue+is%3Aopen+label%3Abug

[contribute-url]: CONTRIBUTING.md
[coc-url]: CODE_OF_CONDUCT.md

[template-btn]: images/template-btn.svg

[support-url]: Support.de.md
[development-url]: Development.de.md
