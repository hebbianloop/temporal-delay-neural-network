__author__ = 'James'

from . import attributes
from . import example
from . import examples


class Data:
    """A class for storing examples for machine-learning methods."""

    def __init__(self, filename=None, attributes_=None, examples_=None):
        """
        Reads the attribute information and the training examples from the specified file.
        :type filename: str
        """
        self._speed = None
        self._filename = filename
        self._attributes = attributes_
        if self._attributes is None:
            self._attributes = attributes.Attributes()
        self._examples = examples_
        if self._examples is None:
            self._examples = examples.Examples(self._attributes)
        self._name = ''
        self._load()

    def attribute_value(self, item):
        """
        :type item: tuple
        :rtype : str
        """

        return self._attributes[item[0]][item[1]]

    def add(self, value):
        """Adds the specified example to this data set.
        or
        Adds the examples of the specified data set to this data set.
        :type value: Example | DataSet
        """

        if isinstance(value, example.Example):
            self._examples.add(value)
        if isinstance(value, Data):
            for ex in value.examples:
                self._examples.add(ex)

    @property
    def speed(self):
        """gives the data time increment"""
        return self._speed

    @speed.setter
    def speed(self, item):
        self._speed = item

    @property
    def attributes(self):
        """

        :rtype : Attributes
        """

        return self._attributes

    @property
    def examples(self):
        """

        :rtype : Examples
        """

        return self._examples

    @property
    def has_bool_attributes(self):
        """
        :rtype : bool
        """

        return self._attributes.has_bool_attributes

    def _load(self):
        """Loads examples from the specified file.
        Does some checking by reading the attributes information from the file,
        but presently, does not compare attributes information to make sure
        they're compatible."""

        if self._filename is not None:
            _file = open(self._filename)
            data_set = []
            for line in _file:
                if line != '\n':
                    data_set.append(line.rstrip().split(' '))
            _file.close()
            self._parse(data_set)

    def _parse(self, data_set):
        """
        Parses the header for a data set.
        :type data_set: list
        """

        for line in data_set:
            if line[0] == '@dataset':
                self._name = line[1]
            elif line[0] == '@speed':
                self._speed = int(line[1])
            elif line[0] == '@attribute':
                self._attributes.parse(line[1:])
            elif line[0] == '@examples':
                self._examples = examples.Examples(self._attributes)
            else:
                self._examples.parse(line)

    def __str__(self):

        return '@dataset ' + self._name + '\n\n' + '@speed ' + str(self._speed) + '\n\n' + str(
            self._attributes) + '\n\n' + str(self._examples) if self._examples is not None else 'No examples'

    def __len__(self):
        return len(self.examples)
