![hestia-practice](https://github.com/Amine-Chakhchoukh/hestia-practice/actions/workflows/pythonpackage.yml/badge.svg)
[![codecov](https://codecov.io/gh/Amine-Chakhchoukh/hestia-practice/branch/main/graph/badge.svg?token=1P2LQKKPE1)](https://codecov.io/gh/Amine-Chakhchoukh/hestia-practice)

# Hestia technical assessment
Hestia's Tech Task

## The task

A python script that takes a sparsely populated dataframe and outputs a more condensed one.
In more detail: the input file had one data node per row, and the aim is to combine related data nodes into rows for ease of reading/usage.

## Chosen approach

- I decided to use the power of pandas and use a pandas.merge for this task.
- Tests are done using pytest.

### Notes

- With pandas.merge one needs to be careful with the order of the columns, when doing many consecutive merges.
- ~~As I timeboxed my work (still going over the recommended 2h!) I didn't have a chance to run the test using Github Actions and get the coverage. I run my tests locally and they all passed.~~ (now running)

## Improvements

A few things come to mind here:

- Another approach to using pandas.merge is using dictionaries as follows:
  - every row can be thought of as its own dictionary (the keys being the column names and the dictionary values are the entries in the row).
  - loop through the list of dictionaries matching certain keys together. When a row is merged with another, the corresponding dictionary is removed from the list.
 
The above approach is simple enough and has the advantage of not worrying about the merge order. One disadvantage I suspect is time of execution. Testing how long this would take in practice would be helpful as a comparison.

- ~~Adding coverage and having tests run when changes are pushed using Github Actions.~~ (now running)
