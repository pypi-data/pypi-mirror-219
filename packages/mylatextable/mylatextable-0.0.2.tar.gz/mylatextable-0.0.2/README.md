# mylatextable

This package intends to make it easier to create LaTeX-formated tables from tabular data that is available in Python.

A typical use case would be

```
from mylatextable import MyLatexTable
header = [...] # Define header fields
table = MyLatexTable(header_fields=header, use_booktabs=True)
rows = .... # create a list of rows according to your logic
for row in rows:
    table.add_row(row)
print(table.get_latex()) # display LaTeX code
```



### Release
To release a new version, update the version number in pyproject.toml and enter the following commands.

```
python -m build .
python -m twine upload dist/*
```

This package is available at https://pypi.org/project/mylatextable/.