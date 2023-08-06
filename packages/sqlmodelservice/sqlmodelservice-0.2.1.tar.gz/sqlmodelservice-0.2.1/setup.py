# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlmodelservice']

package_data = \
{'': ['*']}

install_requires = \
['sqlmodel>=0.0.8,<0.0.9']

setup_kwargs = {
    'name': 'sqlmodelservice',
    'version': '0.2.1',
    'description': 'A generic service layer on top of SQLModel for conveniently creating APIs with frameworks like FastAPI.',
    'long_description': '# SQLModelService\n\n`SQLModelService` is a generic service layer on top of [SQLModel](https://sqlmodel.tiangolo.com/) for conveniently creating APIs with frameworks like [FastAPI](https://fastapi.tiangolo.com/).\n\nSee the [documentation](https://volfpeter.github.io/sqlmodelservice) for examples and the API reference.\n\n## Installation\n\nThe library is available on PyPI and can be installed with:\n\n```console\n$ pip install sqlmodelservice\n```\n\n## Dependencies\n\nThe only direct dependency of the project -- as the name suggests -- is `SQLModel`.\n\n## Contributing\n\nContributions are welcome.\n\n## License\n\nThe library is open-sourced under the conditions of the [MIT license](https://choosealicense.com/licenses/mit/).\n',
    'author': 'Peter Volf',
    'author_email': 'do.volfp@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
