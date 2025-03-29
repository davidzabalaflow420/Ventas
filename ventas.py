import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

class Producto:
    def __init__(self, nombre, marca, precio):
        self.nombre = nombre
        self.marca = marca
        self.precio = precio

    def __str__(self):
        return f"{self.nombre} ({self.marca}) - ${self.precio}"

class Inventario:
    def __init__(self, archivo="productos.json"):
        self.archivo = archivo
        self.productos = self.cargar_productos()

    def cargar_productos(self):
        try:
            with open(self.archivo, "r") as f:
                productos = [Producto(**p) for p in json.load(f)]
                print("Productos cargados:", productos)
                return productos
        except FileNotFoundError:
            print("Archivo de productos no encontrado, iniciando con lista vacía.")
            return []

    def guardar_productos(self):
        with open(self.archivo, "w") as f:
            json.dump([p.__dict__ for p in self.productos], f)
        print("Productos guardados en el archivo.")

class Carrito:
    def __init__(self):
        self.items = []
    
    def agregar(self, producto):
        self.items.append(producto)
        print(f"Producto agregado al carrito: {producto}")
    
    def vaciar(self):
        self.items.clear()
        print("Carrito vaciado.")
    
    def total(self):
        total = sum(p.precio for p in self.items)
        print(f"Total del carrito: ${total}")
        return total

class Ventas:
    def __init__(self, archivo="ventas.json"):
        self.archivo = archivo
        self.ventas = self.cargar_ventas()
    
    def cargar_ventas(self):
        try:
            with open(self.archivo, "r") as f:
                ventas = json.load(f)
                print("Ventas cargadas:", ventas)
                return ventas if isinstance(ventas, dict) else {}
        except FileNotFoundError:
            print("Archivo de ventas no encontrado, iniciando con diccionario vacío.")
            return {}
    
    def guardar_ventas(self):
        with open(self.archivo, "w") as f:
            json.dump(self.ventas, f)
        print("Ventas guardadas en el archivo.")
    
    def registrar_venta(self, carrito):
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        if fecha_actual not in self.ventas:
            self.ventas[fecha_actual] = {}
        
        for producto in carrito.items:
            if producto.nombre in self.ventas[fecha_actual]:
                self.ventas[fecha_actual][producto.nombre]['cantidad'] += 1
            else:
                self.ventas[fecha_actual][producto.nombre] = {'precio': producto.precio, 'cantidad': 1}
        
        self.guardar_ventas()
        print("Venta registrada para el día", fecha_actual)

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Ventas Maloka")
        
        self.inventario = Inventario()
        self.carrito = Carrito()
        self.ventas = Ventas()
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        self.label_productos = tk.Label(self.root, text="Productos Disponibles")
        self.label_productos.pack()
        
        self.lista_productos = tk.Listbox(self.root)
        self.lista_productos.pack()
        self.cargar_lista_productos()
        
        self.boton_agregar = tk.Button(self.root, text="Agregar al Carrito", command=self.agregar_al_carrito)
        self.boton_agregar.pack()
        
        self.label_carrito = tk.Label(self.root, text="Carrito de Compras")
        self.label_carrito.pack()
        
        self.lista_carrito = tk.Listbox(self.root)
        self.lista_carrito.pack()
        
        self.boton_finalizar = tk.Button(self.root, text="Finalizar Venta", command=self.finalizar_venta)
        self.boton_finalizar.pack()
        
        self.boton_ver_productos = tk.Button(self.root, text="Ver Productos", command=self.ver_productos)
        self.boton_ver_productos.pack()
        
        self.boton_ver_ventas = tk.Button(self.root, text="Ver Ventas del Día", command=self.ver_ventas)
        self.boton_ver_ventas.pack()
    
    def cargar_lista_productos(self):
        self.lista_productos.delete(0, tk.END)
        for p in self.inventario.productos:
            self.lista_productos.insert(tk.END, str(p))
        print("Lista de productos actualizada en la interfaz.")
    
    def agregar_al_carrito(self):
        seleccion = self.lista_productos.curselection()
        if seleccion:
            producto = self.inventario.productos[seleccion[0]]
            self.carrito.agregar(producto)
            self.lista_carrito.insert(tk.END, str(producto))
        print("Producto añadido al carrito desde la interfaz.")
    
    def finalizar_venta(self):
        if not self.carrito.items:
            messagebox.showwarning("Carrito vacío", "No hay productos en el carrito.")
            return
        
        total = self.carrito.total()
        self.ventas.registrar_venta(self.carrito)
        messagebox.showinfo("Venta Finalizada", f"La venta se ha registrado correctamente.\nTotal: ${total:.2f}")
        self.carrito.vaciar()
        self.lista_carrito.delete(0, tk.END)
        print("Venta finalizada y carrito vaciado en la interfaz.")
    
    def ver_productos(self):
        productos_info = "\n".join(str(p) for p in self.inventario.productos)
        messagebox.showinfo("Productos Disponibles", productos_info if productos_info else "No hay productos almacenados.")
        print("Se mostraron los productos disponibles.")
    
    def ver_ventas(self):
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        if fecha_actual not in self.ventas.ventas or not self.ventas.ventas[fecha_actual]:
            messagebox.showinfo("Ventas del Día", "No hay ventas registradas para hoy.")
            print("No hay ventas registradas para hoy.")
            return
        
        ventas_info = "\n".join([f"{nombre} ${info['precio']} x{info['cantidad']}" for nombre, info in self.ventas.ventas[fecha_actual].items()])
        messagebox.showinfo("Ventas del Día", ventas_info)
        print("Se mostraron las ventas del día.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
