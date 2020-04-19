# Tarea 1: DCCriaturas Fantasticass :school_satchel:


## Consideraciones generales
* El programa cumple con todas las funcionalidades propuestas en el enunciado, sin ningun bonus.
* No niego la presencia de alguno que otro bug, he tratado de encontrar y solucionar todos los que pude, pero son cosas que pasan :sleep:


### Cosas implementadas y no implementadas

* **Menus**
  * **Menu de inicio** :heavy_check_mark:
    * En el menu de inicio se pregunta si se desea cargar usuario existente, registrar nuevo usuario o
    salir y terminar el programa. Todas las opciones cumplen con los requisitos del enunciado.
  * **Menu de acciones**
    * **Menu de cuidar DCCriaturas**:
      * Se puede alimentar, recuperar y sanar una dccriatura, ademas de ocupar la habilidad especial, cumpliendo cada funcionalidad con los requisitos del enunciado.
    * **Menu DCC**:
      * Se puede adoptar una dccriatura, comprar alimentos o ver el estado actual del magizoologo y sus dccriaturas. Tambien todo de acuerdo a lo propuesto en el enunciado.
    * **Pasar al dia siguiente**:
      * La opcion pasar al dia siguiente simula un nuevo dia de acuerdo a lo propuesto en el enunciado.

* **Entidades**
  * La entidad magizoologo y DCCriatura son clases abstractas con metodos normales y metodos abstractos de las cuales heredan los/las distintas dccriaturas y magizoologos respectivamente.
  * El dcc es una clase que contiene las funciones que realiza el DCC. Esta no se instancia, es decir es estatica.

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```criaturas.csv``` en el mismo directorio que main.py
2. ```magizoologos.csv``` en el mismo directorio que main.py


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```random```: ```randint() / choice()```
2. ```abc```: ```ABC / abstractmethod```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```dcc.py```: Contiene a ```DCC```
2. ```dccriaturas.py```: Contiene la clases abstracta ```DCCriatura``` y las clases ```Erkling```, ```Niffler``` y ```Augurey``` que heredan de ella.
3. ```loginmenu.py``` Contiene la clase ```LoginMenu``` con las funcionalidades del menu de inicio de sesion
4. ```mainmenu.py``` Contiene a ```MainMenu``` con las funcionalidades del menu de acciones
5. ```parametros.py``` contiene todos los parametros del juego

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Un magizoologo sin licencia igual debe pagar multas, pues en el caso de que se le quite la multa al fiscalizarlo por no tener dinero para pagar no se especifica si queda exento de multas hasta recuperar la licencia. Esto se revisa en la issue ```#408```

* El enunciado estaba super detallado, por lo que no tuve que realizar más supuestos.

-------
