# pycones

[![PyPI Version][pypi-image]][pypi-url]

...

<!-- Badges: -->

[pypi-image]: https://img.shields.io/pypi/v/pycones
[pypi-url]: https://pypi.org/project/pycones


## basic utils

- flatten a list

```python
flatten([1, 2, [3, [4, 5]]])
# [1, 2, 3, 4, 5]
```

- join lists into a string

```python
list_join(list("abc"), list("def"), sep=",")
# "a,b,c,d,e,f"
```

- switch jupyter kernel into python or r

```python
nb_kernel_switch(notebook_path, kernel='python')
```
