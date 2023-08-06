# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['langroid',
 'langroid.agent',
 'langroid.agent.special',
 'langroid.cachedb',
 'langroid.embedding_models',
 'langroid.language_models',
 'langroid.parsing',
 'langroid.prompts',
 'langroid.scripts',
 'langroid.utils',
 'langroid.utils.llms',
 'langroid.utils.output',
 'langroid.utils.web',
 'langroid.vector_store']

package_data = \
{'': ['*']}

install_requires = \
['autopep8>=2.0.2,<3.0.0',
 'black[jupyter]>=23.3.0,<24.0.0',
 'bs4>=0.0.1,<0.0.2',
 'chromadb>=0.3.21,<0.4.0',
 'colorlog>=6.7.0,<7.0.0',
 'faker>=18.9.0,<19.0.0',
 'fakeredis>=2.12.1,<3.0.0',
 'fire>=0.5.0,<0.6.0',
 'flake8>=6.0.0,<7.0.0',
 'halo>=0.0.31,<0.0.32',
 'mkdocs-awesome-pages-plugin>=2.8.0,<3.0.0',
 'mkdocs-gen-files>=0.4.0,<0.5.0',
 'mkdocs-jupyter>=0.24.1,<0.25.0',
 'mkdocs-literate-nav>=0.6.0,<0.7.0',
 'mkdocs-material>=9.1.5,<10.0.0',
 'mkdocs-section-index>=0.3.5,<0.4.0',
 'mkdocs>=1.4.2,<2.0.0',
 'mkdocstrings[python]>=0.21.2,<0.22.0',
 'mypy>=1.2.0,<2.0.0',
 'nltk>=3.8.1,<4.0.0',
 'openai>=0.27.5,<0.28.0',
 'pre-commit>=3.3.2,<4.0.0',
 'pydantic==1.10.11',
 'pygithub>=1.58.1,<2.0.0',
 'pygments>=2.15.1,<3.0.0',
 'pyparsing>=3.0.9,<4.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'qdrant-client>=1.3.1,<2.0.0',
 'redis>=4.5.5,<5.0.0',
 'requests-oauthlib>=1.3.1,<2.0.0',
 'requests>=2.31.0,<3.0.0',
 'rich>=13.3.4,<14.0.0',
 'ruff>=0.0.270,<0.0.271',
 'tiktoken>=0.3.3,<0.4.0',
 'trafilatura>=1.5.0,<2.0.0',
 'typer>=0.7.0,<0.8.0',
 'types-redis>=4.5.5.2,<5.0.0.0',
 'types-requests>=2.31.0.1,<3.0.0.0',
 'wget>=3.2,<4.0']

setup_kwargs = {
    'name': 'langroid',
    'version': '0.1.17',
    'description': 'Harness LLMs with Multi-Agent Programming',
    'long_description': '<div style="display: flex; align-items: center;">\n  <img src="docs/assets/orange-logo.png" alt="Logo" \n        width="80" height="80"align="left">\n  <h1>Langroid</h1>\n</div>\n\n[![Pytest](https://github.com/langroid/langroid/actions/workflows/pytest.yml/badge.svg)](https://github.com/langroid/langroid/actions/workflows/pytest.yml)\n[![Lint](https://github.com/langroid/langroid/actions/workflows/validate.yml/badge.svg)](https://github.com/langroid/langroid/actions/workflows/validate.yml)\n[![Docs](https://github.com/langroid/langroid/actions/workflows/mkdocs-deploy.yml/badge.svg)](https://github.com/langroid/langroid/actions/workflows/mkdocs-deploy.yml)\n\n\n## Contributors:\n- Prasad Chalasani (Independent ML Consultant)\n- Somesh Jha (Professor of CS, U Wisc at Madison)\n- Mohannad Alhanahnah (Research Associate, U Wisc at Madison)\n- Ashish Hooda (PhD Candidate, U Wisc at Madison)\n\n## Set up dev env\n\nWe use [`poetry`](https://python-poetry.org/docs/#installation) \nto manage dependencies, and `python 3.11` for development.\n\nFirst install `poetry`, then create virtual env and install dependencies:\n\n```bash\n# clone this repo and cd into repo root\ngit clone ...\ncd <repo_root>\n# create a virtual env under project root, .venv directory\npython3 -m venv .venv\n\n# activate the virtual env\n. .venv/bin/activate\n\n# use poetry to install dependencies (these go into .venv dir)\npoetry install\n\n```\nTo add packages, use `poetry add <package-name>`. This will automatically \nfind the latest compatible version of the package and add it to `pyproject.\ntoml`. _Do not manually edit `pyproject.toml` to add packages._\n\n## Set up environment variables (API keys, etc)\n\nCopy the `.env-template` file to a new file `.env` and \ninsert these secrets:\n- OpenAI API key, \n- GitHub Personal Access Token (needed by  PyGithub to analyze git repos; \n  token-based API calls are less rate-limited).\n- Redis Password for the redis cache. \n- Qdrant API key for the vector database.\n\n```bash\ncp .env-template .env\n# now edit the .env file, insert your secrets as above\n``` \n\nCurrently only OpenAI models are supported. Others will be added later.\n\n## Run tests\nTo verify your env is correctly setup, run all tests using `make tests`.\n\n## Generate docs (private only for now)\n\nGenerate docs: `make docs`, then go to the IP address shown at the end, like \n`http://127.0.0.1:8000/`\nNote this runs a docs server in the background.\nTo stop it, run `make nodocs`. Also, running `make docs` next time will kill \nany previously running `mkdocs` server.\n\n\n## Contributing, and Pull requests\n\nIn this Python repository, we prioritize code readability and maintainability.\nTo ensure this, please adhere to the following guidelines when contributing:\n\n1. **Type-Annotate Code:** Add type annotations to function signatures and\n   variables to make the code more self-explanatory and to help catch potential\n   issues early. For example, `def greet(name: str) -> str:`.\n\n2. **Google-Style Docstrings:** Use Google-style docstrings to clearly describe\n   the purpose, arguments, and return values of functions. For example:\n\n   ```python\n   def greet(name: str) -> str:\n       """Generate a greeting message.\n\n       Args:\n           name (str): The name of the person to greet.\n\n       Returns:\n           str: The greeting message.\n       """\n       return f"Hello, {name}!"\n   ```\n\n3. **PEP8-Compliant 80-Char Max per Line:** Follow the PEP8 style guide and keep\n   lines to a maximum of 80 characters. This improves readability and ensures\n   consistency across the codebase.\n\nIf you are using an LLM to write code for you, adding these \ninstructions will usually get you code compliant with the above:\n```\nuse type-annotations, google-style docstrings, and pep8 compliant max 80 \n     chars per line.\n```     \n\n\nBy following these practices, we can create a clean, consistent, and\neasy-to-understand codebase for all contributors. Thank you for your\ncooperation!\n\nTo check for issues locally, run `make check`, it runs linters `black`, `ruff`,\n`flake8` and type-checker `mypy`. Issues flagged by `black` can usually be \nauto-fixed using `black .`, and to fix `ruff issues`, do:\n```\npoetry run ruff . --fix\n```\n\n- When you run this, `black` may warn that some files _would_ be reformatted. \nIf so, you should just run `black .` to reformat them. Also,\n- `flake8` may warn about some issues; read about each one and fix those \n  issues.\n\nYou can also run `make lint` to (try to) auto-tix `black` and `ruff`\nissues. \n\nSo, typically when submitting a PR, you would do this sequence:\n- run `pytest tests -nc` (`-nc` means "no cache", i.e. do not use cached LLM \n  API call responses)\n- fix things so tests pass, then proceed to lint/style/type checks\n- `make check` to see what issues there are\n- `make lint` to auto-fix some of them\n- `make check` again to see what issues remain\n- possibly manually fix `flake8` issues, and any `mypy` issues flagged.\n- `make check` again to see if all issues are fixed.\n- repeat if needed, until all clean. \n\nWhen done with these, git-commit, push to github and submit the PR. If this \nis an ongoing PR, just push to github again and the PR will be updated. \n\nStrongly recommend to use the `gh` command-line utility when working with git.\nRead more [here](docs/development/github-cli.md).\n\n\n\n## Run some examples\n\nThere  are now several examples under `examples` and `examples_dev`. \nThey are typically run with `python3 examples/.../chat.py`, but sometimes \nthe app name may not be `chat.py`.\nGenerally speaking, these commands can take additional command-line options, \ne.g.: \n- `-nc` to disable using cached LLM responses (i.e. forces fresh response)\n- `-d` or `--debug` to see more output\n- `-f` to enable using OpenAI function-calling instead of Langroid tools.\n\nHere are some apps to try (others will be described later):\n\n### "Chat" with a set of URLs.\n\n```bash\npython3 examples/docqa/chat.py\n```\n\nAsk a question you want answered based on the URLs content. The default \nURLs are about various articles and discussions on LLM-based agents, \ncompression and intelligence. If you are using the default URLs, try asking:\n\n> who is Pattie Maes?\n\nand then a follow-up question:\n\n> what did she build?\n\n## Logs of multi-agent interactions\n\nWhen running a multi-agent chat, e.g. using `task.run()`, two types of logs \nare generated:\n- plain-text logs in `logs/<task_name>.log`\n- tsv logs in `logs/<task_name>.tsv`\n\nWe will go into details of inter-agent chat structure in another place, \nbut for now it is important to realize that the logs show _every attempt at \n  responding to the current pending message, even those that are not allowed_.\nThe ones marked with an asterisk (*) are the ones that are considered the \nresponses for a given `step()` (which is a "turn" in the conversation).\n\nThe plain text logs have color-coding ANSI chars to make them easier to read \nby doing `less <log_file>`. The format is:\n```\n(TaskName) Responder SenderEntity (EntityName) (=> Recipient) TOOL Content\n```\n\nThe structure of the `tsv` logs is similar. A great way to view these is to \ninstall and use `visidata` (https://www.visidata.org/):\n```bash\nvd logs/<task_name>.tsv\n```\n\n',
    'author': 'Prasad Chalasani',
    'author_email': 'pchalasani@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.12',
}


setup(**setup_kwargs)
