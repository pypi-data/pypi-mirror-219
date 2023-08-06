# Hashable dict/list - Subclasses of list/dict with a custom hash function based on alternating addition and subtraction of element hashes - pure Python

## pip install hashlistdict 

#### Tested against Windows 10 / Python 3.10 / Anaconda 


The HashList and HashDict classes provide a custom hash function implementation for lists and dictionaries, respectively. 
The advantages and potential use cases for these classes are as follows:

### Customized Hashing: 

By overriding the **\_\_hash\_\_()** method, the classes allow you to define a custom hash function based on the elements of the list or 
the key-value pairs of the dictionary. This gives you more control over the hashing process and 
allows you to incorporate specific logic or considerations when computing the hash value.

### Hash-Based Data Structures: 

The custom hash function provided by these classes enables you to use instances of HashList and HashDict as keys in hash-based data structures such as 
dictionaries and sets. Since the hash value of an object is used to determine its position within a hash table, having a custom 
hash function can be useful when you want to ensure proper indexing and efficient retrieval of elements.

### Data Integrity and Immutability: 

Hashing is often used to verify data integrity or to create unique identifiers for objects. 
By providing a custom hash function, you can ensure that the hash value remains consistent and 
reliable for objects of HashList and HashDict. This can be valuable in scenarios where immutability 
and data integrity are important, such as caching, memoization, or cryptographic applications.


## HashList

```python
class HashList(builtins.list)

 |  HashList(iterable=(), /)
 |  
 |  A subclass of list that provides a custom hash function.
 |  
 |  This class overrides the __hash__() method to compute a hash value based on the elements of the list.
 |  The hash value is calculated by alternating between adding and subtracting the hash values of the elements.
 |  The method uses the `fla_tu()` function to flatten the list and its nested elements before computing the hash.
 |  
 |  Note:
 |      The order of the elements matters when computing the hash.
 |  
 |  Examples:
 |      l1 = HashList([1, 2, 3, 4, {1: 2, 3: 4}])
 |      print(hash(l1))
 |      # Output: -5103430572081493847
 |  
 |  Method resolution order:
 |      HashList
 |      builtins.list
 |      builtins.object
 
 ```
 
 ## HashDict

 ```python
 
 class HashDict(builtins.dict)
 
 |  A subclass of dict that provides a custom hash function.
 |  
 |  This class overrides the __hash__() method to compute a hash value based on the key-value pairs of the dictionary.
 |  The hash value is calculated by alternating between adding and subtracting the hash values of the keys and values.
 |  The method uses the `fla_tu()` function to flatten the dictionary and its nested elements before computing the hash.
 |  
 |  Note:
 |      The order of the key-value pairs matters when computing the hash.
 |  
 |  Examples:
 |      d1 = HashDict({1: 'a', 2: 'b', 3: 'c'})
 |      print(hash(d1))
 |      # Output: -5076628985615637757
 |  
 |  Method resolution order:
 |      HashDict
 |      builtins.dict
 |      builtins.object
 
 ```
 
 
 ### Examples 
 
```python

from hashlistdict import HashList, HashDict
l1 = HashList([1, 2, 3, 4, {1: 2, 3: 4}])

l2 = HashList([1, 2, 3, 4, {1: 2, 3: 4}])
l3 = HashList([1, 2, 4, 3])

print(hash(l1))
print(hash(l2))
print(l3)
di = {l1: "baba", l2: "bubu", l3: "bobo"}  # baba will be overwritten - same hash
print(di)

# {[1, 2, 3, 4, {1: 2, 3: 4}]: 'bubu', [1, 2, 4, 3]: 'bobo'}

import numpy as np

l11 = HashList(
    [
        {1: 2, 3: 4},
        1,
        2,
        3,
        4,
    ]
)

l22 = HashList([1, 2, 3, 4, {1: 2, 3: 4}])
l33 = HashList([1, 2, 4, 3, {3: 4, 1: 2}])
l44 = HashList([np.array([1, 2, 4, 3]), {3: 4, 1: 2}])
l55 = HashList([[1, 2, 4, 3], {3: 4, 1: 2}])

di2 = {l11: "baba", l22: "bubu", l33: "bobo", l44: "bibi", l55: "bebe"}

print(di2)

# [1, 2, 4, 3] {[1, 2, 3, 4, {1: 2, 3: 4}]: 'bubu', [1, 2, 4, 3]: 'bobo'} {[{1: 2, 3: 4}, 1, 2, 3, 4]: 'baba', [1, 2,
# 3, 4, {1: 2, 3: 4}]: 'bubu', [1, 2, 4, 3, {3: 4, 1: 2}]: 'bobo', [array([1, 2, 4, 3]), {3: 4, 1: 2}]: 'bibi', [[1,
# 2, 4, 3], {3: 4, 1: 2}]: 'bebe'}


# Test HashList with nested dictionaries
l1 = HashList([{1: 2, 3: 4}, 1, 2, 3, 4])
l2 = HashList([1, 2, 3, 4, {1: 2, 3: 4}])
l3 = HashList([1, 2, 4, 3, {3: 4, 1: 2}])

print(f'{hash(l1)=}')
print(f'{hash(l2)=}')
print(f'{hash(l3)=}')
# Output: <hash values>

# Test HashList with numpy arrays
l4 = HashList([np.array([1, 2, 4, 3]), {3: 4, 1: 2}])
l5 = HashList([[1, 2, 4, 3], {3: 4, 1: 2}])

print(f'{hash(l4)=}')
print(f'{hash(l5)=}')

# Test HashDict with nested dictionaries
d1 = HashDict({1: {2: 3}, 4: {5: 6}})
d2 = HashDict({1: {2: 3}, 4: {5: 6}})
d3 = HashDict({1: {4: 5}, 2: {3: 6}})

print(f'{hash(d1)=}')
print(f'{hash(d2)=}')
print(f'{hash(d3)=}')

# Output: <hash values>

# hash(l1)=-1436120659400041378
# hash(l2)=-5103430572081493847
# hash(l3)=3618454608618990865
# hash(l4)=3029580590484665753
# hash(l5)=1100456941032353086
# hash(d1)=-415071809182110355
# hash(d2)=-415071809182110355
# hash(d3)=4338543280270579718

```