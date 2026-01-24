import utime

def test_velocidad():
    inicio = utime.ticks_us() # Tiempo inicial
    
    # Tarea: Sumar 1 millón de veces
    contador = 0
    for i in range(1000000):
        contador += 1
        
    fin = utime.ticks_us() # Tiempo final
    
    duracion = utime.ticks_diff(fin, inicio)
    print(f"Resultado: {contador}")
    print(f"MicroPython tardó: {duracion} microsegundos")

test_velocidad()
