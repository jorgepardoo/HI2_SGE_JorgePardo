import tkinter as tk
from tkinter import (Scrollbar,messagebox,ttk)
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def producto():
    #Nos conectamos a la base de datos
    conn = sqlite3.connect("supermercado.db")
    cursor = conn.cursor()

    #Creamos la tabla si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS productos
                  (IdProducto INTEGER PRIMARY KEY AUTOINCREMENT,
                   NombreProducto TEXT,
                   IdCategoria TEXT,
                   Precio TEXT,
                   Stock TEXT)''')
    
    #Funcion del boton de salir para salir de la ventana
    def salir():
        ventanaProductos.destroy()

    #Funcion para recoger el contenido del Treeview
    def leer_registros():
        with sqlite3.connect("supermercado.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM productos")
            registros = cur.fetchall()
        return registros

    #Funcion para mostrar el contenido del Treeview
    def mostrar_registros():
        lista_registros.delete(*lista_registros.get_children())
        for registro in leer_registros():
            lista_registros.insert("", "end", values=registro)

    #Funcion Insert
    def crear_registro():
        #Recopilamos los datos
        identificador = IdProducto_entrada.get()
        nombre = nombre_entrada.get()
        categoria = IdCategoria_entrada.get()
        precio = precio_entrada.get()
        stock = stock_entrada.get()
        #Nos conectamos a la base de datos
        with sqlite3.connect("supermercado.db") as conn:
            cursor = conn.cursor()
        #Realizamos el insert
        cursor.execute(
            "INSERT INTO productos (IdProducto,NombreProducto, IdCategoria, Precio, Stock) VALUES (?, ?, ?, ?, ?)",
            (identificador,nombre, categoria, precio,stock))
        conn.commit()
        #Mostramos los datos en el Treeview
        mostrar_registros()
        #Mostramos un mensaje de exitoso
        messagebox.showinfo("Éxito", "Producto creado exitosamente.")

    #Funcion delete
    def eliminar_registro():
        seleccion = lista_registros.selection() #trae el elemento que tenemos clicado en la lista_registri
        if seleccion:
            id_seleccionado = lista_registros.item(seleccion, "values")[0]
            cursor = conn.cursor() # Nos conectamos a la base de datos
            cursor.execute("DELETE FROM productos WHERE IdProducto = ?", (id_seleccionado,))
            conn.commit()
            mostrar_registros()
            messagebox.showinfo("👍", "Producto eliminado exitosamente.")

    #Funcion Update
    def editar_registro():
        seleccion = lista_registros.selection()
        if seleccion:
            id_seleccionado = lista_registros.item(seleccion, "values")[0]
            # Obtener los nuevos valores desde las cajas de entrada            
            nombre = nombre_entrada.get()
            categoria = IdCategoria_entrada.get()
            precio = precio_entrada.get()
            stock = stock_entrada.get()
            with sqlite3.connect("supermercado.db") as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("UPDATE productos SET NombreProducto = ?, IdCategoria = ?, Precio = ?, Stock = ? WHERE IdProducto = ?",
                                (nombre, categoria, precio, stock,id_seleccionado))
                    conn.commit()
                    mostrar_registros()
                    messagebox.showinfo("👍", "Producto editado.")
                except sqlite3.Error as e:
                    messagebox.showerror("❌", f"No se pudo editar el producto: {e}")

    #Mostrar grafico
    def mostrar_grafico():
            conn = sqlite3.connect("supermercado.db")
            # Creamos un dataframe con los datos de cada categoria
            sql = pd.read_sql_query('''SELECT categoria.NombreCategoria FROM productos INNER JOIN categoria ON productos.IdCategoria = categoria.IdCategoria''', conn)
            df = pd.DataFrame(sql, columns=['NombreCategoria'])

            # Calculamos la frecuencia de cada categoria
            frecuencia_categoria = df['NombreCategoria'].value_counts()

            fig, ax = plt.subplots()
            ax.pie(frecuencia_categoria, labels=frecuencia_categoria.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            ax.set_title('Categorias de Productos')

            grafico_canvas = FigureCanvasTkAgg(fig, master=ventanaProductos)
            grafico_canvas.draw()
            grafico_canvas.get_tk_widget().place(x=10, y=280)

    ventanaProductos = tk.Tk()
    ventanaProductos.title('Ventana Productos')
    ventanaProductos.geometry("700x300")

    #Creamos los campos que se encuentran en el diseño 
    IdProducto=tk.Label(ventanaProductos,text='ID Producto')
    IdProducto.place(x=10,y=35)
    IdProducto_entrada = tk.Entry(ventanaProductos)
    IdProducto_entrada.place(x=13,y=55)
    nombre=tk.Label(ventanaProductos,text='Nombre')
    nombre.place(x=10,y=75)
    nombre_entrada = tk.Entry(ventanaProductos)
    nombre_entrada.place(x=13,y=95)
    IdCategoria=tk.Label(ventanaProductos,text='ID Categoria')
    IdCategoria.place(x=10,y=115)
    IdCategoria_entrada = tk.Entry(ventanaProductos)
    IdCategoria_entrada.place(x=13,y=135)
    precio=tk.Label(ventanaProductos, text='Precio')
    precio.place(x=10,y=155)
    precio_entrada = tk.Entry(ventanaProductos)
    precio_entrada.place(x=13,y=175)
    stock=tk.Label(ventanaProductos, text='Stock')
    stock.place(x=10,y=195)
    stock_entrada = tk.Entry(ventanaProductos)
    stock_entrada.place(x=13,y=215)
    #Creamos los botones de las acciones de la base de datos
    botonInsert = tk.Button(ventanaProductos,command=crear_registro,text="Insertar")
    botonInsert.place(x=10,y=250)
    botonUpdate = tk.Button(ventanaProductos,command=editar_registro,text="Actualizar")
    botonUpdate.place(x=70,y=250)
    botonDelete = tk.Button(ventanaProductos,command=eliminar_registro,text="Eliminar")
    botonDelete.place(x=140,y=250)    
    botonGrafico = tk.Button(ventanaProductos,command=mostrar_grafico,text="Mostrar Grafico")
    botonGrafico.place(x=210,y=250)
    botonSalir = tk.Button(ventanaProductos,command=salir,text="<", width=2, height=1)
    botonSalir.place(x=10,y=10)
    def ordenar_columna(tree, col, reverse):
        data = [ (tree.set(child, col), child) for child in tree.get_children('')]
        data.sort(reverse=reverse)
        for i, item in enumerate(data):
            tree.move(item[1], '', i)
        tree.heading(col, command=lambda: ordenar_columna(tree, col, not reverse))

    lista_registros = ttk.Treeview(ventanaProductos, columns=("IdProducto", "Nombre", "IdCategoria", "Precio", "Stock"),show="headings", selectmode="browse")
    
    lista_registros.heading("IdProducto", text="IdProducto",command=lambda: ordenar_columna(lista_registros,"IdProducto",False))
    lista_registros.heading("Nombre", text="Nombre",command=lambda: ordenar_columna(lista_registros,"Nombre",False))
    lista_registros.heading("IdCategoria", text="IdCategoria",command=lambda: ordenar_columna(lista_registros,"IdCategoria",False))
    lista_registros.heading("Precio", text="Precio",command=lambda: ordenar_columna(lista_registros,"Precio",False))
    lista_registros.heading("Stock", text="Stock",command=lambda: ordenar_columna(lista_registros,"Stock",False))

    lista_registros.column("IdProducto", width=100)
    lista_registros.column("Nombre", width=100)
    lista_registros.column("IdCategoria", width=100)
    lista_registros.column("Precio", width=100)
    lista_registros.column("Stock", width=100)
    style = ttk.Style()
    style.configure("Treeview", background="gray", foreground="blue", rowheight=25,)

    style.map("Treeview", background=[('selected', '#cc007b')])
    lista_registros.place(x=170,y=10)
    scrollbar = Scrollbar(ventanaProductos, orient="vertical", command=lista_registros.yview)
    scrollbar.place(x=672,y=10,height=225)
    lista_registros.configure(yscrollcommand=scrollbar.set)

    mostrar_registros()
    ventanaProductos.mainloop()