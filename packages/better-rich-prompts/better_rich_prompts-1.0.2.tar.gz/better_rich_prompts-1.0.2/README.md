[![Supported Python Versions](https://img.shields.io/pypi/pyversions/better-rich-prompts/1.0.0)](https://pypi.org/project/better-rich-prompts/) [![PyPI version](https://badge.fury.io/py/better-rich-prompts.svg)](https://badge.fury.io/py/better-rich-prompts)

[![Downloads](https://pepy.tech/badge/better-rich-prompts/month)](https://pepy.tech/project/better-rich-prompts)


[English readme](https://github.com/EwenLo/better-rich-prompts/blob/master/README.md)

better-rich-prompts is a Python extension library for [Rich](https://github.com/Textualize/rich).

This [Library](https://rich.readthedocs.io/en/latest/) makes it easy to use lists and dictionaries as choices for `prompt.ask` .

## Compatibility
This library should work 
## Installing
```sh
python -m pip install better-rich-prompts
```

## Using List Prompt

### Example 1 - Using list of dictionaries
```python
from better_rich_prompts.prompt import ListPrompt

choices = [
    {"name": "english", "language_code": "en"},
    {"name": "spanish", "language_code": "es"},
    {"name":"french","language_code":"fr"},
]
ListPrompt.ask("Select a language", choices, choice_key="name")
```
![ListPrompt Example](https://raw.githubusercontent.com/EwenLo/better-rich-prompts/main/imgs/dict_prompt_ex1.png)

### Example 2 - Using list of strings
```python
from better_rich_prompts.prompt import ListPrompt

choices = ["en", "es", "fr"]
ListPrompt.ask("Select a language", choices,default="en")
```
![ListPrompt Example](https://raw.githubusercontent.com/EwenLo/better-rich-prompts/main/imgs/list_prompt_ex2.png)

### Example 3 - Using list of custom objects
```python
from better_rich_prompts.prompt import ListPrompt

class Language:
    def __init__(self, name, code):
        self.name = name
        self.code = code


choices = [
    Language("english", "en"),
    Language("spanish", "es"),
    Language("french", "fr"),
]
ListPrompt.ask(
    "Select a language", choices, default="en", choice_key=lambda c: c.code
)
```
![ListPrompt Example](https://raw.githubusercontent.com/EwenLo/better-rich-prompts/main/imgs/list_prompt_ex3.png)

## Using Dict Prompt
```python
from better_rich_prompts.prompt import DictPrompt

choices = {"en":"english","es":"spanish","fr":"french"}
DictPrompt.ask("Select a language", choices)
```
![ListPrompt Example](https://raw.githubusercontent.com/EwenLo/better-rich-prompts/main/imgs/dict_prompt_ex1.png)
