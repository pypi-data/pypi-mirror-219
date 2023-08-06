
<p align="center">
    <img src="https://github.com/Textualize/trogon/assets/554369/f4751783-c322-4143-a6c1-d8c564d4e38f" alt="A picture of a trogon (bird) sitting on a laptop" width="300" align="center">
</p>
    
[![Discord](https://img.shields.io/discord/1026214085173461072)](https://discord.gg/Enf6Z3qhVr)

---

This is a fork of Trogon that introduces these features:

- refactor to make click optional
- remove support for custom click types `IntRange`, `FloatRange`
- support for manually constructing schemas
- support for argparse
- support for typer
- add examples for yapx, myke, and sys.argv
- support ommission of hidden parameters and subcommands from the TUI
- support the redaction of sensitive "secret" values
- support for showing required prompts as read-only
- positional arguments come before keyword arguments in the generated command
- ability to join list arguments values like this: `-x 1 -x 2 -x 3` (default), or like this: `-x 1 2 3`
- vim-friendly keybindings

I was motivated to create this fork so I could integrate Trogon into my Python CLI library [Yapx](https://www.f2dv.com/code/r/yapx/i/).

---

# Trogon

Auto-generate friendly terminal user interfaces for command line apps.


<details>  
  <summary> 🎬 Video demonstration </summary>

&nbsp;
    
A quick tour of a Trogon app applied to [sqlite-utils](https://github.com/simonw/sqlite-utils).

https://github.com/Textualize/trogon/assets/554369/c9e5dabb-5624-45cb-8612-f6ecfde70362

</details>


Trogon works with the popular Python libraries [Argparse](https://docs.python.org/3/library/argparse.html), [Click](https://click.palletsprojects.com/), [Typer](https://github.com/tiangolo/typer), [Yapx](https://www.f2dv.com/code/r/yapx/i/), and [myke](https://www.f2dv.com/code/r/myke/i/), and will support other libraries and languages in the future. You can also manually build your own TUI schema and use it however you like, even in conjunction with `sys.argv`. See the `examples/` directory for examples of each.

## How it works

Trogon inspects your (command line) app and extracts a *schema* which describes the options / switches / help etc.
It then uses that information to build a [Textual](https://github.com/textualize/textual) UI you can use to edit and run the command. 

Ultimately we would like to formalize this schema and a protocol to extract or expose it from apps.
This which would allow Trogon to build TUIs for any CLI app, regardless of how it was built.
If you are familiar with Swagger, think Swagger for CLIs.

## Screenshots

<table>

<tr>
<td>
<img width="100%" alt="Screenshot 2023-05-20 at 12 07 31" src="https://github.com/Textualize/trogon/assets/554369/009cf3f2-f0c4-464b-bd74-60e303864443">
</td>

<td>
<img width="100%" alt="Screenshot 2023-05-20 at 12 08 21" src="https://github.com/Textualize/trogon/assets/554369/b1039ee6-4ba6-4123-b0dd-aa7b2341672f">
</td>
</tr>

<tr>

<td>
<img width="100%" alt="Screenshot 2023-05-20 at 12 08 53" src="https://github.com/Textualize/trogon/assets/554369/c0a42277-e946-4bef-b0d0-3fa87e4ab55b">
</td>

<td>
<img width="100%" alt="Screenshot 2023-05-20 at 12 09 47" src="https://github.com/Textualize/trogon/assets/554369/55477f6c-e6b8-49b6-85c1-b01bee006c8e">
</td>

</tr>

</table>

## Why?

Command line apps reward repeated use, but they lack in *discoverability*.
If you don't use a CLI app frequently, or there are too many options to commit to memory, a Trogon TUI interface can help you (re)discover options and switches.

## What does the name mean?

This project started life as a [Textual](https://github.com/Textualize/textual) experiment, which we have been giving give bird's names to.
A [Trogon](https://www.willmcgugan.com/blog/photography/post/costa-rica-trip-report-2017/#bird) is a beautiful bird I was lucky enough to photograph in 2017.

See also [Frogmouth](https://github.com/Textualize/frogmouth), a Markdown browser for the terminal.

## Roadmap

Trogon is usable now. It is only 2 lines (!) of code to add to an existing project.

It is still in an early stage of development, and we have lots of improvements planned for it.

## Installing

Trogon may be installed with PyPI.

```bash
pip install trogon
```

## Quickstart

### Click

1. Import `from trogon.click import tui`
2. Add the `@tui` decorator above your click app. e.g.
    ```python
    @tui()
    @click.group(...)
    def cli():
        ...
    ```
3. Your click app will have a new `tui` command available.

### Argparse

1. Import `from trogon.argparse import add_tui_argument`
      or, `from trogon.argparse import add_tui_command`
2. Add the TUI argument/command to your argparse parser. e.g.
    ```python
    parser = argparse.ArgumentParser()

    # add tui argument (my-cli --tui)
    add_tui_argument(parser)
    # and/or, add tui command (my-cli tui)
    add_tui_command(parser)
    ```
3. Your argparse parser will have a new parameter `--tui` and/or a new command `tui`.

See also the `examples` folder for example apps.

## Custom command name and custom help

By default the command added will be called `tui` and the help text for it will be `Open Textual TUI.`

You can customize one or both of these using the `help=` and `command=` parameters.

### Click

```python
@tui(command="ui", help="Open terminal UI")
@click.group(...)
def cli():
    ...
```

### Argparse

```python
parser = argparse.ArgumentParser()

# add tui argument (my-cli --tui)
add_tui_argument(parser, option_strings=["--ui"], help="Open terminal UI")
# and/or, add tui command (my-cli tui)
add_tui_command(parser, command="ui", help="Open terminal UI")
```

## Follow this project

If this app interests you, you may want to join the Textual [Discord server](https://discord.gg/Enf6Z3qhVr) where you can talk to Textual developers / community.
