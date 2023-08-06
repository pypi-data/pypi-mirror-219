# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['afkode', 'afkode.commands', 'afkode.ios', 'afkode.macos']

package_data = \
{'': ['*'], 'afkode': ['prompts/debug/*', 'prompts/programflow/*']}

install_requires = \
['PyAudio>=0.2.13,<0.3.0',
 'PyYAML>=6.0,<7.0',
 'gTTS>=2.3.2,<3.0.0',
 'google-auth==2.22.0',
 'openai>=0.27.5,<0.28.0',
 'pydub>=0.25.1,<0.26.0',
 'requests>=2.23.0,<3.0.0',
 'requests_toolbelt>=1.0.0,<2.0.0',
 'types-requests>=2.31.0,<3.0.0',
 'urllib3==1.26.16']

extras_require = \
{'docs': ['m2r2>=0.3,<0.4',
          'sphinx>=6.2,<7.0',
          'sphinx-autodoc-typehints>=1.23,<2.0',
          'sphinx_rtd_theme>=1.2,<2.0'],
 'lint': ['black>=23.3,<24.0',
          'darglint>=1.8,<2.0',
          'flake8>=6.0,<7.0',
          'flake8-annotations>=3.0,<4.0',
          'flake8-bandit>=4.1,<5.0',
          'flake8-bugbear>=23.6,<24.0',
          'flake8-builtins>=2.1,<3.0',
          'flake8-docstrings>=1.7,<2.0',
          'mypy>=0.910,<0.911',
          'safety>=2.3,<3.0',
          'xdoctest>=1.1,<2.0',
          'types-PyYAML>=6.0,<7.0'],
 'tests': ['pytest>=6.2,<7.0',
           'pytest-cases>=3.6,<4.0',
           'pytest-cov>=3.0,<4.0']}

entry_points = \
{'console_scripts': ['afkode = afkode.run:start']}

setup_kwargs = {
    'name': 'afkode',
    'version': '0.4.4',
    'description': 'Personal voice command interface for iPhone on pythonista powered by Whisper and ChatGPT.',
    'long_description': '# AFKode - Speak it, Save it, AFKode it!\n\nAFKode allows users to interact with AI and file system using only voice, allowing you to work away from keyboard.\nWorks on iPhone with pythonista, or on MacOS.\nPowered by Whisper and ChatGPT.\n\nThis project was inspired by long walks on the beach while ruminating and organizing ones thoughts.\n\nUsers of this program should be comfortable using pythonista/python.\nYou are required to BYO OpenAI secret key in variable `OPENAI_KEY` using environment variables or within `afkcode/secrets.py`.\n\nKey features:\n\n- Detection of start/stop dictation for transcription\n- Uses ChatGPT create smart file naming for your notes\n\nInterfaces:\n\n* At home: Supports MacOS with base speakers/microphone or AirPods. May not work with other bluetooth headsets like Bose headphones.\n* Out and about: Supports Pythonista iOS with base speakers/microphones, or plugged in lightning wired heaphones. Bluetooth headsets like AirPods and Bose headphones currently not working.\n\n## Contents\n\n* [Instructions for users](#instructions-for-users)\n  * [Installation](#installation)\n  * [Usage documentation](#usage-documentation)\n  * [Bug reports](#bug-reports)\n* [Instructions for developers](#instructions-for-developers)\n  * [Poetry](#environment-1-poetry)\n  * [Testing with Nox](#testing-with-nox)\n  * [Code formatting with Pre-commit](#code-formatting-with-pre-commit)\n* [Contributors](#contributors)\n\n## Instructions for users\n\nThe following are the quick start instructions for using the project as an end-user.\n\nFollow the [Instructions for developers](#instructions-for-developers) to set up the virtual environment and dependency management.\n\n### Installation\n\nMacOS requirements:\n\n- Python 3.8\n- pyaudio\n- ffmpeg for mp3 text-to-speech, `brew install ffmpeg`\n\n```\nbrew install portaudio\n```\n\nNote: Instructions marked with %% are not functioning and are for demo purposes only.\n\nInstall the project using pip %%:\n\n```bash\npip install afkode\n```\n\nTo replicate the data transformations and model results, run the following commands from the project root.\nThese should be run from the `poetry shell`, or `conda` environment, or with the `poetry run` prefix.\n```bash\npython -m afkode.run\n```\n\n### Usage documentation\n\nThe user guides can be found on [github pages](https://ndjenkins85.github.io/afkode).\nThis includes overview of features, discussion of `afkode` framework, and API reference.\n\n### Bug reports\n\nPlease raise an [issue](https://github.com/ndjenkins85/afkode/issues) with `bug` label and I will look into it!\n\n## Instructions for developers\n\nThe following are the setup instructions for developers looking to improve this project.\nFor information on current contributors and guidelines see the [contributors](#contributors) section.\nFollow each step here and ensure tests are working.\n\n### Poetry\n\n[Poetry](https://python-poetry.org/docs/) handles virtual environment management, dev and optional extra libraries, library development, builds and publishing.\n\nCheck the poetry website for the latest instructions on how to install poetry.\nYou can use the following command on OS/linux to install poetry 1.1.9 used in this project.\n\n```bash\ncurl -sSL https://install.python-poetry.org | python - --version 1.1.9\n```\n\nIt is recommended to set virtual environment creation to within project using the following command.\nThis adds a `.venv` directory to project to handle cache and virtual environment.\n```bash\npoetry config virtualenvs.in-project true\n```\n\nYou can set up the virtual environment in the repo using the following command.\nMake sure that any other virtual environments (i.e. `conda deactivate`) are deactivated before running.\n\n```bash\npoetry install\n```\n\nTroubleshooting: You may need to point poetry to the correct python interpreter using the following command.\nIn another terminal and in conda, run `which python`.\n```bash\npoetry env use /path/to/python3\n```\n\nWhen the environment is correctly installed, you can enter the virtual environment using `poetry shell`. Library can be built using `poetry build`.\n\n### Testing with Nox\n\n[Nox](https://nox.thea.codes/en/stable/index.html) is a command-line tool that automates testing in multiple Python environments, similar to tox, Makefiles or scripts. Unlike tox, Nox uses a standard Python file for configuration.\n\nHere it is used for code quality, testing, and generating documentation.\n\nThe following command can be used to run mypy, lint, and tests.\nIt is recommended to run these before pushing code, as this is run with Github Actions.\nSome checks such as black are run more frequently with [pre-commit](#code-formatting-with-pre-commit).\n\n```bash\npoetry run nox\n```\n\nLocal Sphinx documentation can be generated with the following command.\nDocumentation publishing using Github Actions to Github pages is enabled by default.\n\n```bash\npoetry run nox -s docs\n```\n\nOther available commands include:\n\n```bash\npoetry run nox -rs coverage\n```\n\n### Code formatting with Pre-commit\n\n[Pre-commit](https://pre-commit.com/) is a framework for managing and maintaining multi-language pre-commit hooks.\n\nIt intercepts the `git commit` command to run checks of staged code before the commit is finalized.\nThe checks are specified in `.pre-commit-config.yaml`.\nChecks in use are quick, pragmatic, and apply automatic formatting checks.\nIf checks fail, it is usually only a matter of re-staging the files (`git add`) and attempting to commit again.\n\nThe aim is to provide a lightweight way to keep some code standards automatically in line with standards.\nThis does not replace the need to run nox tests, although pre-commits will satisfy some of the nox test checks.\n\nOn first time use of the repository, pre-commit will need to be installed locally.\nYou will need to be in the `poetry shell` or `conda` environment.\nRun the following command to perform a first time install.\n\n```bash\npre-commit install\n```\n\nThis will cache several code assets used in the checks.\n\nWhen you have new code to commit, pre-commit will kick in and check the code.\nAlternatively, you can run the following command to run for all files in repo.\n\n``` bash\npre-commit run --all-files\n```\n\n## Contributors\n\n* [Nick Jenkins](https://www.ndjenkins.com) - Data Scientist, API & Web dev, Team lead, Writer\n\nSee [CONTRIBUTING.md](CONTRIBUTING.md) in Github repo for specific instructions on contributing to project.\n\nUsage rights governed by [LICENSE](LICENSE)  in Github repo or page footer.\n',
    'author': 'Nick Jenkins',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.ndjenkins.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.9',
}


setup(**setup_kwargs)
