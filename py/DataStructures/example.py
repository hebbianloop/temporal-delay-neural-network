
class Example:
    """Stores an example for data sets for machine learning."""

    def __init__(self, attributes, scanner):
        """
        Constructs an Example from input. separating the weight, if it exists, and the class_label into properties of
        the example.
        :type attributes: Attributes.py
        """

        self._example = []
        self._attributes = attributes

        for ex in scanner:
            self._example.append(bool(int(ex)))

    @property
    def attributes(self):
        return self._attributes

    def __iter__(self):
        """

        :rtype : collections.Iterable[int|float]
        """

        for i in self._example:
            yield i

    def __getitem__(self, index):
        """
        :type index: int
        :rtype : int | float
        """

        return self._example[index]

    def __setitem__(self, index, value):
        """
        :type index: int
        :type value: int|float
        """
        self._example[index] = value

    def __len__(self):
        """

        :rtype : int
        """

        return len(self._example)

    def __str__(self):
        """

        :rtype : str
        """

        string = ''

        for i in range(len(self._example)):
            if self._attributes[i].is_bool:
                string += str(int(self._example[i])) + ' '
        return string
