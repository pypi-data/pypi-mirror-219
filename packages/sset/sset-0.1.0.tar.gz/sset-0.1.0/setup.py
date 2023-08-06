# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sset']

package_data = \
{'': ['*']}

install_requires = \
['ellc>=1.8.8,<2.0.0',
 'lightkurve>=2.3.0,<3.0.0',
 'numpy>1.20.1',
 'pytest>=7.2.1,<8.0.0',
 'tess-prf>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'sset',
    'version': '0.1.0',
    'description': 'A tool for generating simulated cut outs of TESS target pixel files.',
    'long_description': '# SSET\n## Simulated Source Exposures of TESS\nReady... SSET... _GO!_\n\nA tool for generating simulated cut outs of target pixel files.\nCurrently under development.\n',
    'author': 'rae-holcomb',
    'author_email': 'raeholcomb15@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
