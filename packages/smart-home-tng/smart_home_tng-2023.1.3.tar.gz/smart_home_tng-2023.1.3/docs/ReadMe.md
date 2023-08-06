<a href="ReadMe.en.md"><img src="images/en.svg" valign="top" align="right"/></a>
<a href="ReadMe.md"><img src="images/de.svg" valign="top" align="right"/></a>
<!--[![Version][version-badge]][version-url]-->
[![License][license-badge]][license-url]
<!--
[![Bugs][bugs-badge]][bugs-url]
-->

[![Logo][logo]][project-url]

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

Dadurch solle jedem, der sich mit Klassenhierarchien etwas auskennt aber auch 
"Einsteigern", relativ schnell klar werden, welche Klasse welche Aufgaben übernimmt, 
welche Teile der "Schnittstelle"  von allen benutzt werden dürfen und welche Teile 
nur innerhab der Klasse für die Implementierung der Funktionalität vorhanden sind.

Leider unterstützt Python die Verwendung von 
(Achtung, C++ - Code) ```private``` oder ```protected``` in Klassen nicht,
so das ich "nur" darauf vertrauen kann, das die nicht öffentlichen Teile der 
Implementierung, von denen, die dieses Projekt für sinnvoll und interessant
halten, als nicht öffentliche Teile der Implementierung respektiert werden.
Wie heißt es doch im Handwerk so treffend: Nicht das Werkzeug macht den 
Handwerker aus, sondern ein guter Handwerker erzielt mit jedem Werkzeug
das gewünschte Ergebnis. Wobei selbstverständlich das beste Ergebnis nur
zustande kommt, wenn dem guten Handwerker auch das beste Werkzeug zur 
Verfügung steht (also in diesem speziellen Fall, die Lieblingssprache). 
Aber die vollständige Umsetzung in c++ würde den Kreis derjenigen, die
das Projekt interessant und einsetzbar halten zu sehr einschränken.
Python wurde aus gutem Grund für die Entwicklung von Home Assistant
verwendet und daran möchte ich auch nichts ändern.

### Warum ein "neues Home Assistent", wenn das Existierende so gut ist?

Nun, auf den ersten Blick mag es so aussehen, als könnte/müsste man mit Home 
Assistant wunschlos glücklich sein. Tolle Oberfläche, sehr aktive Community, 
sehr umfassende Unterstützung von smarten Geräten, ... Was will man mehr?

Leider habe ich einen zweiten Blick (in den Quellcode) riskieren müssen, da ich
bei der Entwicklung einer neuen Integration für Home Assistant (mein *"Jarvis für Zuhause"*)
gescheitert bin! Home Assistant konnte aufgrund zirkulärer Imports nicht
von "Jarvis" importiert werden. Mein Bug-Report an Home Assistant verlief
im Sande. Ich konnte meine "Entwicklungsversion" von Home Assistant immerhin
so weit patchen, dass die von mir benötigten Teile "ohne meckern" importiert
und "Jarvis" so mit pyTest - Tests geprüft werden konnte.

Der Versuch meine gewonnenen Erkenntnisse bei der Home Assistant Community
"an den Mann" zu bringen und damit das Projekt (wenn auch nur ein wenig)
besser zu machen war genauso willkommen, wie eine Schmeissfliege auf der 
Frühstücksmarmelade (vermutlich verdient Nabu Casa an der 
**"Home Assistant Cloud"** bereits so gut, dass der
Open-Source-Gedanke nur noch zu Werbezwecken propagiert, aber nicht
mehr Ernst genommen wird.) Da ich nicht das 5. Rad am Wagen sein will,
bleibt mir also nur meine Vision eines zuverlässigen zentralen 
Steuerungssystems selbst zu realisiern und zu hoffen, das ein
paar Gleichgesinnte meinen Ansatz für interessant genug halten, um
das Projekt durch ihre Mitwirkung voran zu bringen.

### Verbesserungsvorschläge / Fehlerberichte / Serviceanfragen

Wenn du Vorschläge für neue Features hast, einen Fehler melden möchtest oder bei 
einem Problem nicht weiter kommst, schau bitte als Erstes bei 
[Unterstützung und Wartung][support-url] nach. Dort wird ausführlich erläutert, 
wie und wo du dein Anliegen vorbringen kannst.

### Mitwirkung

Mitwirkungen machen die Open-Source-Community zu einem so großartigen Ort zum 
Lernen, Inspirieren und Schaffen. Ich würde mich freuen, wenn du ein neues 
Feature, einen Bugfix oder irgendetwas anderes zu diesem Projekt beitragen 
möchtest. Es ist alles willkommen, daß dieses Projekt voran bringt. Aber bitte 
lies zuerst [Mitwirkung][contribute-url] an diesem Projekt und den 
[Verhaltenskodex][coc-url] für Mitwirkende, **bevor** du mit dem Programmieren 
beginnst.

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
[Allgemeinen Öffentlichen GNU-Lizenz v3][license-url].

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
