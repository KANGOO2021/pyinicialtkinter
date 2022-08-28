from tkinter import *
from tkinter.messagebox import *
import sqlite3
from tkinter import ttk
import re


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# MODELO
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def conexion():
    con = sqlite3.connect("base.db")
    return con


def crear_tabla():
    con = conexion()
    cursor = con.cursor()
    sql = """CREATE TABLE vehiculos
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             vehiculo varchar(30) NOT NULL,
             patente varchar(7) NOT NULL,
             año INTEGER(4) NOT NULL,
             precio varchar(10) NOT NULL)
    """
    cursor.execute(sql)
    con.commit()
try:
    conexion()
    crear_tabla()
except:
    print("Hay un error o base/tabla ya existente")


def alta(vehiculo, patente, año, precio, tree):

    patron_patente_vieja = r"^[A-Z]{3}[[\d]{3}$"
    patron_patente_nueva = r"^[A-Z]{2}[[\d]{3}[A-Z]{2}$"
    patente= b_val.get() 
    if(re.match(patron_patente_vieja, patente)) or (re.match(patron_patente_nueva, patente)):

        con = conexion()
        cursor = con.cursor()
        data = (vehiculo, patente, año, precio)
        sql = "INSERT INTO vehiculos(vehiculo, patente, año, precio) VALUES(?, ?, ?, ?)"
        cursor.execute(sql, data)
        con.commit()
        print(vehiculo, patente, año, precio)
        print("Vehiculo agregado correctamente")
        limpiarCampos()
        actualizar_treeview(tree)
        

    else:
        print("Patente incorrecta")
        showwarning(title="Advertencia", message="Patente incorrecta(use las MAYÚSCULAS)")


def actualizar_treeview(mitreview):
    registros = mitreview.get_children()
    for x in registros:
        mitreview.delete(x)

    sql = "SELECT * FROM vehiculos ORDER BY id DESC"
    con = conexion()
    cursor = con.cursor()
    datos = cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        print(fila)
        mitreview.insert("", 0, text=fila[0], values=(
            fila[1], fila[2], fila[3], fila[4]))


def venta(tree):
    valor = tree.selection()
    item = tree.item(valor)
    mi_id = item['text']
    con = conexion()
    cursor = con.cursor()
    data = (mi_id,)
    sql = "DELETE FROM vehiculos WHERE id = ?;"
    cursor.execute(sql, data)
    con.commit()
    tree.delete(valor)
    print('El vehiculo ha sido VENDIDO', item['values'])


def lista():
	con = sqlite3.connect("base.db")
	cursor = con.cursor()
	try:
		cursor.execute("SELECT * FROM vehiculos ORDER BY id DESC")
		for row in cursor:
			tree.insert("", 0, text=row[0], values=(row[1], row[2], row[3], row[4]))
	except:
		pass
       

def cambio(vehiculo, patente, año, precio, tree):
    con = conexion()
    cursor = con.cursor() 
    data = (vehiculo, precio, año, patente)
    sql = "UPDATE vehiculos SET vehiculo=?,precio=?,año=? WHERE patente= ?;"
    cursor.execute(sql, data)
    con.commit()
    actualizar_treeview(tree)
    limpiarCampos()


def limpiarCampos():
	a_val.set("")
	b_val.set("")
	c_val.set("")
	d_val.set("")


def salirAplicacion():
	valor=askquestion("Salir","¿Está seguro que desea salir de la Aplicación?")
	if valor=="yes":
		root.destroy()


def mensaje():
	acerca = '''
    Desarrollado por:
    Sergio Muñoz
    Curso Python Inicial
	'''
	showinfo(title="INFORMACION", message=acerca)


def info():
	info = '''
    ABMC Tkinter
    Para modificar, liste, complete la
    patente y modifique los campos restantes.
	'''
	showinfo(title="INFORMACION", message=info)


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# VISTA
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

root = Tk()
root.title("ABMC TKINTER")
root.geometry("630x450")
root.config(background='#F07B22')


titulo = Label(root, text="Concesionario TK", font=(
    'Arial bold', 30), bg="#D9D9D9", justify="center",
     relief="raised", borderwidth=3)
titulo.grid(row=0, column=0, columnspan=8)

vehiculo = Label(root, text="VEHICULO", font=('Arial bold', 15),
                 relief="raised", bg="#92A1B3")
patente = Label(root, text="PATENTE", font=(
    'Arial bold', 15), relief="raised", bg="#92A1B3")
año = Label(root, text="AÑO", font=('Arial bold', 15),
            relief="raised", bg="#92A1B3")
precio = Label(root, text="PRECIO", font=(
    'Arial bold', 15), relief="raised", bg="#92A1B3")

vehiculo.grid(row=1, column=0, padx=10, pady=10)
patente.grid(row=2, column=0, padx=10, pady=10)
año.grid(row=1, column=2, padx=10, pady=10)
precio.grid(row=2, column=2, padx=10, pady=10)

# Defino variables para tomar valores de campos de entrada
a_val, b_val, c_val, d_val = StringVar(), StringVar(), StringVar(), StringVar()


entry_vehiculo = Entry(root, textvariable= a_val, width=15,
                    bd=3, font=('Arial bold', 15))
entry_patente = Entry(root, textvariable= b_val, width=15,
                     bd=3, font=('Arial bold', 15))
entry_año = Entry(root, textvariable= c_val, width=15,
                  bd=3, font=('Arial bold', 15))
entry_precio = Entry(root, textvariable= d_val, width=15,
                     bd=3, font=('Arial bold', 15))

entry_vehiculo.grid(row=1, column=1, padx=5, pady=5)
entry_patente.grid(row=2, column=1, padx=5, pady=5)
entry_año.grid(row=1, column=3, padx=5, pady=5)
entry_precio.grid(row=2, column=3, padx=5, pady=5)



#****************************************************
# TREEVIEW
#****************************************************

style = ttk.Style()

style.theme_use('default')
style.configure("Treeview.Heading", font=('Arial bold', 15))
style.configure("Treeview", font=('Arial bold', 12))
style.map("Treeview", background=[('selected', '#F07B22')])


tree= ttk.Treeview(root)

tree['columns'] = ("Vehículo", "Patente", "Año", "Precio")
tree.column("#0", anchor=CENTER, width=50)
tree.column("Vehículo", anchor=CENTER, width=230)
tree.column("Patente", anchor=CENTER, width=120)
tree.column("Año", anchor=CENTER, width=100)
tree.column("Precio", anchor=CENTER, width=100)

tree.heading("#0", text="ID")
tree.heading("Vehículo", text="Vehículo", anchor=CENTER)
tree.heading("Patente", text="Patente", anchor=CENTER)
tree.heading("Año", text="Año", anchor=CENTER)
tree.heading("Precio", text="Precio", anchor=CENTER)

tree.tag_configure('orow', background='#EEEEEE', font=('Arial bold', 15))
tree.grid(row=7, column=0, columnspan=5, padx=10, pady=10)

tree_scroll = Scrollbar(root, orient=VERTICAL)
tree_scroll.grid(row=7, column=4, sticky=NS, pady=10)
tree.config(yscrollcommand=tree_scroll.set)
tree_scroll.config(command=tree.yview)

#****************************************************
# MENU en casacada(ayuda)
#****************************************************

menubar = Menu(root)
ayudamenu = Menu(menubar, tearoff=0)
ayudamenu.add_command(label="Info", command=info)
ayudamenu.add_command(label="Acerca", command=mensaje)
ayudamenu.add_command(label="Salir", command=salirAplicacion)
menubar.add_cascade(label="Ayuda", menu=ayudamenu)

#****************************************************
# BOTONES que disparan las funciones
#****************************************************

boton_alta = Button(
    root, text="ALTA", padx=5, pady=5, width=5, bd=3, font=('Arial', 15), 
    bg="#07DB6D", command=lambda: alta(a_val.get(), b_val.get(), c_val.get(),
    d_val.get(), tree))
boton_alta.grid(row=5, column=0, columnspan=1)

boton_venta = Button(
    root, text="VENTA", padx=5, pady=5, width=5,bd=3, font=('Arial', 15),
    bg="#0099ff", command=lambda: venta(tree))
boton_venta.grid(row=5, column=1, columnspan=1)

boton_lista = Button(
    root, text="LISTA", padx=5, pady=5, width=5,bd=3, font=('Arial', 15),
    bg="#ffff00", command=lambda: lista())
boton_lista.grid(row=5, column=2, columnspan=1)

boton_cambio = Button(
    root, text="CAMBIO", padx=5, pady=5, width=7,bd=3, font=('Arial', 15),
    bg="#e62e00", command=lambda: cambio(a_val.get(), b_val.get(),c_val.get(),d_val.get(), tree))
boton_cambio.grid(row=5, column=3, columnspan=1)

root.config(menu=menubar)
root.mainloop()








