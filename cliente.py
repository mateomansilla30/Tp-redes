import requests

cierre = 'si'

while cierre != 'no':
    cierre = input("Desea realizar una operación? (si/no): ").lower()

    if cierre not in ['si', 'sí', 'no', 'nó']:
        print("Respuesta no válida. Por favor, responde 'si' o 'no'.")
        continue

    if cierre == 'si' or cierre == 'sí':
        print("Opciones disponibles:")
        print("1: Ver todos los libros")
        print("2: Opción 2")
        print("3: Eliminar un Libro")
        print("4: Opción 4")
        print("5: Opción 5")
        print("------------------------------")
        opciones_lista = [1, 2, 3, 4, 5]
        opcion = int(input("Elija una de las opciones: 1, 2, 3, 4, 5: "))

        if opcion not in opciones_lista:
            print(f"Opción no disponible, por favor elija una de las opciones: {opciones_lista}")
            continue

        base_url = "http://127.0.0.1:8000/"

        if opcion == 1:
            response = requests.get(f"{base_url}/books")
            if response.status_code == 200:
                books = response.json()  
                print("Libros disponibles:")
                i= 0
                for book in books:
                    i+= 1
                    print({i},f"- {book['title']} by {book['author']}")
            else:
                print(f"Error al realizar la solicitud: {response.status_code}")
        
        if opcion == 2:
            print("En construccion")
            
            
        if opcion == 3:
            book_title = input("Ingrese el título del libro que desea eliminar: ").strip()
            response = requests.delete(f"{base_url}/books/{book_title}")
            if response.status_code == 200:
                print(response.json()['message'])
            else:
                print(f"Error al realizar la solicitud: {response.status_code}")

            
    elif cierre == 'no' or cierre == 'nó':
        print("Gracias por usar nuestra API :)")
        break
