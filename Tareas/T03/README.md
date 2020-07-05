# Tarea 3: DCCuatro :flower_playing_cards:
##
##


## Consideraciones generales :octocat:

La tarea debiese cumplir con todo lo que pide el eunciado, si no se me pasó algo.

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Reglas DCCuatro: Hecha completa
* Networking: Hecha completa

* Interfaz: Hecha completa (no está tan bonita eso sí :c)

* Archivos: Los parametros van en archivos.json, sin embargo los path los calculo en server.py pues no le encontré sentido a poner a mano 30+ paths que siguen un patrón. El archivo generador_de_mazos.py lo ocupo tal cual para generar el mazo inicial de cartas.

## Ejecución :computer:

Para iniciar el servidor, se debe ejecutar el archivo ```main.py``` ubicado en ```T03/server```. Para iniciar el cliente se debe correr el mismo archivo ubicado en ```T03/client```.

Además se debe crear los siguientes archivos y directorios adicionales:
1. ```sprites/simple``` en ```server``` que contiene los sprites de las cartas
2. ```directorio``` en ```ubicación```

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```PyQt5``` con las funcionalidades del front end
2. ```json``` para leer archivos y mensajes en formato json
3.  ```threading``` para manejar las conexiones entre el cliente y el servidor sin entorpecer la UI y las conexiones con los demas clientes
4.  ```socket``` para establecer la conexion entre el servidor y los clientes
5.  ```random``` para manejar los eventos al azar en generador_de_mazos.py

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```game_engine.py```: Contiene a ```GameEngine```, con la logica interna y las reglas del juego DCCuatro
2. ```generador_de_mazos.py```: ```sacar_cartas```, función que nos entregaron para manejar la creación de cartas.
3. ```utils.py``` con la funcion ```json_hook``` para al leer json, los numeros sean interpretados como int y no str.
4. ```client.py``` contiene una subclase de QObject encargada de mandar y recibir mensajes al servidor, y enviar señales a la clase Logic
5. ```logic.py```: contiene la subclase de QObject ```Logic``` que recibe las señales de ```Client``` con los comandos mensajes del servidor y envía señales a las interfaces.
6. ```game.py``` con la clase GameWindow, donde se implementa todo lo gráfico del juego.
7. ```login.py``` con la parte gráfica de la ventana de inicio
8. ```room.py``` con la ventana de la sala de espera
9. ```server.py``` con la clase Server que recibe y envía mensajes a los clientes, encargandose de procesar las acciones y ocupa a la clase GameEngine para los procesos de lógica asociados a las reglas del juego.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Un supuesto que realicé es que si un jugador grita DCCuatro en su turno, este instantáneamente roba 4 cartas (si el grito era inválido, obviamente) y pasa de turno. Esto podría ser un problema en caso de que el jugador deba robar 6 o + cartas, pues puede gritar DCCuatro para robar menos.
2. Otro supuesto asociado a girtar DCCuatro es que siempre supuse que si un jugador A gritaba DCCuatro y un jugador B tenía 1 carta, este debía robarlas altiro (sin esperar a su turno) y me lo imaginé como que el servidor le enviaba las cartas (de lo contrario el jugador podría negarse a robar para siempre). No me queda claro si infringe la regla de que el juego no debe robar cartas por el jugador. Para el robo de cartas normal, ahí sí es siempre el jugador el que roba cartas, aun que no le quede otra opción.
3. Si 2 jugadores tienen 1 carta, en el caso que (1) un tercer jugador grite DCCuatro, solo uno de esos 2 jugadores robará cartas, y se debe volver a gritar DCCuatro para que el otro robe. Y en el caso que (2) ese tercer jugador también tenga 1 carta restante, al gritar DCCuatro él tendrá la prioridad y por lo tanto quedará registrado como que gritó DCCuatro para él, por lo que para que sus oponentes roben cartas debe volver a gritar DCCuatro.
4. En relación al envío de cartas, una forma simple de optimizar el envío de imágenes es que las cartas que sabemos que siempre serán iguales (las cartas boca abajo) se envíen una sola vez al comienzo del juego y el cliente las guarde en memoria para cada vez que deba ocuparlas, y así lo implementé.
#
#
## Comunicación cliente/servidor

la manera de comunicarse del cliente y el servidor esta basada en 2 tipos de mensajes, aquellos que son imágenes y aquellos que son "comandos".

Todos los mensajes parten con un byte que indica qué tipo de mensajes es, si ese byte es un número 1 entonces es una imagen, si es un 0 es un comando.

* Comandos: Están en formato json y tienen un key y un value. En caso de que sea un comando que no requiere values, se deja el value como None. Un ejemplo es cuando el cliente intenta ingresar a la sala de espera con un nombre, al momento de clickear en el botón "join" se envía el comando CHECK_USERNAME al servidor con el nombre como value, el cual realiza el proceso correspondiente y en caso de que el nombre de usuario sea válido, envía de vuelta el comando VALID_USERNAME al cliente, y este procede a la sala de espera. Como el cliente necesita saber si hay usuarios conectados antes que él para mostrarlos, el servidor manda como values una lista con los usuarios conectados.

* Imágenes: todo mensaje que sea una imágen tendrá un byte que represente el número 1 al comienzo. Luego, habrá un segundo byte, que le indicará al cliente a dónde debe ir la imagen (al pozo, a la mano o si es una carta boca abajo que debe almacenar en la memoria), seguido por el formato especificado en el enunciado para enviar imágenes. 
