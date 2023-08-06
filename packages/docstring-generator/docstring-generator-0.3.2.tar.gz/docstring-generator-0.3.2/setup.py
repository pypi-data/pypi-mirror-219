# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docstring_generator']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'docstring-generator-ext>=0.0.0,<0.1.0']

entry_points = \
{'console_scripts': ['gendocs_new = docstring_generator.new_gen_docs:main']}

setup_kwargs = {
    'name': 'docstring-generator',
    'version': '0.3.2',
    'description': 'Auto generate docstring from type-hints.',
    'long_description': '#### Versioning\n- For the versions available, see the tags on this repository.\n\n### Authors\n- Felix Eisenmenger\n\n### License\n- This project is licensed under the MIT License - see the LICENSE.md file for details\n',
    'author': 'FelixTheC',
    'author_email': 'felixeisenmenger@gmx.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/FelixTheC/docstring_generator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<=3.11',
}


setup(**setup_kwargs)
