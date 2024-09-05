import os
import xml.etree.ElementTree as ET
import graphviz
class Nodo:
    def __init__(self, dato=None, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente
class ListaCircular:
    def __init__(self):
        self.head = None
    
    def agregar(self, dato):
        nuevo_nodo = Nodo(dato)
        if not self.head:
            self.head = nuevo_nodo
            self.head.siguiente = self.head
        else:
            actual = self.head
            while actual.siguiente != self.head:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = self.head
    
    def buscar(self, nombre):
        actual = self.head
        while True:
            if actual.dato.nombre == nombre:
                return actual.dato
            actual = actual.siguiente
            if actual == self.head:
                break
        return None

    def imprimir_nombres(self):
        nombres = []
        actual = self.head
        while True:
            nombres.append(actual.dato.nombre)
            actual = actual.siguiente
            if actual == self.head:
                break
        return nombres

class Matriz:
    def __init__(self, nombre, filas, columnas):
        self.nombre = nombre
        self.filas = filas
        self.columnas = columnas
        self.datos = [[0]*columnas for _ in range(filas)]
    
    def agregar_dato(self, x, y, valor):
        self.datos[x-1][y-1] = valor
    
    def procesar(self):
        print(f"Procesando la matriz: {self.nombre}")
        for fila in self.datos:
            print(fila)
    
    def generar_grafico(self, salida=False):
        dot = graphviz.Digraph(comment=self.nombre)
        for i in range(self.filas):
            for j in range(self.columnas):
                dot.node(f'{i},{j}', str(self.datos[i][j]))
        file_name = f'{self.nombre}_salida.gv' if salida else f'{self.nombre}.gv'
        dot.render(file_name, view=True)

def cargar_archivo(ruta):
    if not os.path.exists(ruta):
        print(f"El archivo '{ruta}' no existe. Por favor, verifica el nombre y la ruta.")
        return None
    
    lista_matrices = ListaCircular()
    try:
        tree = ET.parse(ruta)
        root = tree.getroot()
        
        for matriz in root.findall('matriz'):
            nombre = matriz.get('nombre')
            filas = int(matriz.get('n'))
            columnas = int(matriz.get('m'))
            nueva_matriz = Matriz(nombre, filas, columnas)
            
            for dato in matriz.findall('dato'):
                x = int(dato.get('x'))
                y = int(dato.get('y'))
                valor = int(dato.text)
                nueva_matriz.agregar_dato(x, y, valor)
            
            lista_matrices.agregar(nueva_matriz)
        
        print(f"Archivo '{ruta}' cargado correctamente.")
        return lista_matrices
    except ET.ParseError as e:
        print(f"Error al analizar el archivo XML: {e}")
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
    return None

def escribir_archivo_salida(matriz, ruta_salida):
    root = ET.Element("matrices")
    matriz_elemento = ET.SubElement(root, "matriz", nombre=f"{matriz.nombre}_Salida", n=str(matriz.filas), m=str(matriz.columnas))
    
    for i in range(matriz.filas):
        for j in range(matriz.columnas):
            dato = ET.SubElement(matriz_elemento, "dato", x=str(i+1), y=str(j+1))
            dato.text = str(matriz.datos[i][j])
    
    tree = ET.ElementTree(root)
    tree.write(ruta_salida)

def mostrar_datos_estudiante():
    print("Datos del Estudiante")
    print("Carné: 202102855")
    print("Nombre: Elddyng Echeverria")
    print("Curso: Introducción a la Programación y Computación 2")
    print("Carrera: Ingeniería en Ciencias y Sistemas")

def menu_principal():
    lista_matrices = None
    
    while True:
        print("\nMenu principal:")
        print("1. Cargar archivo")
        print("2. Procesar archivo")
        print("3. Escribir archivo salida")
        print("4. Mostrar datos del estudiante")
        print("5. Generar grafica")
        print("6. Salida")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            ruta = input("Ingrese la ruta del archivo XML: ")
            lista_matrices = cargar_archivo(ruta)
        
        elif opcion == '2':
            if lista_matrices:
                nombres_matrices = lista_matrices.imprimir_nombres()
                print("Matrices cargadas:")
                for nombre in nombres_matrices:
                    print(f"- {nombre}")
                
                nombre_matriz = input("Ingrese el nombre de la matriz a procesar: ")
                matriz = lista_matrices.buscar(nombre_matriz)
                if matriz:
                    matriz.procesar()
                else:
                    print("Matriz no encontrada.")
            else:
                print("Primero debe cargar un archivo.")
        
        elif opcion == '3':
            if lista_matrices:
                nombre_matriz = input("Ingrese el nombre de la matriz a escribir: ")
                matriz = lista_matrices.buscar(nombre_matriz)
                if matriz:
                    ruta_salida = input("Ingrese la ruta de salida del archivo XML: ")
                    escribir_archivo_salida(matriz, ruta_salida)
                    print("Archivo de salida escrito correctamente.")
                else:
                    print("Matriz no encontrada.")
            else:
                print("Primero debe cargar un archivo.")
        
        elif opcion == '4':
            mostrar_datos_estudiante()
        
        elif opcion == '5':
            if lista_matrices:
                nombre_matriz = input("Ingrese el nombre de la matriz para generar gráfica: ")
                matriz = lista_matrices.buscar(nombre_matriz)
                if matriz:
                    matriz.generar_grafico()
                    print("Gráfica generada correctamente.")
                else:
                    print("Matriz no encontrada.")
            else:
                print("Primero debe cargar un archivo.")
        
        elif opcion == '6':
            print("Saliendo del programa.")
            break
        
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu_principal()