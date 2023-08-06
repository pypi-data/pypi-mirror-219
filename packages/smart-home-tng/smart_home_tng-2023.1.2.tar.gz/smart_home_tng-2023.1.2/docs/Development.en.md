<a href="Development.en.md"><img src="images/en.svg" valign="top" align="right"/></a>
<a href="Development.de.md"><img src="images/de.svg" valign="top" align="right"/></a>
<!--[![Version][version-badge]][version-url]-->
[![License][license-badge]][license-url]
<!--
[![Bugs][bugs-badge]][bugs-url]
-->

[![Logo][logo]][project-url]

### Setting up the development environment


[![ggshield]][ggshield-url]
#### Set up GitGuardian Shield (if desired).

To use the checks of [GitGuardian][ggshield-url], you first need a free 
account.  you first need a free account. The link in the previous sentence will
take you directly to the start page and then use the ``Start for free`` button. 
After you have set up your account, you can use ``API`` / 
``Personal access tokens`` to generate the required personal access tokens. 
After pressing ``Create token`` give your token a name, so that you can later 
recognize what you used it for, and then make the following settings following 
settings:

- ```Expires:``` For the token that you want to use in your development 
environment I recommend an expiration period of 6 months to max. 1 year. For 
the Token you want to use on GitHub, I recommend 6 months max.
- ```Scope:``` Please select ```scan``` only.

After pressing the ``Create token`` button, your new access token will be 
displayed (somewhat inconspicuous at the top, highlighted in green). Copy it 
into a file or into your password manager. You will never see it again. After 
you have created the two tokens, they "only" have to be deposited in the 
correct places to finally activate GitGuardian as GitHub App. 


##### Integration of GitGuardian in the pre-commit checks

The actual integration of GitGuardian into the pre-commit checks this 
Blueprint has already done for you. However, you still need to store your 
access token in a suitable place and prepare the virtual Python environment 
and install the GitGuardian Shield. The details for the installation can be 
found in the section **Preparation of the virtual Python environment**. Here, 
let's stay at the appropriate places for your access tokens.

You can either store your token in the ``GITGUARDIAN_API_KEY`` environment 
variable (e.g. by exporting it in ``~/.bashrc``) or you can put it into the 
configuration file of GitGuardian ``~/.gitguardian.yml`` (my preferred 
variant). With the second variant you have the advantage that you can configure
GitGuardian to your personal needs in the same place (see GitGuardian (see 
GitGuardian documentation) and, even though it is not in the documentation you 
can also store **your access token** here. (I love it when the docus hide the 
most important stuff.) Your configuration file could then look something like 
this:

```
api-key: <your just created personal access token>
...
# other personal settings
```

##### Integration of GitGuardian into GitHub workflows

First of all, you should prepare your repositories already. For this you have 
to go to the ``Settings`` for each repository. There you will find under 
``Secrets`` the item ``Actions``. Use the ```New repository secret``` button. 
There you can enter your second personal access token. At ``Name`` you have to 
enter the name **GITGUARDIAN_API_KEY** and for ``Value`` your token. Done!

Finally you have to activate GitGuardian as a GitHub App (you can find it under
your GitHub account settings / Applications). However, the process must be 
**initiated on GitGuardian**. To do this, go to [Dashboard][gg-dash] and click on 
``INTEGRATIONS``. Under *VCS Integrations* you will find GitHub and there you 
just need to and there you have to press the ``Install`` button and make the 
settings. With this you have done it.

##

[![python][python]][python-url]
#### Preparation of the Python virtual environment

So that in Visual Studio Code (my favorite IDE) the switch between different 
virtual python environments works, all VENVs must be located under a "central" 
directory. I have chosen ``~/.venv``. If you prefer a different location, you 
will need to modify the script file ```script/run-in-env``` to suit your 
configuration. About halfway through the script, you will find a for loop 
```for venv in venv .venv . **~/.venv**; do``. There you have to enter your 
central VENV directory instead of the highlighted central VENV directory in my 
configuration.

If you don't have a central directory yet, where you have "collected" all 
VENVs, please create a new one. You need write permissions in this folder, so 
it can be somewhere in your home directory.

Since Home Assistant is currently developed with Python 3.9, please make sure 
you have a suitable Python interpreter installed. You can check it with 
```python3.9 --version```. If Python shows a version number (in my case Python 
3.9.5) you can continue.

Please change to your newly created / existing central VENV directory. There 
enter ``python3.9 -m venv 3.9``. This will create a new virtual directory for 
your development of a Home Assistant integration. Tip: I defined an alias for 
```source ~/.venv/3.9/bin/activate``` in ~/.bash_aliases, so I only need to 
call *p3.9* when I want to work with this virtual environment.

If you want to test your integration directly on your machine (e.g. in a Docker 
container), then I recommend you to create a second virtual environment for 
this purpose, as Home Assistant pins all the libraries it uses to a fixed 
version and thus updates for many of the Libraries you install with pip will 
be undone by Home Assistant the next time you start it. I have my second 
virtual Python virtual environment ha-dev, but again you can let your 
imagination run wild, and take a different name if desired.

After the virtual environment(s) exist, you may need to modify the 
```.python-version``` file. There you enter the name of the virtual environment 
you want to use for the development of your integration.

##### Installing the required components for pre-commit checks

Since Python is not compiled, syntactical errors are not detected until the 
code is executed. In order to be already informed about actual or at least 
potential errors during the development, we still need some tools. Some of 
them are required by Home Assistant or by the Home Assistant Community (HACS), 
some I "only" thought to be useful and have included them.

Before you start installing the components, you have to activate your virtual 
environment with ```source ~/.venv/3.9/bin/activate`` or your corresponding 
alias. You will probably already know that the prompt will change and you will 
see the activated virtual environment in brackets in front of your name.

I would like to start with my first recommendation of the ReadMe: The 
installation of GitGuardian Shield. If you decided not to check with GGShield, 
you can skip this step.

To install GitGuardian Shield, please type the following command in a terminal:

```
pip install -U ggshield
```

For the remaining components, I will indicate whether they are suggested by 
Home Assistant or HACS (i.e. optional) or whether they are required so that 
you can decide for yourself which checks you would like to omit or exchange 
for a better variant of the check from your point of view.

- pre-commit (Runs all tests before allowing a commit). From Home Assistant 
prescribed:<br/>
Installation: ```pip install -U pre-commit```.
- Black (Source Formatter): Required by Home Assistant and HACS. 
Installation: ```pip install -U black```.
- ISort (Sorting of Imports): Required by Home Assistant and HACS. 
Installation ```pip install -U isort```.
- PyLint (Python Linter): Required by Home Assistant. 
Installation ```pip install -U pylint```.
- Prettier (Python Linter): Recommended by Home Assistant. 
Installation ```pip install -U prettier```.
- MyPy (Python Linter): Recommended by Home Assistant. 
Installation ```pip install -U mypy```.
- Flake8 (Python Linter): Recommended by Home Assistant. 
Installation ```pip install -U flake8```.
- Bandit (Python Linter): Recommended by Home Assistant. 
Installation ```pip install -U bandit```.
- YAMLint (YAML Linter): Recommended by Home Assistant. 
Installation ```pip install -U yamllint```.
- Typos (spell checker (English only)): Recommended by me. 
Installation follows later.
- CodeSpell (spell checker (English only)): Recommended by Home Assistant. 
Installation ```pip install -U codespell```.
- PyTest (check implementation with test classes / functions): Recommended by 
Home Assistant, strongly recommended by me.<br/>
Installation: ```pip install -Uwiekest```.

##### Installing Typos

Typos can be found in the GitHub repositories of *crate-ci*. The effort to 
install Typos is a bit higher than CodeSpell, which is favored by Home 
Assistant, but in my experience it is much better at detection (fewer 
false-negative detections) and is significantly better to configure. I almost 
broke my fingers trying to convince CodeSpell to ignore the German versions of 
my "ReadMes" Ignore and with Typos it was a blast. There you can (similar to 
the .gitignore files) create *.ignore* files and relative simply enter which 
files should not be checked. You need the appropriate binary archive for your 
operating system from the [releases][crate-ci]. In it you will find a file 
named ```typos```.  You have to copy it into a directory that is in the **$PATH** 
(I chose .local/bin). Ready!

##

[![vscode][vscode]][vscode]
#### Configuring Visual Studio Code

First, you need a few extensions to get the full support of the IDE for Python 
development. These are:

- **Python** from Microsoft,
- **Pylance** from Microsoft and possibly 
- **Remote Containers** from Microsoft, if you want to test on your development 
computer. 

After you have installed the extensions, you should restart Visual Studio Code.

Then you have to tell VS Code where your central VENV directory is located. The 
best way to do this is to search for *venv* in the settings. If you have only 
one central VENV directory, you can enter it directly at 
*”Python > **Venv Path**”*. If you have more than one, you must decide for one 
thing there (I recommend taking the one where your virtual environment for the 
development of your integration is located). You can enter the other central 
ENV directories at *”Python > **Venv Folders**”*. 

I haven’t made it yet to "teach" VS Code to use the extensions and tools from 
the virtual environment, unless I activate the environment beforehand (e.g. in 
a shell script). If you know a solution to this little problem, I’d be happy 
and grateful if you could share your knowledge with me. At the moment, 
therefore, the tools are started via a shell script ```(script/run-in-env.sh)``` 
that activates the correct environment before executing the tool.

If you now open or create a .py file, VS code will ask you which Python version 
for Python development in this project should be used. Please select the 
virtual environment you have created for the development of your integration. 
If VS Code does not “ask” you by itself, you can select the right one in the 
bottom right of the status line via “Select language mode”.

Then you should search for *black* in the settings and select 
*”Python > Formatting: **Provider**”* **black**, because Home Assistant 
requires the code formatting with Black.

If necessary, you should also adapt Pylance (Microsoft’s Python Language Server)
to your needs, which is responsible for troubleshooting and IntelliSense. Then 
you finally did it.

I hope that I have not forgotten anything important and wish you a lot of fun 
and success in programming your Integration.

<!----------------------------------------------------------------------------->

[license-badge]: images/license.de.svg
[license-url]: ../COPYRIGHT.de.md
[logo]: images/logo.svg
[project-url]: https://github.com/nixe64/The-Next-Generation

[version-badge]: images/version.svg
[version-url]: https://github.com/nixe64/The-Next-Generation/releases

[ggshield]: images/gg-logo.svg
[ggshield-url]: https://www.gitguardian.com/
[gg-dash]: https://dashboard.gitguardian.com/
[python]: images/python-logo.svg
[python-url]: https://www.python.org/
[crate-ci]: https://github.com/crate-ci/typos/releases
[vscode]: images/vscode.svg