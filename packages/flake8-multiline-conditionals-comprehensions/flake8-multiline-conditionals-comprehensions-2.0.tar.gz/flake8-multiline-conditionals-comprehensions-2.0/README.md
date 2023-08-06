# flake8-multiline-conditionals-comprehensions

[![Build Status](https://github.com/atollk/flake8-multiline-conditionals-comprehensions/workflows/tox/badge.svg)](https://github.com/atollk/flake8-multiline-conditionals-comprehensions/actions)
[![Build Status](https://github.com/atollk/flake8-multiline-conditionals-comprehensions/workflows/pylint/badge.svg)](https://github.com/atollk/flake8-multiline-conditionals-comprehensions/actions)
[![Build Status](https://github.com/atollk/flake8-multiline-conditionals-comprehensions/workflows/black/badge.svg)](https://github.com/atollk/flake8-multiline-conditionals-comprehensions/actions)
[![Build Status](https://github.com/atollk/flake8-multiline-conditionals-comprehensions/workflows/flake8/badge.svg)](https://github.com/atollk/flake8-multiline-conditionals-comprehensions/actions)


flake8 plugin that works on conditional expressions and comprehension 
expressions to enforce each segment to be put on a new line.

## Contents
  * [Options](#options)
  * [Comprehension Errors](#comprehension-errors)
  * [Condition Errors](#condition-errors)

## Options
The flag `--select_mcc2` can be used to select the set of errors
to include. By default, the active errors are MCC200, MCC201, MCC202,
MCC220, MCC221, MCC223.


## Comprehension Errors

### MCC200

A comprehension expression should place each of its generators on a 
separate line.

```python
# Bad
[x+y for x in range(10) for y in range(10)]

# Good
[
    x + y
    for x in range(10)
    for y in range(10)
]
```


### MCC201

A multiline comprehension expression should place each of its segments
(map, generator, filter) on a separate line.

```python
# Bad
[x+y for x in range(10) 
for y in range(10) if x+y > 5]

# Good
[
    x + y
    for x in range(10)
    for y in range(10)
    if x + y > 5
]
```


### MCC202

A comprehension expression should not contain multiple filters.

```python
# Bad
[x for x in range(10) if x % 2 == 0 if x % 3 == 0]

# Good
[x for x in range(10) if x % 2 == x % 3 == 0]
```

### MCC203

A comprehension expression should not span over multiple lines.

```python
# Bad
[x + y 
for x in range(10) ]

# Good
[x+y for x in range(10)]
```

### MCC204

A comprehension expression should span over multiple lines.

```python
# Bad
[x for x in range(10)]

# Good
[x 
for x in range(10)]
```



## Condition Errors

### MCC220

A multiline conditional expression should place each of its segments
on a separate line.

```python
# Bad
1 
if something() else 0

# Good
1
if something()
else 0
```


### MCC221

A conditional expression used for assignment should be surrounded by
parantheses.

```python
# Bad
a = 1 if something() else 0

# Good
a = (1 if something() else 0)
```


### MCC222

A conditional expression should not contain further conditional
expressions.

```python
# Bad
1 if x > 0 else -1 if x < 0 else 0

# Good
if x > 0:
    return 1
elif x < 0:
    return -1
else:
    return 0
```


### MCC223

A conditional expression should not span over multiple lines.

```python
# Bad
1
if something()
else 0

# Good
1 if something() else 0
```


### MCC224

A conditional expression should span over multiple lines.

```python
# Bad
1 if something() else 0

# Good
1
if something()
else 0
```


### MCC225

Conditional expressions should not be used.
