# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['miko',
 'miko.cmdline',
 'miko.graph',
 'miko.metad',
 'miko.structure',
 'miko.tesla',
 'miko.tesla.ai2_kit',
 'miko.tesla.base',
 'miko.tesla.dpgen',
 'miko.utils']

package_data = \
{'': ['*']}

install_requires = \
['ai2-kit>=0.3.18,<0.4.0',
 'ase>=3.21.1,<4.0.0',
 'dscribe>=2.0,<3.0',
 'matplotlib>=3.7.1,<4.0.0',
 'mdanalysis>=2.2,<3.0',
 'numpy>=1.18,<1.24',
 'pandas>=1.3.3,<2.0.0',
 'pymatgen>=2023.5.10,<2024.0.0',
 'scipy>=1.10.1,<2.0.0',
 'seaborn>=0.12.2,<0.13.0']

entry_points = \
{'console_scripts': ['miko = miko.cmdline.base:cli']}

setup_kwargs = {
    'name': 'miko-analyzer',
    'version': '0.3.3',
    'description': 'Analyzing tool for deep learning based chemical research.',
    'long_description': '# Miko-Analyzer\n\n[![Python package](https://github.com/Cloudac7/miko-analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/Cloudac7/miko-analyzer/actions/workflows/ci.yml)\n[![Coverage Status](https://coveralls.io/repos/github/Cloudac7/miko-analyzer/badge.svg?branch=master)](https://coveralls.io/github/Cloudac7/miko-analyzer?branch=master)\n\n> コードで占う巫女。\n> Miko using code to perform divinition.\n\nAn analysis plugin for [Deep Potential](https://github.com/deepmodeling/deepmd-kit) based chemical research.\n\nSupporting simple calculation workflow with the help of [DPDispatcher](https://github.com/deepmodeling/dpdispatcher).\n\n## Installation\n\nTo install, clone the repository:\n\n```\ngit clone https://github.com/cloudac7/miko-analyzer.git\n```\n\nand then install with `pip`:\n\n```\ncd miko-analyzer\npip install .\n```\n\n',
    'author': 'Cloudac7',
    'author_email': 'scottryuu@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cloudac7/miko-analysis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
