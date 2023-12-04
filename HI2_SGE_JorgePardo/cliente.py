import tkinter as tk
from tkinter import (Scrollbar,messagebox,ttk)
import sqlite3



def cliente():
    #Nos conectamos a la base de datos
    conn = sqlite3.connect("supermercado.db")
    cursor = conn.cursor()
    #Creamos la tabla si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes
                  (IdCliente INTEGER PRIMARY KEY AUTOINCREMENT,
                   Nombre TEXT,
                   Apellido TEXT,
                   Telefono TEXT,
                   Direccion TEXT,
                   Correo TEXT)''')
    
    #Funcion del boton de salir para salir de la ventana
    def salir():
        ventanaCliente.destroy()

    #Funcion para recoger el contenido del Treeview
    def leer_registros():
        with sqlite3.connect("supermercado.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM clientes")
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
        identificador = IdCliente_entrada.get()
        nombre = nombre_entrada.get()
        apellido = apellido_entrada.get()
        telefono = telefono_entrada.get()
        direccion = direccion_entrada.get()
        correo = correo_entrada.get()
        #Nos conectamos a la base de datos
        with sqlite3.connect("supermercado.db") as conn:
            cursor = conn.cursor()
        #Realizamos el insert
        cursor.execute(
            "INSERT INTO clientes (IdCliente,Nombre, Apellido, Telefono, Direccion, Correo) VALUES (?, ?, ?, ?, ?,?)",
            (identificador,nombre, apellido, telefono,direccion,correo))
        conn.commit()
        #Mostramos los datos en el Treeview
        mostrar_registros()
        #Mostramos un mensaje de exitoso
        messagebox.showinfo("Éxito", "Cliente creado exitosamente.")


    def eliminar_registro():
        seleccion = lista_registros.selection() #trae el elemento que tenemos clicado en la lista_registri
        if seleccion:
            '''
            siempre que tengamos un elemento seleccionado,obtenemos el valor de la primera columna del elemento seleccionado de la lista. 
            Este valor es el ID del registro que se va a eliminar.
                    '''

            id_seleccionado = lista_registros.item(seleccion, "values")[0]
            cursor = conn.cursor() # Nos conectamos a la base de datos

            cursor.execute("DELETE FROM clientes WHERE IdCliente = ?", (id_seleccionado,))
            conn.commit()
            mostrar_registros()
            messagebox.showinfo("👍", "Cliente eliminado exitosamente.")

    def editar_registro():
        seleccion = lista_registros.selection()
        if seleccion:
            id_seleccionado = lista_registros.item(seleccion, "values")[0]
            # Obtener los nuevos valores desde las cajas de entrada
            nombre = nombre_entrada.get()
            apellido = apellido_entrada.get()
            telefono = telefono_entrada.get()
            direccion = direccion_entrada.get()
            correo = correo_entrada.get()
            with sqlite3.connect("supermercado.db") as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("UPDATE clientes SET Nombre = ?, Apellido = ?, Telefono = ?, Direccion = ?, Correo = ? WHERE IdCliente = ?",
                                (nombre, apellido, telefono, direccion, correo,id_seleccionado))
                    conn.commit()
                    mostrar_registros()
                    messagebox.showinfo("👍", "Cliente editado.")
                except sqlite3.Error as e:
                    messagebox.showerror("❌", f"No se pudo editar el cliente: {e}")


    
    ventanaCliente = tk.Tk()
    ventanaCliente.title('Ventana Cliente')

    ventanaCliente.geometry("800x350")
    ventanaCliente.resizable(False,False)

    IdCliente=tk.Label(ventanaCliente,text='ID Cliente')
    IdCliente_entrada = tk.Entry(ventanaCliente)
    nombre=tk.Label(ventanaCliente,text='Nombre')
    nombre_entrada = tk.Entry(ventanaCliente)
    apellido=tk.Label(ventanaCliente,text='Apellido')
    apellido_entrada = tk.Entry(ventanaCliente)
    telefono=tk.Label(ventanaCliente, text='Telefono')
    telefono_entrada = tk.Entry(ventanaCliente)
    direccion=tk.Label(ventanaCliente, text='Direccion')
    direccion_entrada = tk.Entry(ventanaCliente)
    correo=tk.Label(ventanaCliente, text='Correo')
    correo_entrada = tk.Entry(ventanaCliente)
    botonInsert = tk.Button(ventanaCliente,command=crear_registro,text="Insertar")
    botonInsert.place(x=10,y=280)
    botonUpdate = tk.Button(ventanaCliente,command=editar_registro,text="Actualizar")
    botonUpdate.place(x=70,y=280)
    botonDelete = tk.Button(ventanaCliente,command=eliminar_registro,text="Eliminar")
    botonDelete.place(x=140,y=280)
    botonSalir = tk.Button(ventanaCliente,command=salir,text="<", width=2, height=1)#Atras
    botonSalir.place(x=10,y=10)
    # Colocar las entradas en la ventana
    IdCliente.place(x=10,y=35)
    IdCliente_entrada.place(x=13,y=55)
    nombre.place(x=10,y=75)
    nombre_entrada.place(x=13,y=95)
    apellido.place(x=10,y=115)
    apellido_entrada.place(x=13,y=135)
    telefono.place(x=10,y=155)
    telefono_entrada.place(x=13,y=175)
    direccion.place(x=10,y=195)
    direccion_entrada.place(x=13,y=215)
    correo.place(x=10,y=235)
    correo_entrada.place(x=13,y=255)

    def ordenar_columna(tree, col, reverse):
        data = [ (tree.set(child, col), child) for child in tree.get_children('')]
        data.sort(reverse=reverse)
        for i, item in enumerate(data):
            tree.move(item[1], '', i)
        tree.heading(col, command=lambda: ordenar_columna(tree, col, not reverse))

    lista_registros = ttk.Treeview(ventanaCliente, columns=("IdCliente", "Nombre", "Apellido", "Telefono", "Direccion", "Correo"),show="headings", selectmode="browse")
    
    lista_registros.heading("IdCliente", text="IdCliente",command=lambda: ordenar_columna(lista_registros,"IdCliente",False))
    lista_registros.heading("Nombre", text="Nombre",command=lambda: ordenar_columna(lista_registros,"Nombre",False))
    lista_registros.heading("Apellido", text="Apellido",command=lambda: ordenar_columna(lista_registros,"Apellido",False))
    lista_registros.heading("Telefono", text="Telefono",command=lambda: ordenar_columna(lista_registros,"Telefono",False))
    lista_registros.heading("Direccion", text="Direccion",command=lambda: ordenar_columna(lista_registros,"Direccion",False))
    lista_registros.heading("Correo", text="Correo",command=lambda: ordenar_columna(lista_registros,"Correo",False))

    lista_registros.column("IdCliente", width=100)
    lista_registros.column("Nombre", width=100)
    lista_registros.column("Apellido", width=100)
    lista_registros.column("Telefono", width=100)
    lista_registros.column("Direccion", width=100)
    lista_registros.column("Correo", width=100)
    style = ttk.Style()
    style.configure("Treeview",
                background="gray",  # Color de fondo
                foreground="blue",  # Color del texto
                rowheight=25,)  # Altura de la fila

    style.map("Treeview", background=[('selected', '#cc007b')])
    lista_registros.place(x=170,y=10)
    scrollbar = Scrollbar(ventanaCliente, orient="vertical", command=lista_registros.yview)
    scrollbar.place(x=772,y=10,height=225)
    lista_registros.configure(yscrollcommand=scrollbar.set)
    mostrar_registros()
    ventanaCliente.mainloop()