from datetime import datetime
import mysql.connector
import tkinter as tk
from tkinter import ttk

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="Colegio"
)

ventana = tk.Tk()
ventana.title("Base de Datos👻")
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

ancho = 700
alto = 500
x = 550
y = 175

ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
titulo = tk.Label(ventana, text="Servicio de Asistencias", font=("Arial", 16), width=20, height=2, anchor="center")
titulo.pack()

def VentanaAñadir():
    ventana2 = tk.Toplevel()
    ventana2.title("Añadir Alumnos👻")

    ventana2.geometry(f"{ancho}x{alto}+{x}+{y}")
    titulo = tk.Label(ventana2, text="Añadir Alumnos", font=("Arial", 16), width=20, height=2, anchor="center")
    titulo.pack()

    label_nombre = tk.Label(ventana2, text="Nombres:")
    label_nombre.pack()
    EntradaNombre = tk.Entry(ventana2)
    EntradaNombre.pack()

    label_apellido = tk.Label(ventana2, text="Apellidos:")
    label_apellido.pack()
    EntradaApellido = tk.Entry(ventana2)
    EntradaApellido.pack()

    label_grado = tk.Label(ventana2, text="Grado:")
    label_grado.pack()
    EntradaGrado = tk.Entry(ventana2)
    EntradaGrado.pack()

    def Añadir_Alumnos():
        Nombres = EntradaNombre.get()
        Apellidos = EntradaApellido.get()
        Grado = EntradaGrado.get()

        mycursor = mydb.cursor()
        sql = "INSERT INTO Alumnos (Nombres, Apellidos, Grado) VALUES (%s, %s, %s)"
        val = (Nombres, Apellidos, Grado)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        ventana2.destroy()

    botonadd = tk.Button(ventana2, text="Añadir Alumno", command=Añadir_Alumnos)
    botonadd.pack()

def VentanaEliminar():
    ventana3 = tk.Toplevel()
    ventana3.title("Eliminar Alumnos👻")

    ventana3.geometry(f"{ancho}x{alto}+{x}+{y}")
    titulo = tk.Label(ventana3, text="Eliminar Alumnos", font=("Arial", 16), width=20, height=2, anchor="center")
    titulo.pack()

    label_nombre = tk.Label(ventana3, text="Nombres:")
    label_nombre.pack()
    EntradaNombre2 = tk.Entry(ventana3)
    EntradaNombre2.pack()

    label_apellido = tk.Label(ventana3, text="Apellidos:")
    label_apellido.pack()
    EntradaApellido2 = tk.Entry(ventana3)
    EntradaApellido2.pack()

    label_grado = tk.Label(ventana3, text="Grado:")
    label_grado.pack()
    EntradaGrado2 = tk.Entry(ventana3)
    EntradaGrado2.pack()

    def Eliminar_Alumnos():
        Nombres = EntradaNombre2.get()
        Apellidos = EntradaApellido2.get()
        Grado = EntradaGrado2.get()

        mycursor = mydb.cursor()
        sql = "DELETE FROM Alumnos WHERE Nombres = %s AND Apellidos = %s AND Grado = %s"
        val = (Nombres, Apellidos, Grado)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record(s) deleted")
        ventana3.destroy()

    botonelim = tk.Button(ventana3, text="Eliminar Alumno", command=Eliminar_Alumnos)
    botonelim.pack()

def EditarAlumnos(Codigo, ventana_listado):
    ventana5 = tk.Toplevel()
    ventana5.title("Editar Alumno👻")
    ventana5.geometry("400x300")

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Alumnos WHERE Codigo = %s", (Codigo,))
    alumno = mycursor.fetchone()

    label_nombre = tk.Label(ventana5, text="Nombres:")
    label_nombre.pack()
    EntradaNombre = tk.Entry(ventana5)
    EntradaNombre.pack()
    EntradaNombre.insert(0, alumno[1])

    label_apellido = tk.Label(ventana5, text="Apellidos:")
    label_apellido.pack()
    EntradaApellido = tk.Entry(ventana5)
    EntradaApellido.pack()
    EntradaApellido.insert(0, alumno[2])

    label_grado = tk.Label(ventana5, text="Grado:")
    label_grado.pack()
    EntradaGrado = tk.Entry(ventana5)
    EntradaGrado.pack()
    EntradaGrado.insert(0, alumno[3])

    def Actualizar():
        Nombres = EntradaNombre.get()
        Apellidos = EntradaApellido.get()
        Grado = EntradaGrado.get()

        sql = "UPDATE Alumnos SET Nombres = %s, Apellidos = %s, Grado = %s WHERE Codigo = %s"
        val = (Nombres, Apellidos, Grado, Codigo)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record updated.")
        ventana5.destroy()
        ventana_listado.destroy()
        VentanaListado()  # Actualiza la lista de alumnos

    botonActualizar = tk.Button(ventana5, text="Actualizar", command=Actualizar)
    botonActualizar.pack()

def VentanaListado():
    ventana4 = tk.Toplevel()
    ventana4.title("Listado de Alumnos👻")
    ventana4.geometry("850x500")

    titulo = tk.Label(ventana4, text="Lista de Alumnos", font=("Arial", 16), width=20, height=2, anchor="center")
    titulo.pack()

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Alumnos")
    alumnos = mycursor.fetchall()

    tree = ttk.Treeview(ventana4, columns=("Codigo", "Nombres", "Apellidos", "Grado"), show="headings")
    tree.heading("Codigo", text="Codigo")
    tree.heading("Nombres", text="Nombres")
    tree.heading("Apellidos", text="Apellidos")
    tree.heading("Grado", text="Grado")

    for alumno in alumnos:
        tree.insert("", tk.END, values=(alumno[0], alumno[1], alumno[2], alumno[3]))

    tree.pack(fill=tk.BOTH, expand=True)

    def AlumnoSeleccionado(event):
        Seleccionado = tree.selection()[0]
        Codigo = tree.item(Seleccionado, "values")[0]
        EditarAlumnos(Codigo, ventana4)

    tree.bind("<Double-1>", AlumnoSeleccionado)
    BotonCierreLista = tk.Button(ventana4, text="Cerrar Listado", command=ventana4.destroy)
    BotonCierreLista.pack()

def VentanaRegistroA():
    ventana6 = tk.Toplevel()
    ventana6.title("Registrar Asistencias👻")
    ventana6.geometry("850x500")
    
    titulo = tk.Label(ventana6, text="Registrar Asistencias", font=("Arial", 16), width=20, height=2, anchor="center")
    titulo.pack()

    mycursor = mydb.cursor()
    mycursor.execute("SELECT Codigo, Nombres, Apellidos, Grado FROM Alumnos")
    alumnos = mycursor.fetchall()

    label_alumno = tk.Label(ventana6, text="Seleccione Alumno:")
    label_alumno.pack()
    alumno_var = tk.StringVar()
    alumnoseleccion = ttk.Combobox(ventana6, textvariable=alumno_var)
    alumnoseleccion['values'] = [f"{alumno[0]} - {alumno[1]} {alumno[2]}" for alumno in alumnos]
    alumnoseleccion.pack()

    label_asistencia = tk.Label(ventana6, text="Asistencia:")
    label_asistencia.pack()
    asistencia_var = tk.StringVar()
    asistenciaseleccion = ttk.Combobox(ventana6, textvariable=asistencia_var)
    asistenciaseleccion['values'] = ['Presente', 'Ausente', 'Justificación']
    asistenciaseleccion.pack()

    def RegistrarAsistencia():
        alumno_seleccionado = alumnoseleccion.get()
        CodigoAlumno = int(alumno_seleccionado.split(' ')[0])
        Fecha = datetime.now().strftime("%Y-%m-%d")
        Hora = datetime.now().strftime("%H:%M:%S")
        Asistencia = asistenciaseleccion.get()

        mycursor = mydb.cursor()
        sql = "INSERT INTO Asistencia (AlumnoCode, Fecha, Hora, Asistencia) VALUES (%s, %s, %s, %s)"
        val = (CodigoAlumno, Fecha, Hora, Asistencia)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        ventana6.destroy()

    BotonRegistrarAsistencia = tk.Button(ventana6, text="Registrar Asistencia", command=RegistrarAsistencia)
    BotonRegistrarAsistencia.pack()

def VentanaEliminarA():
    ventana8 = tk.Toplevel()
    ventana8.title("Eliminar Asistencia👻")

    ventana8.geometry(f"{ancho}x{alto}+{x}+{y}")

    label_codigo = tk.Label(ventana8, text="Ingrese Código del Alumno:")
    label_codigo.pack()
    EntradaAlumnoCode = tk.Entry(ventana8)
    EntradaAlumnoCode.pack()

    label_fecha = tk.Label(ventana8, text="Ingrese Fecha de Asistencia (YYYY-MM-DD):")
    label_fecha.pack()
    EntradaFecha = tk.Entry(ventana8)
    EntradaFecha.pack()

    def EliminarAsistencia():
        AlumnoCode = EntradaAlumnoCode.get()
        Fecha = EntradaFecha.get()

        mycursor = mydb.cursor()
        sql = "DELETE FROM Asistencia WHERE AlumnoCode = %s AND Fecha = %s"
        val = (AlumnoCode, Fecha)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record(s) deleted")
        ventana8.destroy()

    botonEliminar = tk.Button(ventana8, text="Eliminar Asistencia", command=EliminarAsistencia)
    botonEliminar.pack()

def VentanaHistorialA():
    ventana7 = tk.Toplevel()
    ventana7.title("Historial de Asistencias👻")
    ventana7.geometry(f"{ancho}x{alto}+{x}+{y}")

    titulo = tk.Label(ventana7, text="Historial de Asistencias", font=("Arial", 16), width=20, height=2, anchor="center")
    titulo.pack()

    label_codigo = tk.Label(ventana7, text="Ingrese Código del Alumno:")
    label_codigo.pack()
    EntradaAlumnoCode = tk.Entry(ventana7)
    EntradaAlumnoCode.pack()

    def MostrarHistorial():
        AlumnoCode = EntradaAlumnoCode.get()
        mycursor = mydb.cursor()

        # Obtener nombre y apellidos del alumno
        mycursor.execute("SELECT Nombres, Apellidos FROM Alumnos WHERE Codigo = %s", (AlumnoCode,))
        infoalumno = mycursor.fetchone()
        NomyApellidos = f"{infoalumno[0]} {infoalumno[1]}"

        # Obtener historial de asistencias
        sql = "SELECT Fecha, Hora, Asistencia FROM Asistencia WHERE AlumnoCode = %s"
        mycursor.execute(sql, (AlumnoCode,))
        asistencias = mycursor.fetchall()

        # Crear la tabla con encabezados
        tree = ttk.Treeview(ventana7, columns=("Nombre", "Fecha", "Hora", "Asistencia"), show="headings")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Hora", text="Hora")
        tree.heading("Asistencia", text="Asistencia")

        # Insertar filas con los datos obtenidos
        for asistencia in asistencias:
            tree.insert("", tk.END, values=(NomyApellidos, asistencia[0], asistencia[1], asistencia[2]))

        tree.pack(fill=tk.BOTH, expand=True)

    boton_mostrar = tk.Button(ventana7, text="Mostrar Historial", command=MostrarHistorial)
    boton_mostrar.pack()

    BotonCierreHistorial = tk.Button(ventana7, text="Cerrar Historial", command=ventana7.destroy)
    BotonCierreHistorial.pack()

def VentanaConsultas():
    ventanaConsultas = tk.Toplevel()
    ventanaConsultas.title("Consultas👻")
    ventanaConsultas.geometry("700x500")

    BotonBuscarAlumno = tk.Button(ventanaConsultas, text="Buscar Alumno por Nombre y/o Apellido", command=VentanaConsultarAlumno)
    BotonBuscarAlumno.pack(pady=15)

    BotonConsultarAsistenciasAlumnoFecha = tk.Button(ventanaConsultas, text="Buscar Alumno por Grado", command=VentanaConsultarAlumnoGrado)
    BotonConsultarAsistenciasAlumnoFecha.pack(pady=15)

    BotonConsultarAsistenciasFecha = tk.Button(ventanaConsultas, text="Consultar Asistencias por Fecha", command=VentanaConsultarAsistenciasFecha)
    BotonConsultarAsistenciasFecha.pack(pady=15)

def VentanaConsultarAlumno():
    ventana9 = tk.Toplevel()
    ventana9.title("Buscar Alumno👻")
    ventana9.geometry("900x500")

    label_nombre = tk.Label(ventana9, text="Ingrese Nombre o Apellido del Alumno:")
    label_nombre.pack()
    EntradaNombre = tk.Entry(ventana9)
    EntradaNombre.pack()

    def BuscarAlumno():
        Nombre = EntradaNombre.get()
        mycursor = mydb.cursor()
        sql = "SELECT * FROM Alumnos WHERE Nombres LIKE %s OR Apellidos LIKE %s"
        val = ("%"+Nombre+"%", "%"+Nombre+"%")
        mycursor.execute(sql, val)
        resultados = mycursor.fetchall()

        tree = ttk.Treeview(ventana9, columns=("Codigo", "Nombres", "Apellidos", "Grado"), show="headings")
        tree.heading("Codigo", text="Codigo")
        tree.heading("Nombres", text="Nombres")
        tree.heading("Apellidos", text="Apellidos")
        tree.heading("Grado", text="Grado")

        for resultado in resultados:
            tree.insert("", tk.END, values=(resultado[0], resultado[1], resultado[2], resultado[3]))

        tree.pack(fill=tk.BOTH, expand=True)

    botonBuscar = tk.Button(ventana9, text="Buscar Alumno", command=BuscarAlumno)
    botonBuscar.pack()

    BotonCierreBuscar = tk.Button(ventana9, text="Cerrar", command=ventana9.destroy)
    BotonCierreBuscar.pack()

def VentanaConsultarAsistenciasFecha():
    ventana10 = tk.Toplevel()
    ventana10.title("Consultar Asistencias por Fecha👻")
    ventana10.geometry("900x500")

    label_fecha = tk.Label(ventana10, text="Ingrese Fecha de Asistencia (YYYY-MM-DD):")
    label_fecha.pack()
    EntradaFecha = tk.Entry(ventana10)
    EntradaFecha.pack()

    def ConsultarAsistenciasFecha():
        Fecha = EntradaFecha.get()
        mycursor = mydb.cursor()
        sql = "SELECT * FROM Asistencia WHERE Fecha = %s"
        val = (Fecha,)
        mycursor.execute(sql, val)
        resultados = mycursor.fetchall()

        tree = ttk.Treeview(ventana10, columns=("AlumnoCode", "Fecha", "Hora", "Asistencia"), show="headings")
        tree.heading("AlumnoCode", text="AlumnoCode")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Hora", text="Hora")
        tree.heading("Asistencia", text="Asistencia")

        for resultado in resultados:
            tree.insert("", tk.END, values=(resultado[1], resultado[2], resultado[3], resultado[4]))

        tree.pack(fill=tk.BOTH, expand=True)

    botonConsultar = tk.Button(ventana10, text="Consultar Asistencias", command=ConsultarAsistenciasFecha)
    botonConsultar.pack()

    BotonCierreConsultar = tk.Button(ventana10, text="Cerrar", command=ventana10.destroy)
    BotonCierreConsultar.pack()

def VentanaConsultarAlumnoGrado():
    ventana9 = tk.Toplevel()
    ventana9.title("Buscar Alumnos por Grado👻")
    ventana9.geometry("900x500")

    label_grado = tk.Label(ventana9, text="Ingrese Grado del Alumno:")
    label_grado.pack()
    EntradaGrado = tk.Entry(ventana9)
    EntradaGrado.pack()

    def BuscarAlumnoPorGrado():
        Grado = EntradaGrado.get()
        mycursor = mydb.cursor()
        sql = "SELECT * FROM Alumnos WHERE Grado = %s"
        val = (Grado,)
        mycursor.execute(sql, val)
        resultados = mycursor.fetchall()

        tree = ttk.Treeview(ventana9, columns=("Codigo", "Nombres", "Apellidos", "Grado"), show="headings")
        tree.heading("Codigo", text="Codigo")
        tree.heading("Nombres", text="Nombres")
        tree.heading("Apellidos", text="Apellidos")
        tree.heading("Grado", text="Grado")

        for resultado in resultados:
            tree.insert("", tk.END, values=(resultado[0], resultado[1], resultado[2], resultado[3]))

        tree.pack(fill=tk.BOTH, expand=True)

    botonBuscar = tk.Button(ventana9, text="Buscar Alumnos", command=BuscarAlumnoPorGrado)
    botonBuscar.pack()

    BotonCierreBuscar = tk.Button(ventana9, text="Cerrar", command=ventana9.destroy)
    BotonCierreBuscar.pack()

#######################################################
BotonVentanaAñadir = tk.Button(ventana, text="Añadir Alumnos", command=VentanaAñadir)
BotonVentanaAñadir.pack(pady=12)

BotonVentanaEliminar = tk.Button(ventana, text="Eliminar Alumnos", command=VentanaEliminar)
BotonVentanaEliminar.pack(pady=12)

BotonMostrarAlumnos = tk.Button(ventana, text="Mostrar Alumnos", command=VentanaListado)
BotonMostrarAlumnos.pack(pady=12)

BotonRegistrarA = tk.Button(ventana, text="Registrar Asistencias", command=VentanaRegistroA)
BotonRegistrarA.pack(pady=12)

BotonEliminarAsistencia = tk.Button(ventana, text="Eliminar Asistencias", command=VentanaEliminarA)
BotonEliminarAsistencia.pack(pady=12)

BotonHistorialA = tk.Button(ventana, text="Revisar Asistencias", command=VentanaHistorialA)
BotonHistorialA.pack(pady=12)

BotonVentanaConsultas = tk.Button(ventana, text="Realizar Consultas", command=VentanaConsultas)
BotonVentanaConsultas.pack(pady=12)

BotonCierreT = tk.Button(ventana, text="Cerrar Servicio de Asistencias", command=ventana.destroy)
BotonCierreT.pack(pady=12)

ventana.mainloop()