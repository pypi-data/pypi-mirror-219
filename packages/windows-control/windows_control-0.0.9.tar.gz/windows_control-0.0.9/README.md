# Project Name

[windows_control_python](https://pypi.org/project/windows-control/) is a project to generate a Python module named `windows_control`, which provides some simple and efficient ways to do manipulations on Windows systems(Especially on Win10). It is written in Rust using [PyO3](https://crates.io/crates/pyo3).

## Installation

```bash
pip install windows_control
```

## Requirements

- Setting for final usage: Python (version 3.9.11 or later)
- Extra setting for development: Rust (version 1.68 or later)

## Examples

(TODO)

## Contributing

### TODO
windows module
add opencv support,after that pub a new version: https://www.perplexity.ai/search/bc8f7e79-b31a-4ba6-8a7f-f94e239f4c77?s=u

### Prerequisites

Before contributing to the project, you need to know about PyO3. You can follow the instructions:
- [PyO3 getting start](https://pyo3.rs/v0.19.0/getting_started);
- [PyO3 guide](https://pyo3.rs/v0.19.0/building_and_distribution#manual-builds);
- [How to use maturin to publish a python package](https://www.maturin.rs/tutorial.html);
- [PyO3 Define a Class/Struct/Enum](https://pyo3.rs/v0.19.0/class.html#attribute-access).

### Manual Development

1. Install the python package `maturin` by running `pip install maturin` in terminal.
2. Make sure there is a virtual env at your project root directory. You can do it by running `python -m venv .venv` in terminal---the name `.venv` is specified for `maturin`. NOTE: please restart your terminal after creating the virtual env.
3. To add new features (like new funcs or new modules), modify the `src/lib.rs` file.
4. After making changes, generate the Python module by running `maturin develop`. This command generates a library in `target/debug`.
5. On Windows, rename the generated library file `[your_module].dll` to `[your_module].pyd`.
6. Finally, to test the generated library, run `python test.py` in the root directory to verify that the newly added features work correctly in Python.

### Automatic Development

If you have [just](https://crates.io/crates/just) installed, run just to automatically generate and test the project. The justfile contains specific commands for this purpose.

### Publish
First, update the field `version` in file `pyproject.toml`.
Then, use `maturin publish`(in powershell,not git bash) to publish the package to PyPI(or just run `just pub` with [just](https://crates.io/crates/just)).When you see:
```bash
🚀 Uploading 2 packages
✨ Packages uploaded successfully
```
This means it's published successfully, and you can check it in [PyPi](https://pypi.org/project/windows-control/).

Finally, update section `Examples` in both `README.md`(this file) and `README_PUB.md`.


## License

This project is licensed under the MIT License.
