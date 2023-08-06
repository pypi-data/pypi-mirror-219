# Pypdtools

Pypdtools is a Python package that extends the functionality of Pandas DataFrames by introducing the `PtDataFrame` class. `PtDataFrame` provides additional features and enhancements to work with DataFrames in a more convenient and flexible way.

## Features

- Asynchronous iteration support: `PtDataFrame` implements both synchronous and asynchronous iterators, allowing for efficient and convenient data processing in asynchronous contexts.
- Context manager support: `PtDataFrame` can be used as a context manager to easily access the encapsulated Pandas DataFrame.
- Concatenation and reduction: `PtDataFrame` supports concatenation of multiple instances and reduction of a list of `PtDataFrame` objects into a single instance.
- Column extraction: Easily extract a column as a list from a `PtDataFrame`.

**Docs:** <a href="https://msbar.github.io/pypdtools" target="_blank">https://msbar.github.io/pypdtools</a>

**Source code:** <a href="https://github.com/msbar/pypdtools" target="_blank">https://github.com/msbar/pypdtools</a>

## Installation

You can install pypdtools using pip:
```
pip install pypdtools
```

## Usage

Here's an example of how to use the `PtDataFrame` class:

```python
import pandas as pd
from pypdtools.core.dataframe import PtDataFrame

# Create a Pandas DataFrame
data = {
    "a": [1, 2, 3],
    "b": [4, 5, 6],
    "c": [7, 8, 9]
}
df = pd.DataFrame(data)

# Create a PtDataFrame from the Pandas DataFrame
pt_df = PtDataFrame(df)

# Async Iterate over rows
async for row in pt_df:
    print(row)

# Concatenate PtDataFrames
pt_df2 = PtDataFrame(df)
concatenated = pt_df + pt_df2

# Reduce a list of PtDataFrames
pt_df3 = PtDataFrame.reduce([pt_df, pt_df2])

# Extract a column as a list
col_values = pt_df.col_to_list("a")
print(col_values)
```
