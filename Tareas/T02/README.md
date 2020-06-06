# Tarea 02: DCCafé :coffee:



## Consideraciones generales :octocat:

La version entregada es funcional (es decir se puede jugar el juego, a pesar de que no esté completo).

### Cosas implementadas y no implementadas :white_check_mark: :x:

* **Ventana de Inicio**:
	* **Seguir jugando**: no implementado. Solo se puede usar el boton de Comenzar de nuevo (sin embargo, si despues de una ronda se guardan los resultados, Comenzar de nuevo usará los datos guardados).

	* **Comenzar de nuevo**: ocupa la funcionalidad de 'seguir jugando', o sea los datos guardados en los archivos .csv serán los que se ocupen.

* **Ventana de Juego**:
	* **Ventana de pre-ronda**: Funciona correctamente, luego de terminada la ronda si el jugador desde continuar, este entrará en la pre-ronda y solamente podrá comprar mesas y chefs (no podrá eliminarlos haciendo click). Al presionar el boton comenzar se entrará en la ronda.

	* **Ventana de ronda**: No implementé el mecanismo de bocadillos, por lo que los clientes no recibiran su bocadillo al impactar MiuEnzo con la mesa de manera visual, ni tampoco hay un mecanismo que calcule la calidad de los pedidos, sin embargo los clientes dejarán propina siempre que reciban bocadillo. Tampoco implementé las teclas especiales. Se puede pausar, pero al reanudar el juego los QTimers parten de 0 en lugar del momento en donde fueron pausados, por lo que si por ejemplo se pausa el juego a 1 segundo de que un Chef termine su bocadillo, al reanudar este empezará desde el segundo 0. Así mismo con todos los otros timers. Intenté solucionarlo pero al parecer era un problema frecuente de usuarios de Qt (el metodo stop pausa el reloj, y el único método de esa clase para reanudarlo es start(), el cual lo inicia desde 0) con QTimers y no tuve tiempo de inventar una solución.

	* **Ventana de post-ronda**: El resumen del juego funciona bien (a pesar de que el diseño sea horrible), y las opciones de continuar, guardar y salir funcionan correctamente.




## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```sprites``` en el mismo directorio que ```main.py```, ahí van las carpetas de sprites ```bocadillos```, ```chef```, ```clientes```, ```mapa```, ```mesero```. (```bonus```y ```otros``` no son necesarios)
2. ```datos.csv``` en el mismo directorio que main.py
3. ```mapa.csv``` en el mismo directorio de main.py


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```PyQt5``` con los modulos ```QtCore```, ```QtWidgets``` y ```QtGui```
2. ```sys``` y ```os```

### Librerías propias
Por otro lado, los módulos que fueron creados los siguientes:

1. ```utils_backend.py```: Contiene a ```DCCafe```
2. ```reloj.py```: contiene a ```Reloj```, la clase que administra todos los QTimers en el backend y ```ChefTimer``` que hereda de ```QObject```y es ocupada como temporizador para los chefs al cocinar.
3. ```backend.py``` procesos de lógica
4. ```inicio.py``` con la clase de la ventana inicial
5. ```resumen.py```con la clase de la ventana de post ronda
6. ```utils_front.py```con la clase ```DragLabel``` usada para poder hacer Drag and Drop, la clase ```Miuenzo```, la clase ```Chef```, la clase ```Mesa```, la clase ```Cliente``` y la clase incompleta ```Bocadillo```.
7. ```ventana_juego.py``` Ventana de la etapa de pre-ronda y ronda, con el QWidget del mapa, de la tienda y la ventana de estadisticas.
8. ```controller.py``` con la clase ```Controller.py```usada para conectar las señales y administrar los procesos de cambio de ventana
9. ```main.py```modulo ejecutable

### Errores cometidos :(
* LLegó un momento en que pasaba harto tiempo solamente en entender cómo implementé algunos procesos, y cuando ya iba más avanzado se volvió significativamente más complejo seguir implementando nuevos mecanismos. Intenté mantener el backend separado del frontend, pero no sabía si era buena práctica usar un montón de señales (pues había veces que el frontend debía mandar una señal al backend, luego este mandar otra al front end, y solo para un proceso como apretar un botón necesitaba 3 funciones distintas y las señales correspondientes, haciendo bastante confuso el orden de eventos al día siguiente cuando leo mi código), o tratar de reutilizar señales y funciones pero en ese caso se volvía mas compleja cada función y señal. También al haber tantas funciones se me olvidaba el orden en que ocurrían y debía estar un buen tiempo solo entendiendo en que orden ocurrían los eventos y qué señales iban con qué funciones. Todo tip/comentario respecto a como hacer este tipo de programas mas escalables es bienvenido (también no ayudó que no sabia ocupar Qt al iniciar la tarea, por lo que tener un modelo mental de cómo iba a programar el juego era dificil, pero quizas teniendo buenas prácticas en terminos de arquitectura hubiera ayudado bastante).
