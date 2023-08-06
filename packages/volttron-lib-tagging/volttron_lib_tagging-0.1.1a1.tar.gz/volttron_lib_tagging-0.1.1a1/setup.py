# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'tagging': 'tests/tagging',
 'tagging.testing': 'tests/tagging/testing'}

packages = \
['tagging', 'tagging.base', 'tagging.testing']

package_data = \
{'': ['*'], 'tagging': ['data_model/*']}

install_requires = \
['ply>=3.11,<4.0', 'volttron>=10.0.3a9,<11.0']

setup_kwargs = {
    'name': 'volttron-lib-tagging',
    'version': '0.1.1a1',
    'description': 'A base tagging agent api with extension points for using with the VOLTTRON platform. This base agent works with Haystack 3 tags',
    'long_description': "[![Eclipse VOLTTRON™](https://img.shields.io/badge/Eclips%20VOLTTRON--red.svg)](https://eclipse-volttron.readthedocs.io/en/latest/)\n![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)\n![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)\n[![Run Pytests](https://github.com/eclipse-volttron/volttron-lib-tagging/actions/workflows/run-tests.yml/badge.svg)](https://github.com/eclipse-volttron/volttron-lib-tagging/actions/workflows/run-tests.yml)\n[![pypi version](https://img.shields.io/pypi/v/volttron-lib-tagging.svg)](https://pypi.org/project/volttron-lib-tagging/)\n\nVOLTTRON base tagging library that provide common tagging api for users to associate haystack based tags and values to \ntopic names and topic name prefixes. Implementing agents can persist tags in specific data store. \n\nTags used by this library have to be pre-defined in a resource file at volttron_data/tagging_resources. The\nlibrary validates against this predefined list of tags every time user add tags to topics. Tags can be added to one \ntopic at a time or multiple topics by using a topic name pattern(regular expression). This library uses tags from \n[project haystack](https://project-haystack.org/) and adds a few custom tags for campus and VOLTTRON point name.\n\nEach tag has an associated value and users can query for topic names based tags and its values using a simplified \nsql-like query string. Queries can specify tag names with values or tags without values for boolean tags(markers). \nQueries can combine multiple conditions with keyword AND, and OR, and use the keyword NOT to negate a conditions.\n\n## Requirements\n\n - Python >= 3.10\n\n## Installation\n\nThis library can be installed using ```pip install volttron-lib-tagging```. However, this is not necessary. Any \nimplementing tagging agent that uses this library will automatically install it as part of its installation. \nFor example,  installing [SQLiteTaggingAgent](https://github.com/eclipse-volttron/volttron-sqlite-tagging) will \nautomatically install volttron-lib-tagging into the same python environment\n\n## Dependencies and Limitations\n\n1. When adding tags to topics this library calls the platform.historian's (or a configured historian's) \n   get_topic_list and hence requires a platform.historian or configured historian to be running, but it doesn't require \n   the historian to use sqlite3 or any specific database. It requires historian to be running only for using this \n   api (add_tags) and does not require historian to be running for any other api. \n2. Resource files that provides the list of valid tags is mandatory and should be in \n   data_model/tags.csv\n3. Tagging library only provides APIs to query for topic names based on tags. Once the list of topic names is retrieved, \n   users should use the historian APIs to get the data corresponding to those topics. \n4. Current version of tagging library does not support versioning of tag/values. When tags values are set it will \n   overwrite any existing tag entries in the database\n\n## Development\n\nPlease see the following for contributing guidelines [contributing](https://github.com/eclipse-volttron/volttron-core/blob/develop/CONTRIBUTING.md).\n\nPlease see the following helpful guide about [developing modular VOLTTRON agents](https://github.com/eclipse-volttron/volttron-core/blob/develop/DEVELOPING_ON_MODULAR.md)\n\n# Disclaimer Notice\n\nThis material was prepared as an account of work sponsored by an agency of the\nUnited States Government.  Neither the United States Government nor the United\nStates Department of Energy, nor Battelle, nor any of their employees, nor any\njurisdiction or organization that has cooperated in the development of these\nmaterials, makes any warranty, express or implied, or assumes any legal\nliability or responsibility for the accuracy, completeness, or usefulness or any\ninformation, apparatus, product, software, or process disclosed, or represents\nthat its use would not infringe privately owned rights.\n\nReference herein to any specific commercial product, process, or service by\ntrade name, trademark, manufacturer, or otherwise does not necessarily\nconstitute or imply its endorsement, recommendation, or favoring by the United\nStates Government or any agency thereof, or Battelle Memorial Institute. The\nviews and opinions of authors expressed herein do not necessarily state or\nreflect those of the United States Government or any agency thereof.\n",
    'author': 'VOLTTRON Team',
    'author_email': 'volttron@pnnl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eclipse-volttron/volttron-lib-tagging',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
