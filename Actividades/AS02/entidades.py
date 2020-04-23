from copy import copy


class Producto:
    def __init__(self, id_, nombre, categoria, precio, disponible, descuento_oferta):
        self.id_ = id_
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.disponible = disponible
        self.descuento_oferta = descuento_oferta

    def __repr__(self):
        return self.nombre


class Cliente:
    def __init__(self, id_, nombre, carrito):
        self.id_ = id_
        self.nombre = nombre
        self.carrito = carrito


class IterableOfertones:
    def __init__(self, productos):
        self.productos = productos

    def __iter__(self):
        return IteradorOfertones(self.productos)


class IteradorOfertones:
    def __init__(self, iterable):
        self.iterable = sorted(copy(iterable), key=lambda x: x.descuento_oferta,
                               reverse=True)
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.n >= len(self.iterable):
            raise StopIteration()
        else:
            max_oferta = self.iterable[self.n]
            self.n += 1
            return max_oferta
