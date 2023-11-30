import tkinter as tk
from tkinter import PhotoImage
from tkinter import (Scrollbar,messagebox,ttk)
import sqlite3


def factura():
    #Nos conectamos a la base de datos
    conn = sqlite3.connect("supermercado.db")
    cursor = conn.cursor()

    #Creamos la tabla si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS factura
                  (IdFactura INTEGER PRIMARY KEY AUTOINCREMENT,
                   IdPedido TEXT,
                   IdProducto TEXT,
                   Precio TEXT,
                   Cantidad TEXT)''')
    
    #Funcion del boton de salir para salir de la ventana
    def salir():
        ventanaFactura.destroy()

    #Funcion para recoger el contenido del Treeview
    def leer_registros():
        with sqlite3.connect("supermercado.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM factura")
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
        identificador = IdFactura_entrada.get()
        identificadorPedido = IdPedido_entrada.get()
        identificadorProducto = IdProducto_entrada.get()
        precio = precio_entrada.get()
        cantidad = cantidad_entrada.get()

        #Nos conectamos a la base de datos
        with sqlite3.connect("supermercado.db") as conn:
            cursor = conn.cursor()

        #Realizamos el insert
        cursor.execute(
            "INSERT INTO factura (IdFactura,IdPedido, IdProducto, Precio, Cantidad) VALUES (?, ?, ?, ?, ?)",
            (identificador,identificadorPedido, identificadorProducto, precio,cantidad))
        conn.commit()
        #Mostramos los datos en el Treeview
        mostrar_registros()
        #Mostramos un mensaje de exitoso
        messagebox.showinfo("Éxito", "Factura creada exitosamente.")


    def eliminar_registro():
        seleccion = lista_registros.selection() #trae el elemento que tenemos clicado en la lista_registri
        if seleccion:
            '''
            siempre que tengamos un elemento seleccionado,obtenemos el valor de la primera columna del elemento seleccionado de la lista. 
            Este valor es el ID del registro que se va a eliminar.
                    '''

            id_seleccionado = lista_registros.item(seleccion, "values")[0]
            cursor = conn.cursor() # Nos conectamos a la base de datos

            cursor.execute("DELETE FROM factura WHERE IdFactura = ?", (id_seleccionado,))
            conn.commit()
            mostrar_registros()
            messagebox.showinfo("👍", "Factura eliminada exitosamente.")

    def editar_registro():
        seleccion = lista_registros.selection()
        if seleccion:
            id_seleccionado = lista_registros.item(seleccion, "values")[0]

            # Obtener los nuevos valores desde las cajas de entrada            
            identificadorPedido = IdPedido_entrada.get()
            identificadorProducto = IdProducto_entrada.get()
            precio = precio_entrada.get()
            cantidad = cantidad_entrada.get()

            with sqlite3.connect("supermercado.db") as conn:
                cursor = conn.cursor()

                try:
                    cursor.execute("UPDATE factura SET IdPedido = ?, IdProducto = ?, Precio = ?, Cantidad = ? WHERE IdFactura = ?",
                                (identificadorPedido, identificadorProducto, precio, cantidad,id_seleccionado))
                    conn.commit()
                    mostrar_registros()
                    messagebox.showinfo("👍", "Factura editada.")
                except sqlite3.Error as e:
                    messagebox.showerror("❌", f"No se pudo editar la factura: {e}")


    
    ventanaFactura = tk.Tk()
    ventanaFactura.title('Ventana Factura')

    ventanaFactura.geometry("700x300")
    ventanaFactura.resizable(False,False)

    IdFactura=tk.Label(ventanaFactura,text='ID Factura')
    IdFactura_entrada = tk.Entry(ventanaFactura)

    IdPedido=tk.Label(ventanaFactura,text='ID Pedido')
    IdPedido_entrada = tk.Entry(ventanaFactura)

    IdProducto=tk.Label(ventanaFactura,text='ID Producto')
    IdProducto_entrada = tk.Entry(ventanaFactura)

    precio=tk.Label(ventanaFactura, text='Precio')
    precio_entrada = tk.Entry(ventanaFactura)

    cantidad=tk.Label(ventanaFactura, text='Cantidad')
    cantidad_entrada = tk.Entry(ventanaFactura)    


    botonInsert = tk.Button(ventanaFactura,command=crear_registro,text="Insertar")
    botonInsert.place(x=10,y=250)
    botonUpdate = tk.Button(ventanaFactura,command=editar_registro,text="Actualizar")
    botonUpdate.place(x=70,y=250)
    botonDelete = tk.Button(ventanaFactura,command=eliminar_registro,text="Eliminar")
    botonDelete.place(x=140,y=250)

    botonSalir = tk.Button(ventanaFactura,command=salir,text="<", width=2, height=1)#Atras
    botonSalir.place(x=10,y=10)
    
    # Colocar las entradas en la ventana
    IdFactura.place(x=10,y=35)
    IdFactura_entrada.place(x=13,y=55)

    IdPedido.place(x=10,y=75)
    IdPedido_entrada.place(x=13,y=95)

    IdProducto.place(x=10,y=115)
    IdProducto_entrada.place(x=13,y=135)

    precio.place(x=10,y=155)
    precio_entrada.place(x=13,y=175)

    cantidad.place(x=10,y=195)
    cantidad_entrada.place(x=13,y=215)   

    lista_registros = ttk.Treeview(ventanaFactura, columns=("IdFactura", "IdPedido", "IdProducto", "Precio", "Cantidad"),show="headings", selectmode="browse")
    
    lista_registros.heading("IdFactura", text="IdFactura")
    lista_registros.heading("IdPedido", text="IdPedido")
    lista_registros.heading("IdProducto", text="IdProducto")
    lista_registros.heading("Precio", text="Precio")
    lista_registros.heading("Cantidad", text="Cantidad")

    lista_registros.column("IdFactura", width=100)
    lista_registros.column("IdPedido", width=100)
    lista_registros.column("IdProducto", width=100)
    lista_registros.column("Precio", width=100)
    lista_registros.column("Cantidad", width=100)
    style = ttk.Style()
    style.configure("Treeview",
                background="gray",  # Color de fondo
                foreground="blue",  # Color del texto
                rowheight=25,)  # Altura de la fila

    style.map("Treeview", background=[('selected', '#cc007b')])
    lista_registros.place(x=170,y=10)
    scrollbar = Scrollbar(ventanaFactura, orient="vertical", command=lista_registros.yview)
    scrollbar.place(x=672,y=10,height=225)
    lista_registros.configure(yscrollcommand=scrollbar.set)


    mostrar_registros()
    ventanaFactura.mainloop()