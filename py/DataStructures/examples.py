from . import example


class Examples:
    """Stores examples for data sets for machine learning."""

    def __init__(self, attributes, examples=None):
        """
        Given the attributes structure, processes the tokens in the scanner
        as an ArrayList. Numeric values are stored as is. Nominal values are stored
        as Doubles and are indices of the value in the attributes structure.
        :type attributes: Attributes.py
        """

        self._attributes = attributes
        self._examples = []
        if examples is not None:
            self._examples = examples

    def __iter__(self):
        """

        :rtype : collections.Iterable[Example]
        """

        for i in self._examples:
            yield i

    def __len__(self):
        """

        :rtype : int
        """

        return len(self._examples)

    def __getitem__(self, index):
        """
        :type index: int
        :rtype : Example
        """

        return self._examples[index]

    def parse(self, line):
        """creates an example from input and adds it to the object
        :param line: string
        """

        self.add(example.Example(self._attributes, line))

    def add(self, example):
        """
        adds an example.
        :type example: Example
        """

        self._examples.append(example)

    def __str__(self):
        """
        :rtype : str
        """
        return '@examples\n\n' + '\n'.join(str(ex) for ex in self._examples)
