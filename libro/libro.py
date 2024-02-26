class Libro:
    
    def __init__(self, autor, titulo, año_publicacion):
        self.autor = autor
        self.titulo = titulo
        self.año_publicacion = año_publicacion

    def quicksort_libros(lista, criterio):
        if len(lista) <= 1:
            return lista
        else:
            pivot = lista[0]
            menores = [libro for libro in lista[1:] if getattr(libro, criterio) < getattr(pivot, criterio)]
            mayores = [libro for libro in lista[1:] if getattr(libro, criterio) >= getattr(pivot, criterio)]
            return Libro.quicksort_libros(menores, criterio) + [pivot] + Libro.quicksort_libros(mayores, criterio)

    def busqueda_binaria_libros(lista, criterio, valor_busqueda):
        izquierda = 0
        derecha = len(lista) - 1

        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            valor_medio = getattr(lista[medio], criterio)

            if valor_medio == valor_busqueda:
                return lista[medio]
            elif valor_medio < valor_busqueda:
                izquierda = medio + 1
            else:
                derecha = medio - 1

        return None


    def agregar_libro():
        autor = input("Ingrese el autor del libro: ")
        titulo = input("Ingrese el título del libro: ")
        año_publicacion = input("Ingrese el año de publicación: ")

        # Instanciar la clase libro
        nuevo_libro = Libro(autor, titulo, año_publicacion)

        # Agregar el libro a la lista libros
        libros.append(nuevo_libro)

        print("El libro se guardo correctamente en la biblioteca.")

    def buscar_libro():
        # Solicitar al usuario el criterio de búsqueda y el valor a buscar
        criterio = input("Ingrese el criterio de búsqueda (autor, titulo, año_publicacion): ")
        valor_busqueda = input(f"Ingrese el {criterio} del libro que desea buscar: ")

        # Nos aseguramos que la lista de libros está ordenada según el criterio de búsqueda
        libros_ordenados = Libro.quicksort_libros(libros, criterio)

        # Realizar la búsqueda binaria
        libro_encontrado = Libro.busqueda_binaria_libros(libros_ordenados, criterio, valor_busqueda)

        # Mostrar el resultado de la búsqueda
        if libro_encontrado:
            print("Libro encontrado: ")
            print("Autor: ", libro_encontrado.autor)
            print("Titulo: ", libro_encontrado.titulo)
            print("Año de publicación", libro_encontrado.año_publicacion)
        else:
            print("El libro no se encontró en la Biblioteca.")

    def ordenar_biblioteca():
        # Solicitar al usuario el criterio para ordenar
        criterio = input("Ingrese el criterio de ordenamiento (autor, titulo, año_publicacion): ")

        libros_ordenados = Libro.quicksort_libros(libros, criterio)

        # Mostrar la lista de libros ordenados
        print("Biblioteca ordenada según", criterio)
        for libro in libros_ordenados:
            print("Autor:", libro.autor, "| Título:", libro.titulo, "| Año de publicación:", libro.año_publicacion)

    def menu_opciones():
        while True:
            print("\n --- Menú Opciones ---")
            print("1. Agregar un libro")
            print("2. Buscar un libro")
            print("3. Ordenar la biblioteca")
            print("4. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                Libro.agregar_libro()
            elif opcion == "2":
                Libro.buscar_libro()
            elif opcion == "3":
                Libro.ordenar_biblioteca()
            elif opcion == "4":
                print("Hasta luego.")
                break
            else:
                print("Opción no válida, intente nuevamente.")

# Lista de libros
libros = []

# Llamado a la función del menú de opciones
Libro.menu_opciones()
