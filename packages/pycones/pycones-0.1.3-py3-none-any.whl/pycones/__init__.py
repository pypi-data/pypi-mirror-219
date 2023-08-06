"""
The pycones package provides useful functions
"""
import json

__version__ = "0.1.3"


def flatten(lst):
    """
    flatten a list
    """
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def list_join(*args, sep=""):
    """
    join lists into a string
    """
    res = sep.join(flatten(args))
    return res


def nb_kernel_switch(notebook_path, kernel="python"):
    """
    switch jupyter kernel into python or r
    """
    assert notebook_path.endswith(".ipynb"), "please input a .ipynb file"
    kernel = kernel.lower()
    assert kernel in ["python", "r"], "please switch to python or r kernel"

    notebook = json.loads(open(notebook_path, "r").read())
    if kernel == "r":
        notebook["metadata"]["kernelspec"]["name"] = "ir"
        notebook["metadata"]["kernelspec"]["display_name"] = "R"
        notebook["metadata"]["kernelspec"]["language"] = "R"
        notebook["metadata"]["language_info"] = {
            "codemirror_mode": "r",
            "file_extension": ".r",
            "mimetype": "text/x-r-source",
            "name": "R",
            "pygments_lexer": "r",
        }
    elif kernel == "python":
        notebook["metadata"]["kernelspec"]["name"] = "python3"
        notebook["metadata"]["kernelspec"]["display_name"] = "Python 3 (ipykernel)"
        notebook["metadata"]["kernelspec"]["language"] = "python"
        notebook["metadata"]["language_info"] = {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
        }

    json.dump(notebook, notebook_path)
