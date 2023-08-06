# zshgpt

[![PyPI - Version](https://img.shields.io/pypi/v/zshgpt.svg)](https://pypi.org/project/zshgpt)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zshgpt.svg)](https://pypi.org/project/zshgpt)

-----

**Table of Contents**

- [About](#about)
- [Installation](#installation)
- [License](#license)

## About
Heavily inspired by the abandoned project [https://github.com/microsoft/Codex-CLI](https://github.com/microsoft/Codex-CLI)
Made into a oh-my-zsh plugin.

In your zsh console, type a question, starting with comment sign `#`, hit `ctrl+g` and get an answer.
```bash
# Who edited README.MD last according to git history?
```
ChatGPT will then answer with e.g.:
```bash
git log -1 --format="%an" README.md
```
Hit `enter` to execute or `ctrl+c` to deny.

If asked a question that will not resolve in a command, GPT is instructed to use `#`.

```bash
# Who was Norways first prime minister?
# Norway's first prime minister was Frederik Stang, serving from 1873 to 1880.
``` 

## Prerequisite
* Python >= 3.7
* Valid Openai API-key
    * make sure to save under `OPENAI_API_KEY` env.
    * `export OPENAI_API_KEY='sk-...'`

## Installation

```bash
pip install zshgpt
mkdir $ZSH_CUSTOM/plugins/zshgpt
curl https://raw.githubusercontent.com/AndersSteenNilsen/zshgpt/main/zsh_plugin/zsh_plugin.zsh -o $ZSH_CUSTOM/plugins/zshgpt/zshgpt.plugin.zsh
```
Then add zshgpt in your list of plugins in `~/.zshrc`

```
plugins(
    ...
    zshgpt
    ...
)
```

## License

`zshgpt` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
