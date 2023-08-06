# azure-openai-tr
[![pytest](https://github.com/ffreemt/azure-openai-tr/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/azure-openai-tr/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.10%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/azure_openai_tr.svg)](https://badge.fury.io/py/azure_openai_tr)

Translate via Azure Openai

## Install it

```shell
pip install azure-openai-tr
# pip install git+https://github.com/ffreemt/azure-openai-tr
# poetry add git+https://github.com/ffreemt/azure-openai-tr
# git clone https://github.com/ffreemt/azure-openai-tr && cd azure-openai-tr
```

## Use it

Copy `.env.example` to `.env` and edit `.env` accordingly
```
# .env, e.g.
OPENAI_API_BASE = https://dattw.openai.azure.com
OPENAI_API_KEY = ...
DEPLOYMENT_NAME = chat
```

or set those environ variables from the command line.

```python
from azure_openai_tr import azure_openai_tr

print(azure_openai_tr("test this and that")
# '测试这个和那个。'

print(azure_openai_tr("Hey ya", temperature=.2))
# 嘿，你好

print(azure_openai_tr("Hey ya", temperature=.8))
# 嗨啊

print(azure_openai_tr("Hey ya", temperature=.8))
# 嘿 ya

print(azure_openai_tr("test this and that", to_lang='German', temperature=.8))
# Teste dies und jenes.

print(azure_openai_tr("test this and that", to_lang='German', temperature=.8))
# Teste dies und das.

print(azure_openai_tr("test this and that", to_lang='German', temperature=.1))
# Teste dies und das.

print(azure_openai_tr("test this and that", to_lang='中文', temperature=.8, template='翻成 {to_lang}, 列出3个版本\n {text}'))
# 1. 测试这个和那个
# 2. 检验这个和那个
# 3. 试验这个和那个
```

Check source code for more details.