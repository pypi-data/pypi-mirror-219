# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['harlequin', 'harlequin.tui', 'harlequin.tui.components']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'duckdb>=0.8.0',
 'shandy-sqlfmt>=0.19.0',
 'textual-textarea==0.3.2',
 'textual==0.29.0']

entry_points = \
{'console_scripts': ['harlequin = harlequin.cli:harlequin']}

setup_kwargs = {
    'name': 'harlequin',
    'version': '0.0.20',
    'description': 'A terminal-based SQL IDE for DuckDB',
    'long_description': '# harlequin\nA Terminal-based SQL IDE for DuckDB.\n\n![harlequin TUI](harlequinv0018.gif)\n\n(A Harlequin is also a [pretty duck](https://en.wikipedia.org/wiki/Harlequin_duck).)\n\n![harlequin duck](harlequin.jpg)\n\n## Installing Harlequin\n\nAfter installing Python 3.8 or above, install Harlequin using `pip` or `pipx` with:\n\n```bash\npipx install harlequin\n```\n\n> **Tip:**\n>\n> You can run invoke directly with [`pipx run`](https://pypa.github.io/pipx/examples/#pipx-run-examples) anywhere that `pipx` is installed. For example:\n> - `pipx run harlequin --help`\n> - `pipx run harlequin ./my.duckdb`\n\n\n## Using Harlequin\n\nFrom any shell, to open one or more DuckDB database files:\n\n```bash\nharlequin "path/to/duck.db" "another_duck.db"\n```\n\nTo open an in-memory DuckDB session, run Harlequin with no arguments:\n\n```bash\nharlequin\n```\n\nYou can also open a database in read-only mode:\n\n```bash\nharlequin -r "path/to/duck.db"\n```\n\n### Using Harlequin with MotherDuck\n\nYou can use Harlequin with MotherDuck, just as you would use the DuckDB CLI:\n\n```bash\nharlequin "md:"\n```\n\nYou can attach local databases as additional arguments (`md:` has to be first:)\n\n```bash\nharlequin "md:" "local_duck.db"\n```\n\n#### Authentication Options\n\n1. Web browser: Run `harlequin "md:"`, and Harlequin will attempt to open a web browser where you can log in.\n2. Use an environment variable: Set the `motherduck_token` variable before running `harlequin "md:"`, and Harlequin will authenticate with MotherDuck using your service token.\n3. Use the CLI option: You can pass a service token to Harlequin with `harlequin "md:" --md_token <my token>`\n\n#### SaaS Mode\n\nYou can run Harlequin in ["SaaS Mode"](https://motherduck.com/docs/authenticating-to-motherduck#authentication-using-saas-mode) by passing the `md_saas` option: `harlequin "md:" --md_saas`.\n\n### Viewing the Schema of your Database\n\nWhen Harlequin is open, you can view the schema of your DuckDB database in the left sidebar. You can use your mouse or the arrow keys + enter to navigate the tree. The tree shows schemas, tables/views and their types, and columns and their types.\n\n### Editing a Query\n\nThe main query editor is a full-featured text editor, with features including syntax highlighting, auto-formatting with <kbd>f4</kbd>, text selection, copy/paste, and more. \n\n> **Tip:**\n>\n> Some Linux users may need to apt-install `xclip` or `xsel` to enable copying and pasting using the system clipboard.\n\nYou can save the query currently in the editor with <kbd>ctrl + s</kbd>. You can open a query in any text or .sql file with <kbd>ctrl + o</kbd>.\n\n### Running a Query and Viewing Results\n\nTo run a query press <kbd>ctrl + enter</kbd>. Not all terminals support this key combination, so you can also use <kbd>ctrl + j</kbd>, or click the `RUN QUERY` button in the (blue) footer.\n\nUp to 50k records will be loaded into the results pane below the query editor. When the focus is on the data pane, you can use your arrow keys or mouse to select different cells.\n\n### Exiting Harlequin\n\nPress <kbd>ctrl + q</kbd> to quit and return to your shell.\n\n## Contributing\n\nThanks for your interest in Harlequin! Harlequin is primarily maintained by [Ted Conbeer](https://github.com/tconbeer), but he welcomes all contributions and is looking for additional maintainers!\n\n### Providing Feedback\n\nWe\'d love to hear from you! [Open an Issue](https://github.com/tconbeer/harlequin/issues/new) to request new features, report bugs, or say hello.\n\n### Setting up Your Dev Environment and Running Tests\n\n1. Install Poetry v1.2 or higher if you don\'t have it already. You may also need or want pyenv, make, and gcc.\n1. Fork this repo, and then clone the fork into a directory (let\'s call it `harlequin`), then `cd harlequin`.\n1. Use `poetry install --sync` to install the project (editable) and its dependencies (including all test and dev dependencies) into a new virtual env.\n1. Use `poetry shell` to spawn a subshell.\n1. Type `make` to run all tests and linters, or run `pytest`, `black .`, `ruff . --fix`, and `mypy` individually.\n\n### Opening PRs\n\n1. PRs should be motivated by an open issue. If there isn\'t already an issue describing the feature or bug, [open one](https://github.com/tconbeer/harlequin/issues/new). Do this before you write code, so you don\'t waste time on something that won\'t get merged.\n2. Ideally new features and bug fixes would be tested, to prevent future regressions. Textual provides a test harness that we use to test features of Harlequin. You can find some examples in the `tests` directory of this project. Please include a test in your PR, but if you can\'t figure it out, open a PR to ask for help.\n2. Open a PR from your fork to the `main` branch of `tconbeer/harlequin`. In the PR description, link to the open issue, and then write a few sentences about **why** you wrote the code you did: explain your design, etc.\n3. Ted may ask you to make changes, or he may make them for you. Don\'t take this the wrong way -- he values your contributions, but he knows this isn\'t your job, either, so if it\'s faster for him, he may push a commit to your branch or create a new branch from your commits.\n',
    'author': 'Ted Conbeer',
    'author_email': 'tconbeer@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://harlequin.sh',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
