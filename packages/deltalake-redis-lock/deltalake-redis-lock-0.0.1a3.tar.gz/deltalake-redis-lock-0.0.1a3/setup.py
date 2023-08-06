# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['deltalake>=0.10.0,<0.11.0',
 'pandas==2.0.3',
 'pyarrow>=12.0.1,<13.0.0',
 'redis>=4.6.0,<5.0.0']

setup_kwargs = {
    'name': 'deltalake-redis-lock',
    'version': '0.0.1a3',
    'description': 'deltalake-redis-lock',
    'long_description': '# deltalake-redis-lock\n\n![example workflow](https://github.com/wrapbytes/deltalake-redis-lock/actions/workflows/merge.yaml/badge.svg)\n![example workflow](https://github.com/wrapbytes/deltalake-redis-lock/actions/workflows/pr.yaml/badge.svg)\n\nA library creating an interface for a write lock for [delta-rs](https://pypi.org/project/deltalake/).\n\n## Library Usage\n\nWhen using this client, it can be used from multiple hosts. Below follow a minimal example\nto mimic this behaviour.\n\n### Redis Env Variables\n\nMake sure to set these `envs` before executing code.\n```bash\nREDIS_HOST=<host>\nREDIS_PORT=<port>  # default 6739\nREDIS_DB=<0>  # default 0\n```\n\n### Concurrent Write Example\n```python\n# run.py\nimport logging\nimport os\nimport string\nfrom random import choices\nfrom multiprocessing import Pool\n\nfrom pandas import DataFrame\n\nfrom src.delta_rs import write_redis_lock_deltalake\n\n\ndef fake_worker(args):\n    df, table_name = args\n\n    logging.basicConfig(\n        level=logging.INFO,\n        format=\'%(asctime)s [%(levelname)s] %(message)s\',\n        datefmt=\'%Y-%m-%d %H:%M:%S\'\n    )\n\n    write_redis_lock_deltalake(\n        table_or_uri=f"{os.getcwd()}/{table_name}",\n        lock_table_name=table_name,\n        mode="append",\n        data=df,\n        overwrite_schema=True,\n    )\n\n\ndef define_datasets(_table_name: str) -> None:\n    df1 = DataFrame({"id": [1]})\n    df2 = DataFrame({"id": [2]})\n    df3 = DataFrame({"id": [3]})\n    df4 = DataFrame({"id": [4]})\n\n    datasets = [(df1, table_name), (df2, table_name), (df3, table_name), (df4, table_name)]\n\n    with Pool() as pool:\n        pool.map(fake_worker, datasets)\n\n\ndef generate_random_string(length):\n    return "".join(choices(string.ascii_lowercase, k=length))\n\n\nif __name__ == \'__main__\':\n    random_string = generate_random_string(3)\n    table_name = f"test_run_{random_string}"\n\n    define_datasets(_table_name=table_name)\n```\n\nThis can be exeucted with something like:\n\n```bash\nseq 2 | xargs -I{} -P 2 poetry run python run.py\n```\n\n## Setup From Scratch\n\n### Requirement\n\n* ^python3.9\n* poetry 1.1.13\n* make (GNU Make 3.81)\n\n### Setup\n\n```bash\nmake setup-environment\n```\n\nUpdate package\n```bash\nmake update\n```\n\n### Test\n\n```bash\nexport PYTHONPATH="${PYTHONPATH}:src"\nmake test type=unit\n```\n\n### Docker\n\nThe reason `docker` is used in the source code here, is to be able to build up an encapsulated\nenvironment of the codebase, and do `unit/integration and load tests`.\n\n```bash\nmake build-container-image DOCKER_BUILD="buildx build --platform linux/amd64" CONTEXT=.\n```\n\n```bash\nmake get-container-info-environment\nmake run-container-tests type=unit\n```\n',
    'author': 'Simon Thelin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wrapbytes/deltalake-redis-lock',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
