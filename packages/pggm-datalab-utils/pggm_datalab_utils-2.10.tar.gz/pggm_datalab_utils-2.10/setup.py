# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pggm_datalab_utils']

package_data = \
{'': ['*']}

install_requires = \
['pyodbc>=4.0.34,<5.0.0']

setup_kwargs = {
    'name': 'pggm-datalab-utils',
    'version': '2.10',
    'description': 'Utilities created and used by the Datalab of PGGM',
    'long_description': "# Datalab utils\nWell-specified utilities from the Datalab of PGGM. Our aim with this package is to provide some tooling to make our lives a bit easier.\nSo far the package contains:\n- Database utilities, allowing you to connect to cloud databases using pyodbc in a standard pattern.\n- Helpers around nested lists (flattening and unflattening).\n- Helpers to make working with lists of dictionaries a bit easier so you don't have to resort to Pandas as fast.\n\n## How to use the database helpers\n```python\nfrom pggm_datalab_utils.db import cursor, query\n\nbbg_id = 'WOW'\n\nwith cursor('pggm-sql-lre-o.database.windows.net', 'lre') as c:\n    data = query(c, 'select sedol, name from portfolio where bbg_id=?', bbg_id)\n```",
    'author': 'Rik de Kort',
    'author_email': 'rik.de.kort@pggm.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
