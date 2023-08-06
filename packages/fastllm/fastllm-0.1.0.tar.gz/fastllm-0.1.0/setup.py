# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastllm']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=2.2.1,<3.0.0', 'jinja2>=3.1.2,<4.0.0', 'openai>=0.27.8,<0.28.0']

setup_kwargs = {
    'name': 'fastllm',
    'version': '0.1.0',
    'description': 'Fast and easy wrapper around LLMs.',
    'long_description': '# FastLLM\n\nFast and easy wrapper around LLMs. The package aims to be simply, precise and allows for fast prototyping of agents and applications around LLMs. At the moment focus around OpenAI\'s models.\n\n**Warning - very early stage of development.**\n\n## Samples\n\nRequire an openai api key in `OPENAI_API_KEY` environment variable or `.env` file.\n\n```bash\nexport OPENAI_API_KEY=...\n```\n\n### Agents\n\n```python\nfrom fastllm import Agent\n\nfind_cities = Agent("List {{ n }} cities comma separated in {{ country }}.")\n\ncities = find_cities(n=3, country="Austria").split(",")\n\nprint(cities)\n```\n\n```bash\n[\'Vienna\', \'Salzburg\', \'Graz\']\n```\n\n```python\nfrom fastllm import Agent, Message, Model, Prompt, Role\n\ns = ";"\n\ncreative_name_finder = Agent(\n    Message("You are an expert name finder.", Role.SYSTEM),\n    Prompt("Find {{ n }} names.", temperature=2.0),\n    Prompt("Print names {{ s }} separated, nothing else!"),\n    model=Model("gpt-4"),\n)\n\nnames = creative_name_finder(n=3, s=s).split(s)\n\nprint(names)\n```\n\n```bash\n[\'Ethan Gallagher, Samantha Cheng, Max Thompson\']\n```\n\n## Development\n\nUsing [poetry](https://python-poetry.org/docs/#installation).\n\n```bash\npoetry install\n```\n\n### Tests\n\n```bash\npoetry run pytest\n``` ',
    'author': 'Clemens Kriechbaumer',
    'author_email': 'clemens.kriechbaumer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/clemens33/fastllm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
