# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['biliarchiver', 'biliarchiver.cli_tools', 'biliarchiver.utils']

package_data = \
{'': ['*']}

install_requires = \
['bilix==0.18.4',
 'browser-cookie3>=0.19.1,<0.20.0',
 'danmakuc>=0.3.6,<0.4.0',
 'internetarchive>=3.5.0,<4.0.0']

entry_points = \
{'console_scripts': ['bili_archive_bvids = '
                     'biliarchiver.cli_tools:bili_archive_bvids.main',
                     'bili_get_bvids = '
                     'biliarchiver.cli_tools:bili_get_bvids.main',
                     'bili_upload = biliarchiver.cli_tools:bili_upload.main',
                     'biliarchiver = biliarchiver.cli_tools:biliarchiver.main']}

setup_kwargs = {
    'name': 'biliarchiver',
    'version': '0.0.20',
    'description': '',
    'long_description': '# biliarchiver\n\n> 基于 bilix 的 BiliBili 存档工具\n\n## Install\n\n```bash\npip install biliarchiver\n```\n\n## Usage\n\n待补充。\n',
    'author': 'yzqzss',
    'author_email': 'yzqzss@yandex.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
