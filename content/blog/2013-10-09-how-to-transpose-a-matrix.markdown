Title: How to transpose a matrix
Date: 2013-10-09 17:02
Category: blog
Tags: python, recipes, matrix

Python is such an expressive language. For instance, you can transpose a matrix in one line:

``` python
def transpose(matrix):
    return zip(*matrix)

>>> m = [(1, 2, 3), (4, 5, 6)]
>>> transpose(m)
[(1, 4), (2, 5), (3, 6)]
```
