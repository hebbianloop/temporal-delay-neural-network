def attribute_factory(scanner):
    """a function for building attributes
    :type scanner: list
    :rtype: NominalAttribute | NumericAttribute | BoolAttribute"""

    name = scanner[0]
    if scanner[1] == 'boolean':
        return BoolAttribute(name)


class Attribute:
    """Stores information for an attribute. An attribute has a name"""

    def __init__(self, name):
        """
        :type name: str
        """
        self._name = name

    @property
    def name(self):
        """Gets the name of this attribute.
        :rtype : str
        """

        return str(self._name)

    @name.setter
    def name(self, new_name):
        """
        Sets the name of this attribute to the specified name.
        :type new_name: str
        """

        self._name = new_name

    def __len__(self):
        """Gets the size of this attribute's domain."""

        pass

    @property
    def is_bool(self):
        """
        checks if the object is an instance of BoolAttribute
        :rtype: bool
        """
        return isinstance(self, BoolAttribute)


class BoolAttribute(Attribute):
    def __str__(self):
        """
        :rtype : str
        """
        return '@attribute ' + self._name + ' boolean'

    def __contains__(self, item):
        """

        :type item: int
        :rtype: bool
        """
        if item == +1 or item == 0:
            return True
        else:
            return False
