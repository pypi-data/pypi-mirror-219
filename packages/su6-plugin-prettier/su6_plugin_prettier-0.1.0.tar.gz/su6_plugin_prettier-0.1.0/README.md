# su6-plugin-prettier

Plugin for [su6](https://github.com/trialandsuccess/su6) that adds `prettier.io` functionality.

## Installation
```bash
pip install su6-plugin-prettier
# or
pip install su6[prettier]
```

## Usage

```bash
# optionally, if prettier isn't installed yet:
su6 install-prettier

su6 prettier # to check
su6 prettier --fix # to change files
```

### pyproject.toml
(all keys are optional, and also usable as flags to `prettier` (e.g. `--target ./path/to/files`))
```toml
[tool.su6.prettier]
target = "./path/to/js/files"
node_modules = "path/to/node_modules"
```

## License

`su6-plugin-prettier` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
