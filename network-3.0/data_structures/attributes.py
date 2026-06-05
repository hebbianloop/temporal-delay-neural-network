from . import attribute_types


class Attributes:
    """class for storing attributes"""

    def __init__(self):

        self._attributes = []
        self._hasNumericAttributes = False
        self._hasNominalAttributes = False
        self._hasBoolAttributes = False

    def add(self, attribute):
        """
        adds an attribute to the object
        :type attribute: NumericAttribute | NominalAttribute"""

        self._attributes.append(attribute)
        self._hasBoolAttributes = True

    def __getitem__(self, item):
        """
        :type item: int | str
        :rtype : NumericAttribute | NominalAttribute | BoolAttribute | int
        """

        if isinstance(item, int):
            return self._attributes[item]

        elif isinstance(item, str):
            count = 0
            for x in self._attributes:
                if x.name == item:
                    return count
                else:
                    count += 1

    @property
    def has_nominal_attributes(self):
        """
        Checks if there are any nominal attributes
        :rtype : bool
        """

        return self._hasNominalAttributes

    @property
    def has_numeric_attributes(self):
        """
        Checks if there are any numeric attributes
        :rtype : bool
        """

        return self._hasNumericAttributes

    @property
    def has_bool_attributes(self):
        """
        checks if there are any Boolean attributes
        :rtype: bool
        """

        return self._hasBoolAttributes

    def index(self, name):
        """
        :type name: str
        :rtype : int
        """

        count = 0
        for x in self._attributes:
            if x is name:
                return count
            else:
                count += 1

    def __len__(self):
        """

        :rtype : int
        """

        return len(self._attributes)

    def parse(self, scanner):
        """creates an attribute from input and adds it to the object
        :type scanner: list
        """

        attrib = attribute_types.attribute_factory(scanner)
        self.add(attrib)

    def __str__(self):
        """

        :rtype : str
        """

        return '\n'.join(str(x) for x in self._attributes)
