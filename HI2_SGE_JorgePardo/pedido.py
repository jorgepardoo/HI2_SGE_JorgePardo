import tkinter as tk
from tkinter import PhotoImage
from tkinter import (Scrollbar,messagebox,ttk)
import sqlite3


def pedido():
    #Nos conectamos a la base de datos
    conn = sqlite3.connect("supermercado.db")
    cursor = conn.cursor()

    #Creamos la tabla si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS pedido
                  (IdPedido INTEGER PRIMARY KEY AUTOINCREMENT,
                   FechaPedido TEXT,
                   IdCliente TEXT)''')
    
    #Funcion del boton de salir para salir de la ventana
    def salir():
        ventanaPedidos.destroy()

    #Funcion para recoger el contenido del Treeview
    def leer_registros():
        with sqlite3.connect("supermercado.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM pedido")
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
        identificador = IdPedido_entrada.get()
        fecha = FechaPedido_entrada.get()
        identificadorCliente = IdCliente_entrada.get()

        #Nos conectamos a la base de datos
        with sqlite3.connect("supermercado.db") as conn:
            cursor = conn.cursor()

        #Realizamos el insert
        cursor.execute(
            "INSERT INTO pedido (IdPedido,FechaPedido, IdCliente) VALUES (?, ?, ?)",
            (identificador,fecha, identificadorCliente))
        conn.commit()
        #Mostramos los datos en el Treeview
        mostrar_registros()
        #Mostramos un mensaje de exitoso
        messagebox.showinfo("Éxito", "Pedido creado exitosamente.")


    def eliminar_registro():
        seleccion = lista_registros.selection() #trae el elemento que tenemos clicado en la lista_registri
        if seleccion:
            '''
            siempre que tengamos un elemento seleccionado,obtenemos el valor de la primera columna del elemento seleccionado de la lista. 
            Este valor es el ID del registro que se va a eliminar.
                    '''

            id_seleccionado = lista_registros.item(seleccion, "values")[0]
            cursor = conn.cursor() # Nos conectamos a la base de datos

            cursor.execute("DELETE FROM pedido WHERE IdPedido = ?", (id_seleccionado,))
            conn.commit()
            mostrar_registros()
            messagebox.showinfo("👍", "Pedido eliminado exitosamente.")

    def editar_registro():
        seleccion = lista_registros.selection()
        if seleccion:
            id_seleccionado = lista_registros.item(seleccion, "values")[0]

            # Obtener los nuevos valores desde las cajas de entrada            
            fecha = FechaPedido_entrada.get()
            identificadorCliente = IdCliente_entrada.get()

            with sqlite3.connect("supermercado.db") as conn:
                cursor = conn.cursor()

                try:
                    cursor.execute("UPDATE pedido SET FechaPedido = ?, IdCliente = ? WHERE IdPedido = ?",
                                (fecha, identificadorCliente,id_seleccionado))
                    conn.commit()
                    mostrar_registros()
                    messagebox.showinfo("👍", "Pedido editado.")
                except sqlite3.Error as e:
                    messagebox.showerror("❌", f"No se pudo editar el cliente: {e}")


    
    ventanaPedidos = tk.Tk()
    ventanaPedidos.title('Ventana Pedidos')

    ventanaPedidos.geometry("540x250")
    ventanaPedidos.resizable(False,False)

    IdPedido=tk.Label(ventanaPedidos,text='ID Pedido')
    IdPedido_entrada = tk.Entry(ventanaPedidos)

    FechaPedido=tk.Label(ventanaPedidos,text='Fecha del Pedido')
    FechaPedido_entrada = tk.Entry(ventanaPedidos)

    IdCliente=tk.Label(ventanaPedidos,text='ID Cliente')
    IdCliente_entrada = tk.Entry(ventanaPedidos)

    botonInsert = tk.Button(ventanaPedidos,command=crear_registro,text="Insertar")
    botonInsert.place(x=10,y=180)
    botonUpdate = tk.Button(ventanaPedidos,command=editar_registro,text="Actualizar")
    botonUpdate.place(x=70,y=180)
    botonDelete = tk.Button(ventanaPedidos,command=eliminar_registro,text="Eliminar")
    botonDelete.place(x=140,y=180)

    botonSalir = tk.Button(ventanaPedidos,command=salir,text="<", width=2, height=1)#Atras
    botonSalir.place(x=10,y=10)
    
    # Colocar las entradas en la ventana
    IdPedido.place(x=10,y=35)
    IdPedido_entrada.place(x=13,y=55)

    FechaPedido.place(x=10,y=75)
    FechaPedido_entrada.place(x=13,y=95)

    IdCliente.place(x=10,y=115)
    IdCliente_entrada.place(x=13,y=135)

    lista_registros = ttk.Treeview(ventanaPedidos, columns=("IdPedido", "FechaPedido", "IdCliente"),show="headings", selectmode="browse")
    
    lista_registros.heading("IdPedido", text="IdPedido")
    lista_registros.heading("FechaPedido", text="FechaPedido")
    lista_registros.heading("IdCliente", text="IdCliente")

    lista_registros.column("IdPedido", width=100)
    lista_registros.column("FechaPedido", width=100)
    lista_registros.column("IdCliente", width=100)
    style = ttk.Style()
    style.configure("Treeview",
                background="gray",  # Color de fondo
                foreground="blue",  # Color del texto
                rowheight=25,)  # Altura de la fila

    style.map("Treeview", background=[('selected', '#cc007b')])
    lista_registros.place(x=205,y=10)
    scrollbar = Scrollbar(ventanaPedidos, orient="vertical", command=lista_registros.yview)
    scrollbar.place(x=507,y=10,height=225)
    lista_registros.configure(yscrollcommand=scrollbar.set)


    mostrar_registros()
    ventanaPedidos.mainloop()