# Tarea 00: DCCahuín :school_satchel:

## Consideraciones generales :octocat:

### Cosas implementadas y no implementadas :white_check_mark: :x:


* **Menu inicial**: En este se pregunta si desea iniciar sesion, registrarse o salir del programa.
    * **Iniciar sesion**: Implementado correctamente :heavy_check_mark:
    * **Registrarse**: Implementado correctamente :heavy_check_mark:
    * **Salir**: Implementado correctamente :heavy_check_mark:

**Una vez iniciada sesion, aparece un menu de inicio donde se puede acceder al menu de prograposts, al menu seguidores o cerrar sesión y volver al menu de inicio de sesión**

* **Menu de prograposts**:
    * **Publicar un prograpost**: Implementado correctamente :heavy_check_mark:
    * **Eliminar un prograpost**: Implementado correctamente :heavy_check_mark:
    * **Ver mis prograposts**: Implementado correctamente :heavy_check_mark:
    * **Ver mi muro**: Aquí aparecerán los prograposts de los usuarios que el usuario iniciado
    sigue, ordenados ascendiente o descendientemente :heavy_check_mark:
    * **Volver atras**: Opcion para volver al menu de inicio sin cerrar sesión :heavy_check_mark:

* **Menu de seguidores**:
    * **Seguir a alguien**: Implementado correctamente :heavy_check_mark:
    * **Dejar de seguir a alguien**: Implementado correctamente :heavy_check_mark:
    * **Volver atras**: Opcion para volver al menu de inicio sin cerrar sesión :heavy_check_mark:



## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además, hay una carpeta llamada **Menus** donde están ubicados los archivos:

1. ```ìnitial.py```
2. ```followers.py```
3. ```prograposts.py```

Para que el programa funcione, es requisito que estén creados los archivos ```posts.csv```, ```seguidores.csv``` y ```usuarios.csv``` dentro de la carpeta ```T00```, en el mismo nivel que ```main.py```

## Librerías :books:
### Librerías externas utilizadas

1. ```datetime```: Contiene a ```datetime``` utilizada para parsear inputs y almacenar fechas en formato ```yyyy/mm/dd``` (debe instalarse, una manera fácil es escribir ```pip3 install datetime``` en la terminal)


### Librerías propias

**Los siguientes modulos fueron creados dentro de la carpeta** ```Menus```:

1. ```initial``` que contiene la clase ```InitialMenu``` con las funciones del menu de inicio de sesión y el metodo ```interface``` que llama a las clases ```FollowersMenu``` y ```PrograPostsMenu```
2. ```followers``` que contiene la clase ```FollowersMenu``` con las funciones del menu de seguidores
3. ```prograposts``` que contiene la clase ```PrograPostsMenu```con las funciones del menu de prograposts


## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Debido a que habían hartas dudas respecto al flujo de menús, mi forma de implementarlo fue así:

![Grafico de flujo](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbkFbTWVudSBkZSByZWdpc3Ryby9pbmljaW8gZGUgc2VzaW9uXSAtLT4gQihNZW51IGRlIGluaWNpbylcbkIgLS0-IHxNZW51IHByb2dyYXBvc3RzfCBDW01lbnUgZGUgcHJvZ3JhcG9zdHNdXG5CIC0tPiB8TWVudSBkZSBzZWd1aWRvcmVzfCBEW01lbnUgZGUgc2VndWlkb3Jlc11cbkIgLS0-IHxTYWxpcnwgQVxuXG5DIC0tPiBDQShQdWJsaWNhciBhbGdvKVxuQyAtLT4gQ0IoRWxpbWluYXIgdW5hIHB1YmxpY2FjaW9uKVxuQyAtLT4gQ0MoVmVyIG1pcyBwcm9waWFzIHB1YmxpY2FjaW9uZXMpXG5DIC0tPiBDRChWZXIgcHVibGljYWNpb25lcyBkZSB1c3VhcmlvcyBxdWUgc2lnbylcbkMgLS0-IHxWb2x2ZXJ8QlxuXG5EIC0tPiBEQShTZWd1aXIgYSBhbGd1aWVuKVxuRCAtLT4gREIoRGVqYXIgZGUgc2VndWlyIGEgYWxndWllbilcbkQgLS0-IHxWb2x2ZXJ8QiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)
-------
