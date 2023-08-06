# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['interval_sdk',
 'interval_sdk.classes',
 'interval_sdk.components',
 'interval_sdk.superjson',
 'interval_sdk.superjson.tests']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'typing-extensions>=4.4.0,<5.0.0',
 'websockets>=10.1,<11.0']

setup_kwargs = {
    'name': 'interval-sdk',
    'version': '1.5.0',
    'description': "The frontendless framework for high growth companies. Interval automatically generates apps by inlining the UI in your backend code. It's a faster and more maintainable way to build internal tools, rapid prototypes, and more.",
    'long_description': '<a href="https://interval.com">\n  <img alt="Interval" width="100" height="100" style="border-radius: 6px;" src="https://interval.com/img/readme-assets/interval-avatar.png">\n</a>\n\n# Interval Python SDK\n\n[![pypi version](https://img.shields.io/pypi/v/interval-sdk?style=flat)](https://pypi.org/project/interval-sdk) [![Documentation](https://img.shields.io/badge/documentation-informational)](https://interval.com/docs) [![Twitter](https://img.shields.io/twitter/follow/useinterval.svg?color=%2338A1F3&label=twitter&style=flat)](https://twitter.com/useinterval) [![Discord](https://img.shields.io/badge/discord-join-blueviolet)](https://interval.com/discord)\n\n[Interval](https://interval.com) lets you quickly build internal web apps (think: customer support tools, admin panels, etc.) just by writing backend Python code.\n\nThis is our Python SDK which connects to the interval.com web app. If you don\'t have an Interval account, you can [create one here](https://interval.com/signup). All core features are free to use.\n\n## Why choose Interval?\n\n_"Python code > no-code"_\n\nInterval is an alternative to no-code/low-code UI builders. Modern frontend development is inherently complicated, and teams rightfully want to spend minimal engineering resources on internal dashboards. No-code tools attempt to solve this problem by allowing you to build UIs in a web browser without writing any frontend code.\n\nWe don\'t think this is the right solution. **Building UIs for mission-critical tools in your web browser** — often by non-technical teammates, outside of your codebase, without versioning or code review — **is an anti-pattern.** Apps built in this manner are brittle and break in unexpected ways.\n\nWith Interval, **all of the code for generating your web UIs lives within your app\'s codebase.** Tools built with Interval (we call these [actions](https://interval.com/docs/concepts/actions)) are just asynchronous functions that run in your backend. Because these are plain old functions, you can access the complete power of your Python app. You can loop, conditionally branch, access shared functions, and so on. When you need to request input or display output, `await` any of our [I/O methods](https://interval.com/docs/io-methods/) to present a form to the user and your script will pause execution until input is received.\n\nHere\'s a simple app with a single "Hello, world" action:\n\n```python\nfrom interval_sdk import Interval, IO\n\n# Initialize Interval\ninterval = Interval(api_key="<YOUR API KEY>")\n\n@interval.action\nasync def hello_world(io: IO):\n    name = await io.input.text("Your name")\n    return f"Hello, {name}"\n\n\n# Synchronously listen, blocking forever\ninterval.listen()\n```\n\nTo not block, interval can also be run asynchronously using\n`interval.listen_async()`. You must provide your own event loop.\n\nThe task will complete as soon as connection to Interval completes, so you\nlikely want to run forever or run alongside another permanent task.\n\n```python\nimport asyncio, signal\n\nloop = asyncio.get_event_loop()\ntask = loop.create_task(interval.listen_async())\ndef handle_done(task: asyncio.Task[None]):\n    try:\n        task.result()\n    except:\n        loop.stop()\n\ntask.add_done_callback(handle_done)\nfor sig in {signal.SIGINT, signal.SIGTERM}:\n    loop.add_signal_handler(sig, loop.stop)\nloop.run_forever()\n```\n\nInterval:\n\n- Makes creating full-stack apps as easy as writing CLI scripts.\n- Can scale from a handful of scripts to robust multi-user dashboards.\n- Lets you build faster than no-code, without leaving your codebase & IDE.\n\nWith Interval, you do not need to:\n\n- Write REST or GraphQL API endpoints to connect internal functionality to no-code tools.\n- Give Interval write access to your database (or give us _any_ of your credentials, for that matter).\n- Build web UIs with a drag-and-drop interface.\n\n## More about Interval\n\n- 📖 [Documentation](https://interval.com/docs)\n- 🌐 [Interval website](https://interval.com)\n- 💬 [Discord community](https://interval.com/discord)\n- 📰 [Product updates](https://interval.com/blog)\n\n## Contributing\n\nThis project uses [Poetry](https://python-poetry.org/) for dependency\nmanagement\n\n1. `poetry install` to install dependencies\n2. `poetry shell` to activate the virtual environment\n\nTasks are configured using [poethepoet](https://github.com/nat-n/poethepoet)\n(installed as a dev dependency).\n\n- `poe demo [demo_name]` to run a demo (`basic` by default if `demo_name` omitted)\n- `poe test` to run `pytest` (can also run `pytest` directly in virtual env)\n\nCode is formatted using [Black](https://github.com/psf/black). Please configure\nyour editor to format on save using Black, or run `poe format` to format the\ncode before committing changes.\n\n## Tests\n\n*Note:* Tests currently require a local instance of the Interval backend.\n\nTests use [pytest](https://docs.pytest.org/en/7.1.x/) and\n[playwright](https://playwright.dev/python/).\n\nCurrently assumes the `test-runner@interval.com` user exists already.\nRun `yarn test` in the `web` directory at least once to create it before\nrunning these.\n',
    'author': 'Jacob Mischka',
    'author_email': 'jacob@interval.com',
    'maintainer': 'Jacob Mischka',
    'maintainer_email': 'jacob@interval.com',
    'url': 'https://interval.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
