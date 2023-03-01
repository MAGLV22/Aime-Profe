from flask import Flask, render_template, request
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import os
from twilio.rest import Client
import json
import pandas as pd



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///aime_profe.sqlite"
db = SQLAlchemy(app)
class Asistencia(db.Model): 

    __tablename__ = "asistencia"

    index = db.Column (db.Integer, primary_key = True)
    apellido = db.Column (db.String(50))
    nombre = db.Column (db.String(50))
    ci = db.Column (db.String(50))
    asistencia = db.Column (db.Integer)  
    grado = db.Column (db.String(20))
    justificativo = db.Column(db.String(100))
    fecha = db.Column (db.String(50))

with app.app_context():
    db.create_all()

# Modelo de la base de datos
# class Asistencia(db.Model):
#     __tablename__ = "asistencia"

#     id = db.Column(db.Integer, primary_key=True)
#     apellido = db.Column(db.String(50))
#     nombre = db.Column(db.String(50))
#     ci = db.Column(db.String(50))
#     asistencia = db.Column(db.Integer)
#     grado = db.Column(db.String(20))
#     justificativo = db.Column(db.String(100))
#     fecha = db.Column(db.String(50))

# crear la base de datos en contexto de Flask
# with app.app_context():
#     db.create_all()


# Login
@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.form
        diccionario_login = data.to_dict(flat=False)
        email= diccionario_login['email'][0]
        password= diccionario_login['password'][0]

        # Si los input fields NO estàn vacios, entrar a la otra ruta
        if email != '' and password != '' :
           return render_template('index.html')
        else: 
            return render_template('login.html')
    else:
        return render_template("login.html")


# Ruta de bienvenida
@app.route("/", methods = ['GET','POST'])
def index():
    return render_template("Bienvenido.html")


# Elegir grado
@app.route("/<grado>", methods = ['GET','POST'])
def grado(grado):
    print(grado)

    fecha_hoy_list = str(date.today()).split("-")
    fecha_hoy_list[0], fecha_hoy_list[2] = fecha_hoy_list[2], fecha_hoy_list[0]
    fecha_hoy_parsed = '-'.join(fecha_hoy_list)

    return render_template("grado.html", grado=grado, fecha_hoy=fecha_hoy_parsed)

# Elegir marcar asistencia
@app.route("/<grado>/asistencia", methods=["GET", "POST"])
def asistencia(grado):
    asistencias = db.session.query(Asistencia).all()

    print(request.form)
    print(grado)

    return render_template("asistencia.html", asistencias=asistencias)


# Cuando se hace GET request, filtra alumnos (y manda el mensaje).
# Cuando se hace POST tiene que guardar en la DB y mandar mensaje.
@app.route("/<grado>/asistencia/<fecha>", methods=["GET", "POST"])
def asistencia_fecha(grado, fecha): 
    # asistencias = db.session.query(Asistencia).filter_by(grado=grado).filter_by(fecha=fecha).all()
    asistencias = db.session.query(Asistencia).filter_by(fecha=fecha).all()
    # counter = 0
    # for asistencia in asistencias:
    #     if asistencia.asistencia == 1:
    #         counter = counter + 1
        
    # print(counter)
    
    if request.method == "POST":
        print("postttttttttttttttttt")
        asistencia_del_dia_a_cargar = Asistencia(apellido="stark", nombre="tony", ci="1234123", asistencia=1, grado="4T", justificativo="--", fecha="03-03-2023")
        
        diccionario = json.loads(request.form.to_dict(flat=False)["table_data"][0])
        print(diccionario["all_rows"])
        return render_template("asistencia.html", asistencias=asistencias)
    else:
        print("GEEEEEEEEEEEEEEEEEEEEEEEEET")
        return render_template("asistencia.html", asistencias=asistencias)

    # Logica para mandar el mensaje
    account_sid = "AC0694aa690cf553f86c4d7cb9b0eaa528"
    auth_token = "cf7813cf863261f2da6452648d259a3e"
    client = Client(account_sid, auth_token)
    #message = client.messages.create(body = f"La cantidad de alumnos es {counter}",from_ = "+12765959044",to = "+595984533095")
    # print(message.sid)


    return render_template("asistencia.html", asistencias=asistencias)


# CARGAR PLANILLA
@app.route("/carga_planilla", methods=['GET', 'POST'])
def cargar_planilla():
    
    if request.method == 'POST':
            
            file = request.files['file']
            file.save(file.filename)
            file_path =os.path.dirname(os.path.abspath(file.name))
            df = pd.read_excel(file_path +'/'+ file.filename)
            print(df)

            con = sqlite3.connect("instance/aime_profe.sqlite")
            # cur = con.cursor()
            # cur.execute()
            df.to_sql('asistencia',con, if_exists='replace')
            # cur = con.cursor()
            # con.commit()
            # cur.close()
            # con.close()

            asistencias = db.session.query(Asistencia).all()
            print(asistencias)

            return "Planilla cargada con éxito"
    else:
        return render_template("carga_planilla.html")

# crear la base de datos en contexto de Flask
with app.app_context():
    db.create_all()


# Ruta de bienvenida
@app.route("/generar", methods = ['GET','POST'])
def generar():
    return render_template("generar.html")


# Ruta de bienvenida
@app.route("/reporte", methods = ['GET','POST'])
def reporte():
    return render_template("reporte.html")


if __name__ == "__main__":
    app.run(debug=True)