import abc

class ParentClass(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def load(self, input):
        """Retrieve data from the input source and return an object."""
        return

    @abc.abstractmethod
    def save(self, output, data):
        """Save the data object to the output."""
        return

class Subclass(ParentClass):
    def load(self, input):
        """Retrieve data from the input source and return an object."""
        return

    def save(self, output, data):
        """Save the data object to the output."""
        return

if __name__ == '__main__':
    print 'Subclass:', issubclass(Subclass, ParentClass)
    print 'Instance:', isinstance(Subclass(), ParentClass)
