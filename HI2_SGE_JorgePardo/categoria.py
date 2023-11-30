import tkinter as tk
from tkinter import PhotoImage
from tkinter import (Scrollbar,messagebox,ttk)
import sqlite3


def categoria():
    #Nos conectamos a la base de datos
    conn = sqlite3.connect("supermercado.db")
    cursor = conn.cursor()

    #Creamos la tabla si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS categoria
                  (IdCategoria INTEGER PRIMARY KEY AUTOINCREMENT,
                   NombreCategoria TEXT)''')
    
    #Funcion del boton de salir para salir de la ventana
    def salir():
        ventanaCategoria.destroy()

    #Funcion para recoger el contenido del Treeview
    def leer_registros():
        with sqlite3.connect("supermercado.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM categoria")
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
        identificador = IdCategoria_entrada.get()
        nombre = nombre_entrada.get()

        #Nos conectamos a la base de datos
        with sqlite3.connect("supermercado.db") as conn:
            cursor = conn.cursor()

        #Realizamos el insert
        cursor.execute(
            "INSERT INTO categoria (IdCategoria,NombreCategoria) VALUES (?, ?)",
            (identificador,nombre))
        conn.commit()
        #Mostramos los datos en el Treeview
        mostrar_registros()
        #Mostramos un mensaje de exitoso
        messagebox.showinfo("Éxito", "Categoria creada exitosamente.")


    def eliminar_registro():
        seleccion = lista_registros.selection() #trae el elemento que tenemos clicado en la lista_registri
        if seleccion:
            '''
            siempre que tengamos un elemento seleccionado,obtenemos el valor de la primera columna del elemento seleccionado de la lista. 
            Este valor es el ID del registro que se va a eliminar.
                    '''

            id_seleccionado = lista_registros.item(seleccion, "values")[0]
            cursor = conn.cursor() # Nos conectamos a la base de datos

            cursor.execute("DELETE FROM categoria WHERE IdCategoria = ?", (id_seleccionado,))
            conn.commit()
            mostrar_registros()
            messagebox.showinfo("👍", "Categoria eliminado exitosamente.")

    def editar_registro():
        seleccion = lista_registros.selection()
        if seleccion:
            id_seleccionado = lista_registros.item(seleccion, "values")[0]

            # Obtener los nuevos valores desde las cajas de entrada            
            nombre = nombre_entrada.get()

            with sqlite3.connect("supermercado.db") as conn:
                cursor = conn.cursor()

                try:
                    cursor.execute("UPDATE categoria SET NombreCategoria = ? WHERE IdCategoria = ?",
                                (nombre,id_seleccionado))
                    conn.commit()
                    mostrar_registros()
                    messagebox.showinfo("👍", "categoria editado.")
                except sqlite3.Error as e:
                    messagebox.showerror("❌", f"No se pudo editar el cliente: {e}")


    
    ventanaCategoria = tk.Tk()
    ventanaCategoria.title('Ventana categorias')

    ventanaCategoria.geometry("500x250")
    ventanaCategoria.resizable(False,False)

    IdCategoria=tk.Label(ventanaCategoria,text='ID Categoria')
    IdCategoria_entrada = tk.Entry(ventanaCategoria)

    nombre=tk.Label(ventanaCategoria,text='Nombre Categoria')
    nombre_entrada = tk.Entry(ventanaCategoria)

    botonInsert = tk.Button(ventanaCategoria,command=crear_registro,text="Insertar")
    botonInsert.place(x=10,y=180)
    botonUpdate = tk.Button(ventanaCategoria,command=editar_registro,text="Actualizar")
    botonUpdate.place(x=70,y=180)
    botonDelete = tk.Button(ventanaCategoria,command=eliminar_registro,text="Eliminar")
    botonDelete.place(x=140,y=180)

    botonSalir = tk.Button(ventanaCategoria,command=salir,text="<", width=2, height=1)#Atras
    botonSalir.place(x=10,y=10)
    
    # Colocar las entradas en la ventana
    IdCategoria.place(x=10,y=35)
    IdCategoria_entrada.place(x=13,y=55)

    nombre.place(x=10,y=75)
    nombre_entrada.place(x=13,y=95)

    lista_registros = ttk.Treeview(ventanaCategoria, columns=("IdCategoria", "NombreCategoria"),show="headings", selectmode="browse")
    
    lista_registros.heading("IdCategoria", text="IdCategoria")
    lista_registros.heading("NombreCategoria", text="NombreCategoria")

    lista_registros.column("IdCategoria", width=125)
    lista_registros.column("NombreCategoria", width=125)
    style = ttk.Style()
    style.configure("Treeview",
                background="gray",  # Color de fondo
                foreground="blue",  # Color del texto
                rowheight=25,)  # Altura de la fila

    style.map("Treeview", background=[('selected', '#cc007b')])
    lista_registros.place(x=205,y=10)
    scrollbar = Scrollbar(ventanaCategoria, orient="vertical", command=lista_registros.yview)
    scrollbar.place(x=457,y=10,height=225)
    lista_registros.configure(yscrollcommand=scrollbar.set)


    mostrar_registros()
    ventanaCategoria.mainloop()