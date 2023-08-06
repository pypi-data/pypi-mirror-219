<a href="ReadMe.en.md"><img src="images/en.svg" valign="top" align="right"/></a>
<a href="ReadMe.md"><img src="images/de.svg" valign="top" align="right"/></a>
<!--[![Version][version-badge]][version-url]-->
[![License][license-badge]][license-url]
<!--
[![Bugs][bugs-badge]][bugs-url]
-->

[![Logo][logo]][project-url]

### Live Long And Prosper

Here it comes - the next stage in the development of home automation. It is 
based on Home Assistant, the popular central control system in a smart home
or smart house. 

Like Home Assistant it is also designed as a free and open-source 
software, which is developed in Python, with a focus on local control 
and privacy. However, since I am more familiar with c / 
c++ / c# - development, many supporting libraries will rather be 
developed in C++. For the same reason I will also transform the more 
"module hierarchy" based framework to a class hierarchy (as well as Python allows it).

This should help everyone who knows something about class hierarchies, but also 
"beginners", to understand relatively fast, which class takes over which tasks, 
which parts of the "interface" may be used by all and which parts may only be used 
within the class for implementation. 

Unfortunately Python doesn't support the use of 
(attention, C++ - Code) ``private`` or ``protected`` in classes,
so that I can "only" trust that the non-public parts of the implementation are 
respected as private, by those who find this project useful and interesting.

As it is so aptly said in the trade: It is not the tool that makes the 
craftsman, but a good craftsman achieves the desired result with every tool.
Of course, the best result can only be achieved if the good craftsman has 
the best tool available (in this (in this special case, the favorite language). 
But the complete implementation in c++ would limit the circle of those, who would
find the project interesting and usable too much.
Python was used for good reason for the development of Home Assistant
and I don't want to change that.

### Why a “new home assistant” if what exists is so good?

Well, at first glance it might look like you could/should be perfectly
happy with Home Assistant. Great interface, very active community, 
very comprehensive support of smart devices, ... What more do you want?

Unfortunately I had to risk a second look (in the source code) because I
failed in developing a new integration for Home Assistant (my *”Jarvis”*).
Due to circular imports Home Assistant couldn't be imported by “Jarvis", 
which is neccesarry to test the new integration with pytest.
My bug report to Home Assistant ran into "Nirvana", the issue is still 
untouched. 
I was able to patch my “development version” of Home Assistant after all
so far that the parts I needed are imported “without complaining”
and “Jarvis” could be tested with pytest.

Trying to share my gained insights with the Home Assistant Community
and make the project (even if only a little) better was just as welcome 
as a fly fly on the breakfast jam (probably Nabu Casa earns already too much 
money by hosting the **”Home Assistant Cloud”** that the Open-Source thought 
is only propagated for advertising purposes). 
I don’t want to be the fifth wheel at the car, so all I have left is to 
realize my vision of a reliable centralized control system myself and 
to hope that a few like-minded people consider my approach interesting 
enough to advance the project through their participation.

### Feature Requests / Bug Reports / Service Requests

If you have suggestions for new features, want to report a bug, or get stuck 
on a problem, please first check [Support and Servicing][support-url]. It 
explains in detail how and where you can make your case.

### Contributing

Contributions are what make the open source community such a great place to 
learn, inspire, and create. I would be happy if you would like to contribute 
a new feature, bugfix or anything else to this project. Anything that makes 
this project better is welcome. But please read [Contributions][contribute-url] 
to this project and the [Code of Conduct][coc-url] for contributors first 
**before** you start coding.

### Acknowledgements

My thanks go to all those who have supported or will continue to support my 
project and who are actively involved in its realization or who have 
contributed or already contributed to the refinement and completion of my 
initial idea with a new point of view and suggestions for improvements. I would 
also like to thank everyone whose preparatory work I have been able to use for 
the realization of this project. 

However, I would like to express my gratitude to my friend for her understanding 
and support, without which my vision will never become a reality (because it 
often amounts to me sitting late at night and at weekends on the implementation 
and refinement of my idea, leaving less time for joint activities than she would 
have deserved).

### License

Distributed for free use/modification under the terms of
the [GNU General Public License v3][license-url].

But “dear lovers” (as Brisko Schneider would have said), always remember:

**This is free software, without any warranty on functionality or 
usability for a specific purpose.**

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[logo]: images/logo.svg
[project-url]: https://github.com/nixe64/The-Next-Generation/

[license-badge]: images/license.en.svg
[license-url]: ../COPYRIGHT.en.md

[version-badge]: images/version.svg
[version-url]: https://github.com/nixe64/The-Next-Generation/releases

[issues-url]: https://github.com/nixe64/The-Next-Generation/issues
[bugs-badge]: https://img.shields.io/github/issues/nixe64/the-next-generation/bug.svg?label=Fehlerberichte&color=informational
[bugs-url]: https://github.com/nixe64/the-next-generation/issues?utf8=✓&q=is%3Aissue+is%3Aopen+label%3Abug

[contribute-url]: CONTRIBUTING.en.md
[coc-url]: CODE_OF_CONDUCT.en.md

[template-btn]: images/template-btn.svg

[support-url]: Support.en.md
[development-url]: Development.en.md
