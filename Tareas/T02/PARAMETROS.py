
### MiuEnzo ###
VEL_MOVIMIENTO = 4
TIMER_INTERVAL = 20 # los FPS de movimiento seran 1000/TIMER_INTERVAL


### Ventana inicio ###
GM_VENTANA_INICIO = (0, 0, 700, 700)
GM_LOGO_DCCAFE_INICIO = (0, 0, 300, 200)


### Ventana de juego ###
GM_VENTANA_JUEGO = (100, 100, 800, 600)

### Ventana de mapa ###
BORDE_SUPERIOR_MAPA = 0.2 # posicion de las puertas relativas al tamano del mapa

## Ventana de tienda ###
PRECIO_CHEF = 300
PRECIO_MESA = 100

### Ventana de Resumen ###
GM_VENTANA_RESUMEN = (100, 100, 800, 600)


### Chef ###
PLATOS_INTERMEDIO = 4
PLATOS_EXPERTO = 10

### Reloj ###
RAPIDEZ_RELOJ = 0.05 # ponderador contra tiempo real -> para acelerar procesos,
                    # multiplicar por < 1

### Bocadillos ###
PRECIO_BOCADILLO = 100

### Clientes ###
LLEGADA_CLIENTES = 5000
PROPINA = PRECIO_BOCADILLO // 10

TIEMPO_ESPERA_APURADO = 3000 * RAPIDEZ_RELOJ
PROB_APURADO = 0.5

TIEMPO_ESPERA_RELAJADO = 5000 * RAPIDEZ_RELOJ

### DCCafe ###
DINERO_INICIAL = 2000
REPUTACION_INICIAL = 5
REPUTACION_TOTAL = 5
CHEFS_INICIALES = 3
MESAS_INICIALES = 4
CLIENTES_INICIALES = 6
