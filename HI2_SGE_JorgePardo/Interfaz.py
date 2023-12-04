import cliente as cliente
import producto as producto
import pedido as pedidos
import categoria as categorias
import factura as facturas
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import sqlite3
import pandas as pd

VentanaPrincipal = tk.Tk()
VentanaPrincipal.title("Supermercado")

# Seleccionamos el tamaño de la ventana
VentanaPrincipal.geometry('740x400')
VentanaPrincipal.resizable(False, False)

persona = PhotoImage(file="./recursos/persona.png")
productos = PhotoImage(file="./recursos/productos.png")
pedido = PhotoImage(file="./recursos/pedido.png")
categoria = PhotoImage(file="./recursos/categoria.png")
factura = PhotoImage(file="./recursos/factura.png")
excel = PhotoImage(file="./recursos/excel.png")
# Ajustamos el tamaño de cada icono
persona = persona.subsample(4, 4)
productos = productos.subsample(6, 7)
pedido = pedido.subsample(6, 6)
categoria = categoria.subsample(4, 4)
factura = factura.subsample(6, 6)
excel = excel.subsample(8, 8)

# Funcion para exportar base de datos a un excel
def exportar_excel():
    conn = sqlite3.connect('./supermercado.db')
    tablas = ['clientes', 'productos', 'pedido', 'categoria', 'factura']
    with pd.ExcelWriter('./recursos/supermercado.xlsx', engine='xlsxwriter') as writer:
        for tabla in tablas:
            query = f'Select * from {tabla}'
            df = pd.read_sql_query(query, conn)
            df.to_excel(writer, sheet_name=tabla, index=False)
    conn.close()
    messagebox.showinfo("", "Datos exportados.")

# Mostramos el titulo de la aplicacion
titulo = tk.Label(VentanaPrincipal, text="SISTEMA DE GESTIÓN DE UN SUPERMERCADO", font=("Arial Black", 20))
titulo.place(x=20, y=0)

# Añadimos los botones con sus respectivas posiciones y sus respectivas ventanas
boton1 = tk.Button(VentanaPrincipal, width=100, height=100, image=persona, command=cliente.cliente)  # Clientes
boton1.place(x=15,y=35)
boton2 = tk.Button(VentanaPrincipal, width=100, height=100, image=productos, command=producto.producto)# Productos
boton2.place(x=135,y=35)
boton3 = tk.Button(VentanaPrincipal, width=100, height=100, image=pedido, command=pedidos.pedido)  # Pedidos
boton3.place(x=255,y=35)
boton4 = tk.Button(VentanaPrincipal, width=100, height=100, image=categoria, command=categorias.categoria)# Categoria
boton4.place(x=375,y=35)
boton5 = tk.Button(VentanaPrincipal, width=100, height=100, image=factura, command=facturas.factura)  # Detalle / Factura
boton5.place(x=495,y=35)
botonGuardar = tk.Button(VentanaPrincipal, width=100, height=100, image=excel, command=exportar_excel) # Exportar a Excel
botonGuardar.place(x=615,y=35)
VentanaPrincipal.mainloop()
