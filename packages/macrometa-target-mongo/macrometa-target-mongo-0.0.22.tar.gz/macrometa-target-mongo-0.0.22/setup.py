# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['macrometa_target_mongo']

package_data = \
{'': ['*']}

install_requires = \
['adjust-precision-for-schema==0.3.4',
 'c8connector>=0.0.29',
 'pipelinewise-singer-python==1.2.0',
 'prometheus-client==0.16.0',
 'pymongo[srv]>=4.0,<5.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['macrometa-target-mongo = '
                     'macrometa_target_mongo.main:main']}

setup_kwargs = {
    'name': 'macrometa-target-mongo',
    'version': '0.0.22',
    'description': 'Macrometa connector for writing data into MongoDB, can be used as a target for any Data Mesh Integration.',
    'long_description': 'None',
    'author': 'Macrometa',
    'author_email': 'product@macrometa.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.11',
}


setup(**setup_kwargs)
