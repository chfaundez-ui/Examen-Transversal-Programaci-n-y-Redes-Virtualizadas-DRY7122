import requests

API_KEY = "11b7dfcd-c1b5-4e64-8549-3dfda1ccb702"  # Reemplazar con tu clave de API activa

def obtener_coordenadas(ciudad, pais):
    url = f"https://graphhopper.com/api/1/geocode?q={ciudad},{pais}&locale=es&key={API_KEY}"
    response = requests.get(url).json()
    if response.get("hits"):
        point = response["hits"][0]["point"]
        return point["lat"], point["lng"]
    return None

def calcular_ruta():
    while True:
        print("\n==============================")
        print("   Planificador de Viajes     ")
        print("==============================")
        
       # Línea 17: Solicitar la ciudad de origen
        origen = input("Ciudad de Origen (Chile) [o 's' para salir]: ").strip()
        
        # Línea 20: Condición de salida corregida (sin la etiqueta)
        if origen.lower() == 's':
            print("Saliendo del programa...")
            break
            
        destino = input("Ciudad de Destino (Argentina): ").strip()
        
        # Línea 29: Eliminar el texto '' del final
        print("\nSeleccione el medio de transporte:") 
        print("1. Auto (car)") 
        print("2. Bicicleta (bike)") 
        print("3. Pie (foot)") 
        opcion = input("Opción: ").strip()
        
        vehiculos = {"1": "car", "2": "bike", "3": "foot"}
        vehicle = vehiculos.get(opcion, "car")
        
        coord_origen = obtener_coordenadas(origen, "Chile") 
        coord_destino = obtener_coordenadas(destino, "Argentina") 
        
        if not coord_origen or not coord_destino:
            print("No se pudieron encontrar las ciudades ingresadas. Intente nuevamente.")
            continue
            
        # Llamada a la API de Enrutamiento
        route_url = f"https://graphhopper.com/api/1/route?point={coord_origen[0]},{coord_origen[1]}&point={coord_destino[0]},{coord_destino[1]}&vehicle={vehicle}&locale=es&instructions=true&key={API_KEY}"
        route_res = requests.get(route_url).json()
        
        if "paths" in route_res:
            path = route_res["paths"][0]
            distancia_km = path["distance"] / 1000
            distancia_millas = distancia_km * 0.621371
            duracion_minutos = path["time"] / 60000
            
            # Formatear la duración del viaje
            horas = int(duracion_minutos // 60)
            minutos = int(duracion_minutos % 60)
            
            print("\n--- RESUMEN DEL VIAJE ---") 
            print(f"Desde: {origen} -> Hacia: {destino}")
            print(f"Distancia en Kilómetros: {distancia_km:.2f} km") 
            print(f"Distancia en Millas: {distancia_millas:.2f} mi") 
            print(f"Duración estimada: {horas} horas y {minutos} minutos") 
            print(f"Medio de transporte utilizado: {vehicle}") 
            
            print("\n--- NARRATIVA DEL VIAJE ---") 
            for instr in path["instructions"]:
                print(f"- {instr['text']} ({instr['distance']/1000:.2f} km)") 
        else:
            print("Error al calcular la ruta en coche/medio seleccionado.")

if __name__ == "__main__":
    calcular_ruta()