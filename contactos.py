from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#MySQL Connection
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontactos'
mysql = MySQL()
mysql.init_app(app)

# settings
app.secret_key = 'secretkey'

@app.route('/')
def Index():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts')
    data = cursor.fetchall()  
    return render_template('index.html',contacts = data )

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST': 
        nombre= request.form['nombre']
        telefono= request.form['telefono']        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO contacts (nombre, telefono) VALUES (%s, %s)',(nombre, telefono))
        mysql.connection.commit()

        flash('Contacto Agregado')  

        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def edit_contact(id):
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM contacts WHERE id = {id}")
    data = cursor.fetchall()

    return render_template('editar_contactos.html',contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre= request.form['nombre']
        telefono= request.form['telefono']
        
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE contacts SET nombre = %s, telefono = %s WHERE id = %s ",(nombre, telefono, id) )
        mysql.connection.commit() 
        flash('Contacto Actualizado')
        return redirect(url_for('Index'))


@app.route('/delete/<string:id>')
def delete_contact(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()

    flash('Contacto Eliminado')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port= 8000, debug= True)
