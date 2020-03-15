from abc import ABC, abstractmethod, abstractproperty


class Builder(ABC):

    @abstractproperty
    def product(self):
        pass

    @abstractmethod
    def type_command(self):
        pass

    @abstractmethod
    def indeks(self):
        pass

    @abstractmethod
    def type_line(self):
        pass

    @abstractmethod
    def side(self):
        pass

    @abstractmethod
    def district(self):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def angle(self):
        pass


class ConcreteBuilder(Builder):

    def __init__(self, list_val):
        self.reset()
        self.value = list_val

    def reset(self):
        self._product = Command()

    @property
    def product(self):

        product = self._product
        self.reset()
        return product

    def type_command(self):
        self._product.add(["Type", self.value[0]])

    def indeks(self):
        self._product.add(["Indeks", self.value[1]])

    def type_line(self):
        self._product.add(["Type_line", self.value[2]])

    def side(self):
        self._product.add(["Side", self.value[3]])

    def district(self):
        self._product.add(["District", self.value[4]])

    def list(self):
        self._product.add(["List", self.value[1]])

    def angle(self):
        self._product.add(["Angel", self.value[1]])


class Command:
    def __init__(self):
        self.parts = []

    def add(self, part):
        self.parts.append(part)

    def list_parts(self):
        return self.parts


class Director:
    def __init__(self):
        self._builder = None

    @property
    def builder(self):
        return self._builder

    @builder.setter
    def builder(self, builder):
        self._builder = builder

    def none_command(self):
        self.builder.type_command()
        self.builder.indeks()

    def standert_command(self):
        self.builder.type_command()
        self.builder.indeks()
        self.builder.type_line()
        self.builder.side()
        self.builder.district()

    def sort_task(self):
        self.builder.type_command()
        self.builder.indeks()
