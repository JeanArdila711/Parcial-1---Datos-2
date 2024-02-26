from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def obtener_coordenadas(lugares_intermedios):
    geolocator = Nominatim(user_agent="my_geocoder")
    coordenadas = {}
    for lugar in lugares_intermedios:
        location = geolocator.geocode(lugar)
        coordenadas[lugar] = (location.latitude, location.longitude)
    return coordenadas

def construir_grafo(coordenadas, distancias, intermedios):
    grafo = {}
    lugares = list(coordenadas.keys())

    for origen in lugares:
        grafo[origen] = {}
        for destino in lugares:
            if origen != destino:
                distancia = distancias.get((origen, destino))
                if distancia:
                    grafo[origen][destino] = distancia
    
    # Agregar las distancias entre lugares intermedios
    for i in range(len(intermedios)):
        for j in range(i+1, len(intermedios)):
            origen = intermedios[i]
            destino = intermedios[j]
            distancia = distancias.get((origen, destino))
            if distancia:
                grafo[origen][destino] = distancia
                grafo[destino][origen] = distancia
    
    return grafo

def corregir_nombres(lugares, nombres_correctos):
    for i in range(len(lugares)):
        lugar = lugares[i]
        for nombre_correcto in nombres_correctos:
            if lugar.lower() == nombre_correcto.lower():
                lugares[i] = nombre_correcto
                break

def calcular_mejor_ruta(grafo, inicio, destino):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    visitados = set()
    while True:
        nodo_actual = min((nodo for nodo in distancias if nodo not in visitados), key=distancias.get, default=None)
        if nodo_actual is None:
            break
        visitados.add(nodo_actual)
        for vecino, peso in grafo[nodo_actual].items():
            if vecino not in visitados:
                nueva_distancia = distancias[nodo_actual] + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia

    return distancias[destino]

def calcular_ruta_optima(grafo, inicio, destino, intermedios, rutas_calculadas):
    if len(intermedios) == 0:
        return calcular_mejor_ruta(grafo, inicio, destino)
    
    # Verificar si la ruta ya ha sido calculada
    intermedios.sort()  # Ordenar los intermedios para garantizar una clave única
    ruta_actual = (inicio, destino, tuple(intermedios))
    if ruta_actual in rutas_calculadas:
        return rutas_calculadas[ruta_actual]

    mejor_distancia = float('inf')
    for i in range(len(intermedios)):
        nuevo_inicio = inicio
        nuevo_destino = intermedios[i]
        nuevos_intermedios = intermedios[:i] + intermedios[i+1:]
        distancia_inicio_a_intermedio = grafo[nuevo_inicio][nuevo_destino]
        distancia_intermedio_a_destino = calcular_ruta_optima(grafo, nuevo_destino, destino, nuevos_intermedios, rutas_calculadas)
        distancia_total = distancia_inicio_a_intermedio + distancia_intermedio_a_destino
        if distancia_total < mejor_distancia:
            mejor_distancia = distancia_total

    # Almacenar la ruta calculada
    rutas_calculadas[ruta_actual] = mejor_distancia
    return mejor_distancia

def main():
    inicio = input("Ingrese el punto de partida: ").strip().capitalize()
    destino = input("Ingrese el punto de llegada: ").strip().capitalize()
    intermedios = [lugar.strip().capitalize() for lugar in input("Ingrese los lugares intermedios separados por comas: ").split(',')]
    corregir_nombres(intermedios, ['Frankfurt', 'Viena', 'Praga', 'Berna', 'Amsterdam', 'Barcelona', 'Paris', 'Madrid', 'Bruselas', 'London', 'Venecia'])

    print("Lugares intermedios corregidos:", intermedios)

    # Obtener coordenadas de todos los lugares
    coordenadas = obtener_coordenadas([inicio, destino] + intermedios)

    # Calcular las distancias entre los lugares
    distancias = {}
    lugares = list(coordenadas.keys())
    for i in range(len(lugares)):
        for j in range(i + 1, len(lugares)):
            lugar1 = lugares[i]
            lugar2 = lugares[j]
            distancia = geodesic(coordenadas[lugar1], coordenadas[lugar2]).kilometers
            distancias[(lugar1, lugar2)] = distancia
            distancias[(lugar2, lugar1)] = distancia  # Considerar la distancia en ambas direcciones

    # Construir el grafo
    grafo = construir_grafo(coordenadas, distancias, intermedios)

    # Calcular la mejor ruta utilizando recursividad y memoización
    rutas_calculadas = {}
    mejor_distancia = calcular_ruta_optima(grafo, inicio, destino, intermedios, rutas_calculadas)

    if mejor_distancia != float('inf'):
        print(f"La mejor ruta desde {inicio} hasta {destino} pasando por {intermedios} es: {mejor_distancia} kilómetros")
    else:
        print("No se encontró ninguna ruta válida desde el punto de partida hasta el destino.")

main()
