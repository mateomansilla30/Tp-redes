#uvicorn servidor:app --host 0.0.0.0 --port 8000 --reload
import os
import requests
import json
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from typing import Optional


app = FastAPI()

# URL del archivo JSON
url = "https://raw.githubusercontent.com/benoitvallon/100-best-books/refs/heads/master/books.json"
json_filename = "books.json"

def download_json_file():
    if not os.path.exists(json_filename):  
        response = requests.get(url)
        if response.status_code == 200:
            books = response.json()

            booksWithID = [] 
            for i, book in enumerate(books):
                booksWithID.append({ "id": i + 1 , **book })


            with open(json_filename, "w", encoding="utf-8") as file:
                json.dump(booksWithID, file, ensure_ascii=False, indent=4)
            print("Archivo descargado y actualizado con IDs exitosamente.")
        else:
            print(f"Error al descargar el archivo: {response.status_code}")
    else:
        print(f"El archivo {json_filename} ya existe.")



download_json_file()

# Modelo
class Book(BaseModel):
    id: int
    author: str
    country: str
    imageLink: str
    language: str
    link: str
    pages: int
    title: str
    year: int

def load_books():
    if os.path.exists(json_filename):  
        df = pd.read_json(json_filename)
        return df.to_dict(orient="records")  
    else:
        print("Archivo inexistente")
        return []
    
def get_book_by_id(id):
    books = load_books() 
    for book in books: 
        if book["id"] == id: 
            print(book)
            return book 
        
#Funcion creada para guardar los cambios que se hacen en el df en el archivo .json
def save_books(books):
    pd.DataFrame(books).to_json(json_filename, orient="records")

#Opcion 1 - Obtener todos los libros
@app.get("/books")
def get_books(): 
    books = load_books() 
    return { "data":books, "total_registries": len(books) } 

#Opcion 1 - Obtener un libro en especifico
@app.get("/books/{id}")
def get_by_id(id:int):
    book = get_book_by_id(id)
    if (not book):
        raise HTTPException(status_code=404, detail="Book not found")

    return { "data": book } 

#Opcion 3 - Borrar un libro por su Nombre
@app.delete("/books/{book_title}")
def delete_book(book_title: str):
    books = load_books()  
    book_to_delete = None

    # Buscar el libro por título
    for book in books:
        if book['title'].lower() == book_title.lower():  # comparar título 
            book_to_delete = book
            break
    
    if book_to_delete:
        books.remove(book_to_delete)  # eliminar el libro e
        save_books(books)  # guardar los cambios en el archivo JSON
        return {"message": f"El libro '{book_title}' ha sido eliminado exitosamente."}
    
    raise HTTPException(status_code=404, detail="Book not found")

#Opcion 4 - Agregar un libro 
@app.post("/books")
def add_book(book: Book):
    books = load_books()
    
    # Convertir el libro recibido a un diccionario y agregarlo a la lista
    books.append(book.dict())
    
    # Guardar la lista actualizada de libros
    save_books(books)
    
    return {"message": "Libro agregado exitosamente", "book": book}

#Opción 5 - Actualizar un libro
@app.put("/books")
def update_book(id: int):
    book = get_book_by_id(id)


