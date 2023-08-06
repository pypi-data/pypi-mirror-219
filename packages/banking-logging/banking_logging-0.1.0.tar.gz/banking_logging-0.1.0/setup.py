#
import setuptools
from setuptools import setup


metadata = {'name': 'banking_logging',
            'maintainer': 'Edward Azizov',
            'maintainer_email': 'edazizovv@gmail.com',
            'description': 'Shared loggers for banking_api project',
            'license': 'Proprietary',
            'url': '',
            'download_url': '',
            'packages': setuptools.find_packages(),
            'include_package_data': True,
            'version': '0.1.0',
            'long_description': '',
            'python_requires': '>=3.10',
            'install_requires': []}

setup(**metadata)
