import heapq

# 1. Definición del grafo (nodos y aristas con sus pesos) extraído de la imagen
grafo = {
    'A': {'G': 9, 'N': 5},
    'B': {'S': 4, 'I': 3, 'D': 5},
    'C': {'S': 2, 'N': 1, 'F': 8, 'E': 10, 'P': 21},
    'D': {'B': 5, 'Q': 7, 'O': 13, 'E': 2, 'T': 6},
    'E': {'C': 10, 'F': 12, 'D': 2, 'L': 7, 'T': 2},
    'F': {'I': 7, 'C': 8, 'E': 12},
    'G': {'A': 9},
    'H': {}, 
    'I': {'B': 3, 'F': 7},
    'J': {'T': 9},
    'K': {}, 
    'L': {'E': 7},
    'M': {}, 
    'N': {'A': 5, 'C': 1, 'Q': 4},
    'O': {'D': 13},
    'P': {'C': 21},
    'Q': {'N': 4, 'D': 7},
    'R': {}, 
    'S': {'B': 4, 'C': 2},
    'T': {'D': 6, 'E': 2, 'J': 9}
}

# 2. Definición de inventarios y pedidos
farmacias = {
    'B': {'Chicles', 'Antipsicóticos', 'Vendas'},
    'C': {'Supositorios', 'Aspirinas', 'Antitusivo'},
    'F': {'Chicles', 'Vendas', 'Supositorios', 'Antitusivo'},
    'T': {'Antipsicóticos', 'Aspirinas', 'Antitusivo'}
}

pedidos = {
    'Pedido 1': {'items': {'Antitusivo', 'Chicles'}, 'destino': 'T'},
    'Pedido 2': {'items': {'Supositorios', 'Vendas'}, 'destino': 'E'},
    'Pedido 3': {'items': {'Antipsicóticos', 'Aspirinas'}, 'destino': 'D'}
}

# Modificación de Dijkstra para guardar el camino (padres)
def dijkstra_path(grafo, origen):
    dist = {nodo: float("inf") for nodo in grafo}
    padre = {nodo: None for nodo in grafo}
    dist[origen] = 0
    cola = [(0, origen)]
    cerrados = set()
    
    while cola:
        d, u = heapq.heappop(cola)
        if u in cerrados:
            continue
        cerrados.add(u)
        for v, peso in grafo[u].items():
            if d + peso < dist[v]:
                dist[v] = d + peso
                padre[v] = u
                heapq.heappush(cola, (dist[v], v))
    return dist, padre

def reconstruir_ruta(padre, destino):
    ruta = []
    actual = destino
    while actual is not None:
        ruta.append(actual)
        actual = padre[actual]
    return ruta[::-1]

def resolver_ejercicio():
    print("--- 1. Farmacia para cada pedido ---")
    lugares_recogida = {}
    for nombre_pedido, datos in pedidos.items():
        para_este_pedido = []
        for farmacia, stock in farmacias.items():
            if datos['items'].issubset(stock):
                para_este_pedido.append(farmacia)
                lugares_recogida[nombre_pedido] = farmacia
        print(f"{nombre_pedido} ({', '.join(datos['items'])}): Farmacia {para_este_pedido[0]}")

    print("\n--- 2 y 3. Ruta y coste total (Estrategia: sitio útil más cercano) ---")
    actual = 'S'
    coste_total = 0
    ruta_total = ['S']
    
    pendientes_recoger = dict(lugares_recogida) # {'Pedido 1': 'F', 'Pedido 2': 'F', 'Pedido 3': 'T'}
    pendientes_entregar = {} 
    
    paso = 1
    while pendientes_recoger or pendientes_entregar:
        distancias, padres = dijkstra_path(grafo, actual)
        
        # Identificar los "sitios útiles" actuales
        sitios_utiles = set(pendientes_recoger.values()).union(set(pendientes_entregar.values()))
        
        # Encontrar el sitio útil más cercano
        sitio_mas_cercano = None
        distancia_min = float('inf')
        
        for sitio in sitios_utiles:
            if distancias[sitio] < distancia_min:
                distancia_min = distancias[sitio]
                sitio_mas_cercano = sitio
                
        # Nos movemos al sitio más cercano
        camino_segmento = reconstruir_ruta(padres, sitio_mas_cercano)
        
        print(f"Paso {paso}: Desde {actual} el sitio útil más cercano es {sitio_mas_cercano} (Distancia: {distancia_min})")
        print(f"         Ruta tomada: {' -> '.join(camino_segmento)}")
        
        coste_total += distancia_min
        ruta_total.extend(camino_segmento[1:]) # Añadimos sin duplicar el nodo de origen
        actual = sitio_mas_cercano
        
        # Actualizar estado de pedidos en esta ubicación
        recogidos = [p for p, f in list(pendientes_recoger.items()) if f == actual]
        for p in recogidos:
            print(f"         [+] Se recoge {p} en {actual}")
            pendientes_entregar[p] = pedidos[p]['destino']
            del pendientes_recoger[p]
            
        entregados = [p for p, d in list(pendientes_entregar.items()) if d == actual]
        for p in entregados:
            print(f"         [-] Se entrega {p} en {actual}")
            del pendientes_entregar[p]
            
        paso += 1

    print(f"\nRuta final completa: {' -> '.join(ruta_total)}")
    print(f"Coste total: {coste_total} minutos")

if __name__ == "__main__":
    resolver_ejercicio()