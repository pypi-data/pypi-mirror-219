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

extras_require = \
{'hf-embeddings': ['sentence-transformers==2.2.2', 'torch==2.0.0']}

setup_kwargs = {
    'name': 'langroid',
    'version': '0.1.20',
    'description': 'Harness LLMs with Multi-Agent Programming',
    'long_description': '<div style="display: flex; align-items: center;">\n  <img src="docs/assets/orange-logo.png" alt="Logo" \n        width="80" height="80"align="left">\n  <h1>Langroid: Harness LLMs with Multi-Agent Programming</h1>\n</div>\n\n[![Pytest](https://github.com/langroid/langroid/actions/workflows/pytest.yml/badge.svg)](https://github.com/langroid/langroid/actions/workflows/pytest.yml)\n[![Lint](https://github.com/langroid/langroid/actions/workflows/validate.yml/badge.svg)](https://github.com/langroid/langroid/actions/workflows/validate.yml)\n[![Docs](https://github.com/langroid/langroid/actions/workflows/mkdocs-deploy.yml/badge.svg)](https://github.com/langroid/langroid/actions/workflows/mkdocs-deploy.yml)\n\nLangroid is an intuitive, lightweight, transparent, flexible, extensible and principled\nPython framework to harness LLMs using Multi-Agent Programming (MAP).\nWe welcome contributions!\n\nDocumentation: https://langroid.github.io/langroid/\n\n## Contributors:\n- Prasad Chalasani (IIT BTech/CS, CMU PhD/ML; Independent ML Consultant)\n- Somesh Jha (IIT BTech/CS, CMU PhD/CS; Professor of CS, U Wisc at Madison)\n- Mohannad Alhanahnah (Research Associate, U Wisc at Madison)\n- Ashish Hooda (IIT BTech/CS; PhD Candidate, U Wisc at Madison)\n\n## Overview\n\n### The LLM Opportunity\n\nGiven the remarkable abilities of recent Large Language Models (LLMs), there\nis an unprecedented opportunity to build intelligent applications powered by\nthis transformative technology. The top question for any enterprise is: how\nbest to harness the power of LLMs for complex applications? For technical and\npractical reasons, building LLM-powered applications is not as simple as\nthrowing a task at an LLM-system and expecting it to do it.\n\n### Langroid\'s Multi-Agent Programming Framework\n\nEffectively leveraging LLMs at scale requires a *principled programming\nframework*. In particular, there is often a need to maintain multiple LLM\nconversations, each instructed in different ways, and "responsible" for\ndifferent aspects of a task.\n\nAn *agent* is a convenient abstraction that encapsulates LLM conversation\nstate, along with access to long-term memory (vector-stores) and tools (a.k.a functions\nor plugins). Thus a **Multi-Agent Programming** framework is a natural fit\nfor complex LLM-based applications.\n\n> Langroid is the first Python LLM-application framework that was explicitly\ndesigned  with Agents as first-class citizens, and Multi-Agent Programming\nas the core  design principle. The framework is inspired by ideas from the\n[Actor Framework](https://en.wikipedia.org/wiki/Actor_model).\n\nLangroid allows an intuitive definition of agents, tasks and task-delegation\namong agents. There is a principled mechanism to orchestrate multi-agent\ncollaboration. Agents act as message-transformers, and take turns responding to (and\ntransforming) the current message. The architecture is lightweight, transparent,\nflexible, and allows other types of orchestration to be implemented.\nBesides Agents, Langroid also provides simple ways to directly interact with  \nLLMs and vector-stores.\n\n### Highlights\nHighlights of Langroid\'s features as of July 2023:\n\n- **Agents as first-class citizens:** An Agent is an abstraction that encapsulates LLM conversation state,\n  and optionally a vector-store and tools. Agents are the core abstraction in Langroid.\n  Agents act as _message transformers_, and by default provide 3 responder methods,  \n  one corresponding to each entity: LLM, Agent, User.\n- **Tasks:** A Task class wraps an Agent, and gives the agent instructions (or roles, or goals), \n  manages iteration over an Agent\'s responder methods, \n  and orchestrates multi-agent interactions via hierarchical, recursive\n  task-delegation. The `Task.run()` method has the same \n  type-signature as an Agent\'s responder\'s methods, and this is key to how \n  a task of an agent can delegate to other sub-tasks.\n- **LLM Support**: Langroid supports OpenAI LLMs including GPT-3.5-Turbo,\n  GPT-4-0613\n- **Caching of LLM prompts, responses:** Langroid uses [Redis](https://redis.com/try-free/) for caching.\n- **Vector Store Support**: [Qdrant](https://qdrant.tech/) and [Chroma](https://www.trychroma.com/) are currently supported.\n  Vector stores allow for Retrieval-Augmented-Generaation (RAG).\n- **Grounding and source-citation:** Access to external documents via vector-stores \n   allows for grounding and source-citation.\n- **Observability: Logging and provenance/lineage:** Langroid generates detailed logs of multi-agent interactions and\n  and maintains provenance/lineage of messages, so that you can trace back\n  the origin of a message.\n- **Tools/Plugins/Function-calling**: Langroid supports OpenAI\'s recently\n  released [function calling](https://platform.openai.com/docs/guides/gpt/function-calling)\n  feature. In addition, Langroid has its own native equivalent, which we\n  call **tools** (also known as "plugins" in other contexts). Function\n  calling and tools have the same developer-facing interface, implemented\n  using [Pydantic](https://docs.pydantic.dev/latest/),\n  which makes it very easy to define tools/functions and enable agents\n  to use them. Benefits of using Pydantic are that you never have to write\n  complex JSON specs for function calling, and when the LLM\n  hallucinates malformed JSON, the Pydantic error message is sent back to\n  the LLM so it can fix it!\n\n# Usage/quick-start\nThese are quick teasers to give a glimpse of what you can do with Langroid\nand how your code would look. See the \n[`Getting Started Guide`](https://langroid.github.io/langroid/getting_started/)\nfor more details.\n\n## Install `langroid` \nUse `pip` to install `langroid` (from PyPi) to your virtual environment:\n```bash\npip install langroid\n```\n\n## Set up environment variables (API keys, etc)\n\nCopy the `.env-template` file to a new file `.env` and \ninsert these secrets:\n- **OpenAI API** key (required): If you don\'t have one, see [this OpenAI Page](https://help.openai.com/en/collections/3675940-getting-started-with-openai-api).\n- **Qdrant** Vector Store API Key (required for apps that need retrieval from\n  documents): Sign up for a free 1GB account at [Qdrant cloud](https://cloud.qdrant.io)\n  Alternatively [Chroma](https://docs.trychroma.com/) is also currently supported. \n  We use the local-storage version of Chroma, so there is no need for an API key.\n- **GitHub** Personal Access Token (required for apps that need to analyze git\n  repos; token-based API calls are less rate-limited). See this\n  [GitHub page](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).\n- **Redis** Password (optional, only needed to cache LLM API responses):\n  Redis [offers](https://redis.com/try-free/) a free 30MB Redis account\n  which is more than sufficient to try out Langroid and even beyond.\n  \n```bash\ncp .env-template .env\n# now edit the .env file, insert your secrets as above\n``` \nYour `.env` file should look like this:\n```bash\nOPENAI_API_KEY=<your key>\nGITHUB_ACCESS_TOKEN=<your token>\nREDIS_PASSWORD=<your password>\nQDRANT_API_KEY=<your key>\n```\n\nCurrently only OpenAI models are supported. Others will be added later\n(Pull Requests welcome!).\n\n## Direct interaction with OpenAI LLM\n\n```python\nfrom langroid.language_models.openai_gpt import ( \n        OpenAIGPTConfig, OpenAIChatModel, OpenAIGPT,\n)\nfrom langroid.language_models.base import LLMMessage, Role\n\ncfg = OpenAIGPTConfig(chat_model=OpenAIChatModel.GPT4)\n\nmdl = OpenAIGPT(cfg)\n\nmessages = [\n  LLMMessage(content="You are a helpful assistant",  role=Role.SYSTEM), \n  LLMMessage(content="What is the capital of Ontario?",  role=Role.USER),\n],\nresponse = mdl.chat(messages, max_tokens=200)\n```\n\n## Define an agent, set up a task, and run it\n\n```python\nfrom langroid.agent.chat_agent import ChatAgent, ChatAgentConfig\nfrom langroid.agent.task import Task\nfrom langroid.language_models.openai_gpt import OpenAIChatModel, OpenAIGPTConfig\n\nconfig = ChatAgentConfig(\n    llm = OpenAIGPTConfig(\n        chat_model=OpenAIChatModel.GPT4,\n    ),\n    vecdb=None, # no vector store\n)\nagent = ChatAgent(config)\n# get response from agent\'s LLM ...\nanswer = agent.llm_response("What is the capital of Ontario?")\n# ... or set up a task..\ntask = Task(agent, name="Bot") \ntask.run() # ... a loop seeking response from Agent, LLM or User at each turn\n```\n\n## Three communicating agents\n\nA toy numbers game, where when given a number `n`:\n- `repeater_agent`\'s LLM simply returns `n`,\n- `even_agent`\'s LLM returns `n/2` if `n` is even, else says "DO-NOT-KNOW"\n- `odd_agent`\'s LLM returns `3*n+1` if `n` is odd, else says "DO-NOT-KNOW"\n\nFirst define the 3 agents, and set up their tasks with instructions:\n\n```python\n    config = ChatAgentConfig(\n        llm = OpenAIGPTConfig(\n            chat_model=OpenAIChatModel.GPT4,\n        ),\n        vecdb = None,\n    )\n    repeater_agent = ChatAgent(config)\n    repeater_task = Task(\n        repeater_agent,\n        name = "Repeater",\n        system_message="""\n        Your job is to repeat whatever number you receive.\n        """,\n        llm_delegate=True, # LLM takes charge of task\n        single_round=False, \n    )\n    even_agent = ChatAgent(config)\n    even_task = Task(\n        even_agent,\n        name = "EvenHandler",\n        system_message=f"""\n        You will be given a number. \n        If it is even, divide by 2 and say the result, nothing else.\n        If it is odd, say {NO_ANSWER}\n        """,\n        single_round=True,  # task done after 1 step() with valid response\n    )\n\n    odd_agent = ChatAgent(config)\n    odd_task = Task(\n        odd_agent,\n        name = "OddHandler",\n        system_message=f"""\n        You will be given a number n. \n        If it is odd, return (n*3+1), say nothing else. \n        If it is even, say {NO_ANSWER}\n        """,\n        single_round=True,  # task done after 1 step() with valid response\n    )\n```\nThen add the `even_task` and `odd_task` as sub-tasks of `repeater_task`, \nand run the `repeater_task`, kicking it off with a number as input:\n```python\n    repeater_task.add_sub_task([even_task, odd_task])\n    repeater_task.run("3")\n```\n\n\n\n',
    'author': 'Prasad Chalasani',
    'author_email': 'pchalasani@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.1,<3.12',
}


setup(**setup_kwargs)
