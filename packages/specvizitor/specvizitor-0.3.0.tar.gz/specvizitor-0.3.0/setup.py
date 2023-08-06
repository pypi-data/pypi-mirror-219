# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['specvizitor',
 'specvizitor.config',
 'specvizitor.io',
 'specvizitor.plugins',
 'specvizitor.utils',
 'specvizitor.widgets']

package_data = \
{'': ['*'],
 'specvizitor': ['data/icons/dark/*', 'data/icons/light/*', 'data/presets/*']}

install_requires = \
['astropy>=5.2.1,<6.0.0',
 'dacite>=1.8.0,<2.0.0',
 'dictdiffer>=0.9.0,<0.10.0',
 'pandas>=1.5.3,<2.0.0',
 'pgcolorbar>=1.1.3,<2.0.0',
 'pillow>=9.4.0,<10.0.0',
 'platformdirs>=3.0.0,<4.0.0',
 'pyqt5>=5.15.9,<6.0.0',
 'pyqtdarktheme>=2.1.0,<3.0.0',
 'pyqtgraph>=0.13.1,<0.14.0',
 'qtpy>=2.3.0,<3.0.0',
 'scipy>=1.10.1,<2.0.0',
 'specutils>=1.9.1,<2.0.0']

entry_points = \
{'console_scripts': ['specvizitor = specvizitor.gui:main']}

setup_kwargs = {
    'name': 'specvizitor',
    'version': '0.3.0',
    'description': 'Python GUI application for a visual inspection of astronomical spectroscopic data',
    'long_description': '[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)\n\nSpecvizitor is a Python GUI application for a visual inspection of astronomical spectroscopic data. The main goal is to provide a flexible tool for classifying **large**, **homogeneous** samples of galaxies observed with spectroscopy, which is a typical case for blind spectroscopic surveys. Originally developed for the JWST Cycle 1 program [FRESCO](https://jwst-fresco.astro.unige.ch), this software can be easily adapted for a variety of spectroscopic data sets represented in standard data formats used in the astronomy community (FITS, ASCII, etc.).\n\n![Specvizitor GUI](https://github.com/ivkram/specvizitor/blob/main/docs/screenshots/specvizitor_gui.png?raw=true "Specvizitor GUI")\n\n## Installation\n\n### Installing `specvizitor` using pip\n\nSet up a local environment (Python **3.10+**) and run\n\n```shell\n$ pip install specvizitor\n```\n\n### Installing `specvizitor` from source\n\n1. Clone the public repository:\n\n    ```shell\n    $ git clone https://github.com/ivkram/specvizitor\n    $ cd specvizitor\n    ```\n\n2. Set up a local environment (Python **3.10+**) and run\n\n    ```shell\n    $ pip install -e .\n    ```\n\n## Starting `specvizitor`\n    \nTo start `specvizitor`, activate the local environment and run this command in your terminal:\n\n```shell\n$ specvizitor\n```\n\n## Configuring `specvizitor`\n\nThe basic settings such as the path to the catalogue/data directory are available in `Tools > Settings`. For more advanced settings, open the directory indicated in the bottom of the `Settings` widget ("Advanced settings"). Its location is platform-specific and determined using the [platformdirs](https://pypi.org/project/platformdirs/) package. The directory should contain the following YAML files: `specvizitor.yml` (the general GUI settings), `lines.yml` (the list of spectral lines displayed along with a spectrum) and `docks.yml` (the configuration of the data viewer). Several examples of changing these files for your needs are given below, but note that in the future, `specvizitor` will be fully configurable from the GUI.\n\n### Adding spectral lines\n\nOpen `lines.yml` and add an entry with the name of a spectral line and its rest wavelength to `list`, e.g.:\n\n```yaml\nlist:\n  # ...\n  PaG: 10938.086\n```\n\nBy default, all wavelengths are represented in angstroms, which is determined by the `wave_unit` parameter in the same file.\n\n### Configuring the data viewer\n\nThe content of the data viewer is described in `docks.yml`. There are three types of data that can be displayed in the data viewer: `images`, `plots` and `spectra`. \n\n## Troubleshooting\n\nTo reset `specvizitor` to its initial state, run the script with the `--purge` option:\n\n```shell\n$ specvizitor --purge\n```\n\n## License\n\n`specvizitor` is licensed under a 3-clause BSD style license - see the [LICENSE.txt](https://github.com/ivkram/specvizitor/blob/main/LICENSE.txt) file.\n',
    'author': 'Ivan Kramarenko',
    'author_email': 'im.kramarenko@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ivkram/specvizitor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
