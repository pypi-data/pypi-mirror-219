# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyepics_asyncio']

package_data = \
{'': ['*']}

install_requires = \
['pyepics>=3.5.1,<4.0.0']

setup_kwargs = {
    'name': 'pyepics-asyncio',
    'version': '0.2.2',
    'description': 'Async/await wrapper for PyEpics',
    'long_description': '# pyepics-asyncio\n\nSimple `async`/`await` wrapper for [PyEpics](https://github.com/pyepics/pyepics).\n\n## Overview\n\nThere are two main types:\n+ `PvMonitor` - subscribed to PV updates, `get` returns last received value.\n+ `Pv` - connected but not subscribed, each `get` requests PV value over network.\n\n## Usage\n\n### Read PV value\n\n```python\nfrom pyepics_asyncio import Pv\n\npv = await Pv.connect("pvname")\nprint(await pv.get())\n```\n\n### Monitor PV\n\n```python\nfrom pyepics_asyncio import PvMonitor\n\npv = await PvMonitor.connect("pvname")\nasync for value in pv:\n    print(value)\n```\n\n### Write value to PV\n\n```python\nawait pv.put(3.1415)\n```\n\n## Testing\n\nTo run tests you need to have dummy IOC running (located in `ioc` dir):\n\n+ Set appropriate `EPICS_BASE` path in `configure/RELEASE`.\n+ Build with `make`.\n+ Go to `iocBoot/iocTest/` and run script `st.cmd` and don\'t stop it.\n\nIn separate shell run `poetry run pytest --verbose`.\n',
    'author': 'Alexey Gerasev',
    'author_email': 'alexey.gerasev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/agerasev/pyepics-asyncio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
