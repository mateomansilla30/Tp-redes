import requests

cierre = 'si'

while cierre != 'no':
    print("------------------------------")
    cierre = input("Desea realizar una operación? (si/no): ").lower()
    

    if cierre not in ['si', 'sí', 'no', 'nó']:
        print("------------------------------")
        print("Respuesta no válida. Por favor, responde 'si' o 'no'.")
        
        continue

    if cierre == 'si' or cierre == 'sí':
        print("------------------------------")
        print("Opciones disponibles:")
        print("1: Ver todos los libros")
        print("2: Opción 2")
        print("3: Eliminar un Libro")
        print("4: Opción 4")
        print("5: Opción 5")
        opciones_lista = [1, 2, 3, 4, 5]
        print("------------------------------")
        opcion = int(input("Elija una de las opciones: 1, 2, 3, 4, 5: "))
        

        if opcion not in opciones_lista:
            print("------------------------------")
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
                    print(i,f"- {book['title']} by {book['author']}")
                    print("Libros totales: ",i)
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


        if opcion == 4:
            # Solicitar datos para el nuevo libro
            print("Ingrese los detalles del nuevo libro:")
            title = input("Título: ").strip()
            author = input("Autor: ").strip()
            country = input("País: ").strip()
            imageLink = input("Enlace de imagen: ").strip()
            language = input("Idioma: ").strip()
            link = input("Enlace: ").strip()
            pages = int(input("Páginas: "))
            year = int(input("Año: "))

            new_book = {
                "title": title,
                "author": author,
                "country": country,
                "imageLink": imageLink,
                "language": language,
                "link": link,
                "pages": pages,
                "year": year
            }

            response = requests.post(f"{base_url}/books", json=new_book)
            if response.status_code == 200:
                print("Libro agregado exitosamente!")
                print(response.json())
            else:
                print(f"Error al agregar el libro: {response.status_code}")    
            
    elif cierre == 'no' or cierre == 'nó':
        print("------------------------------")
        print("Gracias por usar nuestra API :)")
        break
