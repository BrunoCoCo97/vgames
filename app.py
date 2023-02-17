from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)

#Rutas de la aplicación
@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM videojuego")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        print (record)
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html', data=insertObject)

#Ruta para guardar videojuegos en la bdd
@app.route('/vg', methods=['POST'])
def addvg():
    nombre = request.form['videojuego']
    categoria = request.form['categoria']
    plataforma = request.form['plataforma']
    precio = request.form['precio']
    portada = request.form['portada']

    if nombre and categoria and plataforma and precio and portada:
        cursor = db.database.cursor()
        sql = "INSERT INTO videojuego (nombre, categoria, plataforma, precio, portada) VALUES (%s, %s, %s, %s, %s)"
        data = (nombre, categoria, plataforma, precio, portada)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

#Ruta para eliminar videojuegos
@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM videojuego WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

#Ruta para editar los parametros del videojuego
@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    nombre = request.form['nombre']
    categoria = request.form['categoria']
    plataforma = request.form['plataforma']
    precio = request.form['precio']
    portada = request.form['portada']

    if nombre and categoria and plataforma and precio and portada:
        cursor = db.database.cursor()
        sql = "UPDATE videojuego SET nombre = %s, categoria = %s, plataforma = %s, precio = %s, portada = %s WHERE id = %s"
        data = (nombre, categoria, plataforma, precio, portada, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)