import tkinter as tk
from tkinter import PhotoImage
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


    def eliminar_registro():
        seleccion = lista_registros.selection() #trae el elemento que tenemos clicado en la lista_registri
        if seleccion:
            '''
            siempre que tengamos un elemento seleccionado,obtenemos el valor de la primera columna del elemento seleccionado de la lista. 
            Este valor es el ID del registro que se va a eliminar.
                    '''

            id_seleccionado = lista_registros.item(seleccion, "values")[0]
            cursor = conn.cursor() # Nos conectamos a la base de datos

            cursor.execute("DELETE FROM productos WHERE IdProducto = ?", (id_seleccionado,))
            conn.commit()
            mostrar_registros()
            messagebox.showinfo("👍", "Producto eliminado exitosamente.")

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


    def mostrar_grafico():
        # Leer los datos de la base de datos
        registros = leer_registros()

        # Crear un DataFrame de pandas
        df = pd.DataFrame(registros, columns=["IdProducto", "NombreProducto", "IdCategoria", "Precio", "Stock"])

        # Asegurarse de que la columna "Stock" sea numérica
        df["Stock"] = pd.to_numeric(df["Stock"], errors="coerce")

        # Crear intervalos
        intervalos = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        # Calcular el recuento de productos en cada intervalo
        counts = df["Stock"].value_counts(sort=False)

        df["Intervalo"] = pd.cut(intervalos, counts, include_lowest=True)

        

        # Crear un gráfico de barras con los intervalos
        plt.figure(figsize=(8, 6))
        plt.bar(counts.index, counts, width=0.8, color="blue")
        plt.xlabel("Intervalo de Stock")
        plt.ylabel("Cantidad de Productos")
        plt.title("Distribución de Stock de Productos")

        # Integrar el gráfico en la interfaz de tkinter
        canvas = FigureCanvasTkAgg(plt.gcf(), master=ventanaProductos)
        canvas.draw()
        canvas.get_tk_widget().place(x=10, y=280)  # Ajusta las coordenadas según sea necesario

    
    ventanaProductos = tk.Tk()
    ventanaProductos.title('Ventana Productos')

    ventanaProductos.geometry("700x300")
    #ventanaProductos.resizable(False,False)

    IdProducto=tk.Label(ventanaProductos,text='ID Producto')
    IdProducto_entrada = tk.Entry(ventanaProductos)

    nombre=tk.Label(ventanaProductos,text='Nombre')
    nombre_entrada = tk.Entry(ventanaProductos)

    IdCategoria=tk.Label(ventanaProductos,text='ID Categoria')
    IdCategoria_entrada = tk.Entry(ventanaProductos)

    precio=tk.Label(ventanaProductos, text='Precio')
    precio_entrada = tk.Entry(ventanaProductos)

    stock=tk.Label(ventanaProductos, text='Stock')
    stock_entrada = tk.Entry(ventanaProductos)    


    botonInsert = tk.Button(ventanaProductos,command=crear_registro,text="Insertar")
    botonInsert.place(x=10,y=250)
    botonUpdate = tk.Button(ventanaProductos,command=editar_registro,text="Actualizar")
    botonUpdate.place(x=70,y=250)
    botonDelete = tk.Button(ventanaProductos,command=eliminar_registro,text="Eliminar")
    botonDelete.place(x=140,y=250)
    botonGrafico = tk.Button(ventanaProductos,command=mostrar_grafico,text="Mostrar Grafico")
    botonGrafico.place(x=210,y=250)

    botonSalir = tk.Button(ventanaProductos,command=salir,text="<", width=2, height=1)#Atras
    botonSalir.place(x=10,y=10)
    
    # Colocar las entradas en la ventana
    IdProducto.place(x=10,y=35)
    IdProducto_entrada.place(x=13,y=55)

    nombre.place(x=10,y=75)
    nombre_entrada.place(x=13,y=95)

    IdCategoria.place(x=10,y=115)
    IdCategoria_entrada.place(x=13,y=135)

    precio.place(x=10,y=155)
    precio_entrada.place(x=13,y=175)

    stock.place(x=10,y=195)
    stock_entrada.place(x=13,y=215)   

    lista_registros = ttk.Treeview(ventanaProductos, columns=("IdProducto", "Nombre", "IdCategoria", "Precio", "Stock"),show="headings", selectmode="browse")
    
    lista_registros.heading("IdProducto", text="IdProducto")
    lista_registros.heading("Nombre", text="Nombre")
    lista_registros.heading("IdCategoria", text="IdCategoria")
    lista_registros.heading("Precio", text="Precio")
    lista_registros.heading("Stock", text="Stock")

    lista_registros.column("IdProducto", width=100)
    lista_registros.column("Nombre", width=100)
    lista_registros.column("IdCategoria", width=100)
    lista_registros.column("Precio", width=100)
    lista_registros.column("Stock", width=100)
    style = ttk.Style()
    style.configure("Treeview",
                background="gray",  # Color de fondo
                foreground="blue",  # Color del texto
                rowheight=25,)  # Altura de la fila

    style.map("Treeview", background=[('selected', '#cc007b')])
    lista_registros.place(x=170,y=10)
    scrollbar = Scrollbar(ventanaProductos, orient="vertical", command=lista_registros.yview)
    scrollbar.place(x=672,y=10,height=225)
    lista_registros.configure(yscrollcommand=scrollbar.set)


    mostrar_registros()
    ventanaProductos.mainloop()