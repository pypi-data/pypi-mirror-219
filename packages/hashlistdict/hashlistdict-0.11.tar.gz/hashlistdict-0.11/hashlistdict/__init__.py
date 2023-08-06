from flatten_any_dict_iterable_or_whatsoever import fla_tu


class HashList(list):
    r"""A subclass of list that provides a custom hash function.

    This class overrides the __hash__() method to compute a hash value based on the elements of the list.
    The hash value is calculated by alternating between adding and subtracting the hash values of the elements.
    The method uses the `fla_tu()` function to flatten the list and its nested elements before computing the hash.

    Note:
        The order of the elements matters when computing the hash.

    Examples:
        l1 = HashList([1, 2, 3, 4, {1: 2, 3: 4}])
        print(hash(l1))
        # Output: -5103430572081493847

    """

    def __hash__(self):
        return hash(tuple(fla_tu(self)))+1



class HashDict(dict):
    """A subclass of dict that provides a custom hash function.

    This class overrides the __hash__() method to compute a hash value based on the key-value pairs of the dictionary.
    The hash value is calculated by alternating between adding and subtracting the hash values of the keys and values.
    The method uses the `fla_tu()` function to flatten the dictionary and its nested elements before computing the hash.

    Note:
        The order of the key-value pairs matters when computing the hash.

    Examples:
        d1 = HashDict({1: 'a', 2: 'b', 3: 'c'})
        print(hash(d1))
        # Output: -5076628985615637757

    """

    def __hash__(self):
        return hash(tuple(fla_tu(self))) + 2



