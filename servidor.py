#uvicorn servidor:app --host 0.0.0.0 --port 8000 --reload
import os
import requests
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
    if not os.path.exists(json_filename):  # Verifica si el archivo ya existe
        response = requests.get(url)
        if response.status_code == 200:
            with open(json_filename, "w", encoding="utf-8") as file:
                file.write(response.text)
            print("Archivo descargado exitosamente.")
        else:
            print(f"Error al descargar el archivo: {response.status_code}")
    else:
        print(f"El archivo {json_filename} ya existe.")

download_json_file()

# Modelo
class Book(BaseModel):
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
        # Leer el archivo JSON usando pandas
        df = pd.read_json(json_filename)
        # Convertir el DataFrame en una lista de diccionarios para la API
        return df.to_dict(orient="records")  
    else:
        print("Archivo inexistente")
        return []

def save_books(books):
    pd.DataFrame(books).to_json(json_filename, orient="records")


@app.get("/books")
def get_books(): 
    books = load_books() 
    return books  


#@app.get("/books/{book_id}", response_model=Book) 
#def get_book_by_id(book_id: int):
#    books = load_books() 
 #   print("books: ", books) 
 #   for book in books: 
 #       if book["id"] == book_id: 
 #           print("book: ", book)
  #          return book 
  #  raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books")
async def get_books(country: Optional[str] = None, year: Optional[int] = None):
    print("ENTRA ACA?")
    books = load_books()
    if country:
        books = [book for book in books if book['country'].lower() == country.lower()]
    if year:
        books = [book for book in books if book['year'] == year]
    
    if not books:
        raise HTTPException(status_code=404, detail="No books found with the specified filters.")
    
    return books

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