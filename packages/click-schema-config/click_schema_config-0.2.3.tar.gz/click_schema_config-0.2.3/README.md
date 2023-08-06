# click-schema-config

click-schema-config allows you to add settings from a config file. Those will be automatically pulled into your program description without having to repeat them. Comments will be used as helper text for click.

# Is this project necessary?

After having built and used this, I am no longer convinced it is the best approach. I think [yt-dlp](https://github.com/yt-dlp/yt-dlp) and [parallel](https://www.gnu.org/software/parallel/) way of doing it might be more pertinent: Having profile files that specifies what options to enable.  
That said, codegen-ini solves the problem of packaging click's parameters and well-tying them, which has been a constant pain point for me.  
I will continue developping and using this tool for now, but it might not be the best way to go about this problem.

# Installation

```sh
poetry add click-schema-config
```

or, using pip

```
pip install click-schema-config
```

# Usage

Decorate your function with

```
@schema_from_inis(files=[...])
```

This will automatically infer the structure of your ini files and its documentation and add it to click.

Example of a config.default.ini:

```ini
initialized_to_none =

[test1]
; Wow, multilines
; Talk about eye candy
multiline_commented="value1"
typed: int = 2
inferred = True

[test2]
inline_commented = "value1" # This comment does not appear in the documentation

; This is a comment
after_paragraph = None
```

Note that you can type values directly. If a parameter appears without = succeding it, it becomes a required parameter.

**main**.py

```python
import pprint
import click
from click_schema_config import schema_from_inis


@click.command()
@schema_from_inis(files=["config.default.ini"])
def main(**kwargs):
    pprint.pprint(kwargs)

if __name__ == "__main__":
    main()
```

This will result in:

```sh
python __main__.py --help

Usage: __main__.py [OPTIONS]

Options:
  --initialized_to_none TEXT
  --test1.multiline_commented TEXT
                                  Wow, multilines
                                  Talk about eye candy  [default: value1]
  --test1.typed INTEGER            [default: 2]
  --test1.inferred / --no-test1.inferred
                                   [default: test1.inferred]
  --test2.inline_commented TEXT    [default: value1]
  --test2.after_paragraph TEXT    This is a comment
  --help                          Show this message and exit.
```

and

```sh
python __main__.py

{'initialized_to_none': None,
 'required_parameter_overriden': 'not required',
 'test1__inferred': True,
 'test1__multiline_commented': 'value1',
 'test1__typed': 2,
 'test2__after_paragraph': None,
 'test2__inline_commented': 'value1'}
```

You can of course override using the options:

```sh
python main.py --test2.inline_commented "HEY"

{'initialized_to_none': None,
 'required_parameter_overriden': 'not required',
 'test1__inferred': True,
 'test1__multiline_commented': 'value1',
 'test1__typed': 2,
 'test2__after_paragraph': None,
 'test2__inline_commented': 'HEY'}
```

# Rationale

Having setting files allow for separation of concerns and for users to know what they are expected to tweak and modify. This library is here to provide schema specifications of settings.

# Codegen-ini

This library also comes with the `codegen-ini` tool that allows you to have well-typed click dictionaries.
For instance, in the following code:

```py
@click.command()
@schema_from_inis(files=["config.default.ini"])
def main(**kwargs):
    pprint.pprint(kwargs)
```

It is unclear what keywords are present in kwargs, and what can be accessed. This makes for uncoupled code where changing the configuration leads to bugs and undefined variables.
To solve this, we can use codegen-ini to generate a pydantic class for us

codegen.yaml

```yaml
schemas:
  MyClass: "./config.default.ini"
```

and run it

`codegen-ini`

The following code will be generated in ./generated/MyClass.py:

```py
from pydantic import BaseModel


class MyClass(BaseModel):
    initialized_to_none: None = None
    required_parameter_overriden: str
    required_parameter: int

    """
    Wow, multilines
    Talk about eye candy
    """
    test1__multiline_commented: str = "value1"

    test1__typed: int = 2
    test1__inferred: bool = True
    test2__inline_commented: str = "value1"

    """
    This is a comment
    """
    test2__after_paragraph: None = None


class MyClassPartial(BaseModel):
    initialized_to_none: None | None = None
    required_parameter_overriden: str | None = None
    required_parameter: int | None = None

    """
    Wow, multilines
    Talk about eye candy
    """
    test1__multiline_commented: str | None = None

    test1__typed: int | None = None
    test1__inferred: bool | None = None
    test2__inline_commented: str | None = None

    """
    This is a comment
    """
    test2__after_paragraph: None | None = None
```

Which you can use to type your passed config:

```py
from generated.codegen_ini import MyClass
def main(**kwargs):
    config = MyClass(**kwargs)
    print(config.test1__multiline_commented) # Well typed
```

# TODO

- [ ] Integration with click types, like click.choices and click.intrange
- [ ] Test suite
- [ ] Preserve section structure in codegen-ini's generated classes?
