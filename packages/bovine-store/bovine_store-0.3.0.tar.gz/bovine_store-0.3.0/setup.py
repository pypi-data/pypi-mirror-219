# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bovine_store',
 'bovine_store.actor',
 'bovine_store.server',
 'bovine_store.store',
 'bovine_store.utils']

package_data = \
{'': ['*'], 'bovine_store.server': ['templates/*']}

install_requires = \
['bovine>=0.3.0,<0.4.0',
 'quart>=0.18.3,<0.19.0',
 'tortoise-orm[asyncpg]>=0.19.3,<0.20.0']

setup_kwargs = {
    'name': 'bovine-store',
    'version': '0.3.0',
    'description': 'Store for ActivityPub activities, actors and objects',
    'long_description': "# bovine_store\n\n`bovine_store` is meant to be the module handling storing of\nlocal ActivityPub objects and caching of remote ActivityPub\nobjects.\n\n## Usage\n\nbovine_store assumes that a database connection is initialized using [tortoise-orm](https://tortoise.github.io/). See `examples/basic_app.py` for how to do this in the context of a quart app.\n\n## TODO\n\n- [ ] When properties of actor are updated, send an update Activity\n  - Doesn't fit into the current bovine framework ... bovine_store doesn't know how to send activities\n- [ ] Generally rework the actor properties mechanism. It is currently not possible to emulate say Mastodon featured collection with it.\n- [ ] bovine_store.models.BovineActorKeyPair needs renamings; and work, e.g. a future identity column should have a uniqueness constraint.\n- [ ] Generally the code quality is not as high as it should be.\n\n## Examples\n\nA demonstration webserver can be seen using\n\n```bash\npoetry run python examples/basic_app.py\n```\n\nNote this is a very basic example. Instructions what the example does are\nprinted to the command line after start.\n\nNote: This example creates two files `db.sqlite3`, which contains the\ndatabase and `context_cache.sqlite`, which contains the cache of json-ld\ncontexts.\n",
    'author': 'Helge',
    'author_email': 'helge.krueger@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://codeberg.org/bovine/bovine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
