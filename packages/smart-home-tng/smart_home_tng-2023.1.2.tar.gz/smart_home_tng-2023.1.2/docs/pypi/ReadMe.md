# Smart Home - The Next Generation

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

### Installation

In order to use **Smart Home - The Next Generation**, you need Python 3.11.4
or later. Create a new virtual environment and use it with 

```
source <venv-path>/bin/activate
```
Afterwards you have to install `wheel`, wich is required to download and
install `smart-home-tng` and all requirements. Now you can install 
**Smart Home - The Next Generation** using this command line:
```
pip install --upgrade smart-home-tng
```
The same command line can be used to upgrade smart-home-tng to the newest version.

Now, you are ready to start `Smart Home - The Next Generation`.
```
usage: smart-home-tng [-h] [--version] [-c path_to_config_dir] [--safe-mode] [--debug] [--open-ui] [--skip-pip] [-v]
                      [--log-rotate-days LOG_ROTATE_DAYS] [--log-file LOG_FILE] [--log-no-color] [--script ...]
                      [--ignore-os-check]

Smart Home - The Next Generation: Observe, Control, Automate.

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -c path_to_config_dir, --config path_to_config_dir
                        Directory that contains the Smart Home - The Next Generation configuration
  --safe-mode           Start Smart Home - The Next Generation in safe mode
  --debug               Start Smart Home - The Next Generation in debug mode
  --open-ui             Open the webinterface in a browser
  --skip-pip            Skips pip install of required packages on startup
  -v, --verbose         Enable verbose logging to file.
  --log-rotate-days LOG_ROTATE_DAYS
                        Enables daily log rotation and keeps up to the specified days
  --log-file LOG_FILE   Log file to write to. If not set, CONFIG/smart_home_tng.log is used
  --log-no-color        Disable color logs
  --script ...          Run one of the embedded scripts
  --ignore-os-check     Skips validation of operating system

If restart is requested, exits with code 100
```
### Feature Requests / Bug Reports / Service Requests

If you have suggestions for new features, want to report a bug, or get stuck 
on a problem, feel free to open a new [issue][issues-url] on GitHub. But please,
check the existings issues if anyone else has already opened an issue for the 
same feature request or bug. Thank you.

### Contributing

Contributions are what make the open source community such a great place to 
learn, inspire, and create. I would be happy if you would like to contribute 
a new feature, bugfix or anything else to this project. Anything that makes 
this project better is welcome. Please visit the project on [GitHub][project-url]
to get more information read [Contributions][contribute-url] 
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
the `GNU General Public License v3`.

But “dear lovers” (as Brisko Schneider would have said), always remember:

**This is free software, without any warranty on functionality or 
usability for a specific purpose.**

[issues-url]: https://github.com/nixe64/the-next-generation/issues
[project-url]: https://github.com/nixe64/the-next-generation/
