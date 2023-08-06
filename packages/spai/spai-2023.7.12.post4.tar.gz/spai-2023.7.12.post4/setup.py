# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spai',
 'spai.cli',
 'spai.cli.commands',
 'spai.cli.src.errors',
 'spai.cli.src.repos',
 'spai.cli.src.usecases.auth',
 'spai.cli.src.usecases.project',
 'spai.cli.src.usecases.project.project-template.apis.analytics',
 'spai.cli.src.usecases.project.project-template.apis.xyz',
 'spai.cli.src.usecases.project.project-template.scripts.downloader',
 'spai.cli.src.usecases.project.project-template.scripts.ndvi',
 'spai.cli.src.usecases.project.project-template.uis.map',
 'spai.cli.src.usecases.run',
 'spai.data',
 'spai.data.satellite',
 'spai.data.satellite.sentinelhub',
 'spai.image',
 'spai.image.xyz',
 'spai.pulses',
 'spai.storage']

package_data = \
{'': ['*'],
 'spai.cli.src.usecases.project': ['project-template/*',
                                   'project-template/notebooks/analytics/*']}

install_requires = \
['minio>=7.1.15,<8.0.0', 'overpy>=0.6,<0.7', 'pandas>=2.0.2,<3.0.0']

entry_points = \
{'console_scripts': ['spai = spai.main:app']}

setup_kwargs = {
    'name': 'spai',
    'version': '2023.7.12.post4',
    'description': '',
    'long_description': '# SPAI CLI\n\n## Create new project\n\n```bash\nspai init\n```\n',
    'author': 'Juan Sensio',
    'author_email': 'it@earthpulse.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
