# finance-cli - CLI Python database tool

## Package Information
This CLI tool was built with Poetry and Typer.

TODO

## Usage
Snippet below will store current stock information for 'BRK-A' and 'BRK-B' in a csv and json file.
```bash
poetry run yFinance --json out.json --csv out.csv stock 'BRK-A' 'brk-b'
```


### Project Creation
This initial project was initialized with the following poetry command:
```bash
poetry new yFinance
```

### Edits to TOML file
TODO: Brief overview on toml files.

For the project to be configured as a Typer CLI app, the pyproject.toml needs to be updated.
```
[tool.poetry.scripts]
new yFinance = "new yFinance.main:app"
```

### Project Dependencies

```bash
poetry add "typer[all]"
poetry add "BeautifulSoup4[all]"
poetry add "pandas"
```


