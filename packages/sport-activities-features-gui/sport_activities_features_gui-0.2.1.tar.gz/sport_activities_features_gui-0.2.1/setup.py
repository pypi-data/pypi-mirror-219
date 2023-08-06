# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sport_activities_features_gui',
 'sport_activities_features_gui.logic',
 'sport_activities_features_gui.models',
 'sport_activities_features_gui.widgets',
 'sport_activities_features_gui.windows']

package_data = \
{'': ['*'], 'sport_activities_features_gui': ['media/*']}

install_requires = \
['PyQt6>=6.5.1,<7.0.0',
 'QtAwesome>=1.2.1,<2.0.0',
 'sip>=6.7.9,<7.0.0',
 'sport-activities-features>=0.3.13,<0.4.0']

entry_points = \
{'console_scripts': ['sport-activities-features-gui = '
                     'sport_activities_features_gui.main:main']}

setup_kwargs = {
    'name': 'sport-activities-features-gui',
    'version': '0.2.1',
    'description': 'GUI for sport-activities-features package',
    'long_description': '<p align="center">\n  <img width="200" src="https://raw.githubusercontent.com/firefly-cpp/sport-activities-features-gui/main/.github/logo/sport_activities.png">\n</p>\n\n---\n\n# sport-activities-features-gui\n\nA simple GUI application that uses the library sports-activities-features to import sports activity files (TCX) and makes it easy to view and transform the data in a GUI environment.\n\n## Features\n- Improved bulk importing of tcx files\n- Exporting data to different formats\n- Graphing data\n- Data transformations\n- Calendar view of active days\n- Individual user profiles\n\n## Screenshots\n<p float="left">\n  <img src="https://github.com/otiv33/sport-activities-features-gui/blob/main/screenshots/Screenshot_1.jpg?raw=true" alt="Profiles window" width="200"/>\n  <img src="https://github.com/otiv33/sport-activities-features-gui/blob/main/screenshots/Screenshot_2.jpg?raw=true" alt="Import tab" width="350"/>\n  <img src="https://github.com/otiv33/sport-activities-features-gui/blob/main/screenshots/Screenshot_3.jpg?raw=true" alt="Graphs tab" width="350"/>\n  <img src="https://github.com/otiv33/sport-activities-features-gui/blob/main/screenshots/Screenshot_4.jpg?raw=true" alt="Calendar tab" width="350"/>\n  <img src="https://github.com/otiv33/sport-activities-features-gui/blob/main/screenshots/Screenshot_5.jpg?raw=true" alt="Transformations tab" width="350"/>\n</p>\n\n## Installation\n0. Prerequisites\n    - [Python 3.10](https://www.python.org/downloads/)\n    - [Poetry](https://python-poetry.org/docs/#installation)\n1. Clone [this](https://github.com/firefly-cpp/sport-activities-features-gui) repository from GitHub.\n2. Create a virtual environment and install the dependencies using poetry:\n    ```bash\n    poetry install\n    ```\n3. Run the main.py file\n   1. Script path: `<project_folder>/sport-activities-features-gui/main.py`\n   2. Working directory: `<project_folder>/sport-activities-features-gui/`\n\n## License\n\nThis package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.\n\n## Disclaimer\n\nThis framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!\n',
    'author': 'otiv33',
    'author_email': 'vito.abeln@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/firefly-cpp/sport-activities-features-gui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
