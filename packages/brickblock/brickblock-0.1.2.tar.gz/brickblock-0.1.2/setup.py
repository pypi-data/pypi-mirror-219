# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brickblock']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.2,<4.0.0', 'numpy>=1.25.1,<2.0.0', 'pytest>=7.4.0,<8.0.0']

setup_kwargs = {
    'name': 'brickblock',
    'version': '0.1.2',
    'description': 'A fun visualisation library for those that like boxes',
    'long_description': "# Brickblock: A fun visualisation library for those that like boxes\n\nThis is a small library that uses blocks in matplotlib's visually appealing 3D extension - and aims to be the 'seaborn of matplotlib-3D'.\n\n## Core abstractions\n\nAt the centre of Brickblock is the `Space`. A `Space` represents a 3D cartesian coordinate space. It contains objects, and when a user wants a visualisation, they render the current state of the `Space` - the rendered state is known as a `Scene`.\n\nThere are objects used for composing visualisations in Brickblock, such as the `Cube`. `Cube` objects can be added into the `Space` with a degree of control over their visual presentation: transparency, colour, line widths.\n\nHaving these abstractions allows programmers to more easily create animated 3D visualisations, like GIFs. You define a `Space`, adding and mutating objects to evolve the state, and the `Scene` objects are persisted to enable sequences of images for use in GIFs.\n\n## Contributing\n\nContributions are more than welcome! There is a very rough TODO in `todo.md` that outlines both short- and long-term goals for the library. However, there are some rules:\n\n* Always follow the [code of conduct](CODE_OF_CONDUCT.md)\n* All the tests should be passing with your change\n* Explain your change (PR template coming soon)\n* Add relevant tests and docstrings\n* Format your changes with `black`\n",
    'author': 'Daniel Soutar',
    'author_email': 'danielsoutar144@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/danielsoutar/brickblock',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
