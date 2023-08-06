#
import setuptools
from setuptools import setup


metadata = {'name': 'banking_api_shared',
            'maintainer': 'Edward Azizov',
            'maintainer_email': 'edazizovv@gmail.com',
            'description': 'Shared extensions for banking_api project',
            'license': 'Proprietary',
            'url': 'https://github.com/edazizovv/oaiv',
            'download_url': 'https://github.com/edazizovv/oaiv',
            'packages': setuptools.find_packages(),
            'include_package_data': True,
            'version': '0.1.2',
            'long_description': '',
            'python_requires': '>=3.10',
            'install_requires': []}

setup(**metadata)
