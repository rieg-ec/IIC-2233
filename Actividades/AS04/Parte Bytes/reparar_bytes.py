def reparar_imagen(ruta):
    # Completa esta función
    original = 'user_info.bmp'
    datos = bytes()
    with open(ruta, 'rb') as file:
        bytes_data = file.read()
        for i in range(0, len(bytes_data), 32):
            chunk = bytes_data[i:i+16]
            pertenecientes = chunk[1:16][::-1] if chunk[0] else chunk[1:16]
            datos += pertenecientes
        print(len(datos))
    with open(original, 'wb') as file:
        file.write(datos)

if __name__ == '__main__':
    try:
        reparar_imagen('imagen_danada.xyz')
        print("Contraseña reparada")
    except Exception as error:
        print(f'Error: {error}')
        print("No has podido obtener la información del Ayudante!")
