# Strings by Ouroboros Coding
[![pypi version](https://img.shields.io/pypi/v/Strings-OC.svg)](https://pypi.org/project/Strings-OC) ![MIT License](https://img.shields.io/pypi/l/Strings-OC.svg)

Generic functions for dealing with and generating strings

## Requires
Strings-OC requires python 3.10 or higher

## Installation
```bash
pip install Strings-OC
```

## Functions

### bytes_human
Returns a human readable string using the number passed as a representation of bytes
```python
>>> from strings import bytes_human
>>>	bytes_human(1024)
'1.0KiB'
>>> bytes_human(1024*1024)
'1.0MiB'
>>> bytes_human(1024*1024*1024+1000000000)
'1.9GiB'
```

### digits
Returns only the digits, i.e. the numeric characters, in the given string as a new string. Be careful, as this does not return numbers, but number characters, and will strip out valid float/decimal characters
```python
>>> from strings import digits
>>> digits('1234abcd')
'1234'
>>> digits('a1b2c3d4')
'1234'
>>> digits('3.1415')
'31415'
>>> digits('1e+7')
'17'
```

### from_file
Returns the entire file as a string

```python
>>> from strings import from_file
>>> from_file('version.dat')
'1.0.1\n'
```

Assuming `version.dat` contained the following

```
1.0.1

```

If the file doesn't exist, `from_file` returns `None`. This can be changed by passing a second argument to be the default value.

```python
>>> from strings import from_file
>>> from_file('doesnotexist', '1.0.0')
'1.0.0'
```

### normalize
Returns, as well as possible, a normalized string converted from another string containing characters with special accents. It does this by finding special characters and converting them into their simpler, single character, versions. This is useful for things like automaticlaly generating urls, or for generating from unicode into ascii.
```python
>>> from strings import normalize
>>> normalize('Ȟěƚľỡ, Ẉợɽḷᶁ!')
'Hello, World!'
>>> normalize('ﬃǲǼĳ')
'ffiDAEij'
```

### random
Returns a random string based on set parameters.
```python
>>> from strings import random
>>> random()
'NQFsxVTi'
>>> random()
'KFCMjKQg'
>>> random()
'HJEvCjlA'
```
`random` can takes 3 optional parameters.
#### length
`length` represents the number of random characters you wish to return.
```python
>>> random(length = 10)
'PvIwnubCyN'
>>> random(length = 4)
'bGXE'
>>> random(16)
'WMLdawtSCEFeNtsg'
```
#### characters
`characters` represents the set of chars that are allowed in the string. There is no limit on this list, and no necessity the values be different. This allows for modifying the randomness if there are characters you want to make "more random"
```python
>>> random(8, 'AAAAa')
'AAAAAAAA'
>>> random(length = 8, characters = 'AAAaa')
'aAAAAAaA'
>>> random(characters = 'AAaaa', length = 8)
'aaaaAAaA'
```
`characters` can be set using special built in sets, and can be accessed by passing a list instead of a string
```python
>>> random(16, ['aZ'])
'KwDNSoFPlVVTxwhj'
>>> random(characters = ['az*', '10'])
'a003jsut'
>>> random(characters = ['0x'], length = 32)
'9ce511ab223cef1d65c400ce2e836759'
```

| name | characters |
| --- | --- |
| 0x | 0123456789abcdef |
| 0 | 01234567 |
| 10 | 0123456789 |
| az | abcdefghijklmnopqrstuvwxyz |
| az* | abcdefghijkmnopqrstuvwxyz |
| AZ | ABCDEFGHIJKLMNOPQRSTUVWXYZ |
| AZ* | ABCDEFGHJKLMNPQRSTUVWXYZ |
| aZ | abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ |
| aZ* | abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ |
| ! | !@#$%^&*-_+.? |
| !* | !@$%^*-_. |

\* sets denote removal of characters that might confuse, either systems or humans. &, #, etc for the former, and I, l, O, etc for the latter.
#### duplicates
By default `random` allows duplicate characters in a string, and doesn't see any issue with that. But it's possible you have an issue with it, and want a string made up completely of non-repeating characters. If so, set `duplicates` to `False`.
```python
>>> random(16, ['az'], False)
'ifaunxgtzbywkmpr'
>>> random(26, ['az'], False)
'rmqghwsayntkpizfbeldvcxoju'
>>> random(27, ['az'], False)
ValueError: Can not generate random string with no duplicates from the given characters "abcdefghijklmnopqrstuvwxyz" in random
```
### strtr
`strtr` is a partial copy of the [PHP functon](https://www.php.net/manual/en/function.strtr.php) of the same name. This version does not support the singular use of one $from, and one $to, but the same can be achieved by using a dict with a single key and value. The primary purpose of this function is to be the actual workhorse of the `normalize` function, but there's no reason other people can't make use of it.
```python
>>> from strings import strtr
>>> strtr('Hello, World!', {'World': 'Chris'})
'Hello, Chris!'
```

### to_bool
`to_bool` is useful for turning any string into a valid boolean. But will raise an exception if the value does not represent a bool as it sees it. First, it converts the string to lowercase, then it checks it against the following:
Valid `True` values contain '1', 'on', 't', 'true', 'y', 'yes', 'x'
Valid `False` values contain '0', 'f', 'false', 'n', 'no', 'off', ''
```python
>>> from strings import to_bool
>>> to_bool('true')
True
>>> to_bool('F')
False
>>> to_bool('2')
ValueError: "2" is not a valid boolean representation in to_bool
```

### to_file
Stores a string in a file, overwriting the existing contents, or creating the file if it didn't exist.
```python
>>> from strings import to_file
>>> to_file('version.dat', '1.1.0')
True
```
The `version.dat` file will now contain the following
```
1.1.0
```

### uuid_add_dashes
Used to add dashes "-" to a string representation of a UUID that has none.
```python
>>> from strings import uuid_add_dashes
>>> uuid_add_dashes('b22eb45ac98311eca05a80fa5b0d7c77')
'b22eb45a-c983-11ec-a05a-80fa5b0d7c77'
```

### uuid_strip_dashes
Used to strip dashes "-" from a string representation of a UUID that has them.
```python
>>> from strings import uuid_strip_dashes
>>> uuid_strip_dashes('b22eb45a-c983-11ec-a05a-80fa5b0d7c77')
'b22eb45ac98311eca05a80fa5b0d7c77'
```

### version_compare
Compares to version strings and returns if the first is less than (-1), equal to (0) or greater than (1) the second
```python
>>> from strings import version_compare
>>> version_compare('1.0.1', '1.0')
1
>>> version_compare('1.0.1', '1.0.1')
0
>>> version_compare('1.0.1', '1.1')
-1
```