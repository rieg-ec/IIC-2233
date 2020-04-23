from functools import reduce
# En este archivo tendrás que completar las funciones entregadas.


def desencriptar(cliente_encriptado):
    # No modificar
    nombre_encriptado = list(cliente_encriptado[1])
    letras = list('consumir')
    numeros = [str(i) for i in range(1, 9)]
    clave = [list(i) for i in zip(letras, numeros)]
    for i in range(len(nombre_encriptado)):
        for elemento in clave:
            if nombre_encriptado[i] in elemento:
                if nombre_encriptado[i] == elemento[0]:
                    nombre_encriptado[i] = elemento[1]
                elif nombre_encriptado[i] == elemento[1]:
                    nombre_encriptado[i] = elemento[0]
    nombre_desencriptado = ''.join(nombre_encriptado)
    cliente_desencriptado = cliente_encriptado
    cliente_desencriptado[1] = nombre_desencriptado
    return cliente_desencriptado

def obtener_clientes(lista_clientes_encriptados):
    lista_desencriptada = map(lambda x: desencriptar(x),
                              lista_clientes_encriptados)
    return list(lista_desencriptada)


def categorizar(productos, categoria):
    prod_cat = filter(lambda x: x.categoria == categoria,
                      productos)

    return list(prod_cat)


def calcular_precio(productos):
    precio_total = reduce(lambda x, y: x + y.precio,
                          productos, 0)
    return precio_total


def generar_productos_disponibles(clientes):
    for cliente in clientes:
        for producto in cliente.carrito:
            if producto.disponible:
                yield (cliente, producto)
