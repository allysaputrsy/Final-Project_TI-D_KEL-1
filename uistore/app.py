from flask import Flask, g,  render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb
from pymysql import connect

app = Flask(__name__)

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'uistore'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Secret key untuk session
app.secret_key = '12345'

db = connect(
    host="localhost",

    user="root",
    password="",
    database="toko"
)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'  # Set pesan kesalahan jika login gagal
    
    return redirect(url_for('home'))

@app.context_processor
def inject_username():
    if 'username' in session:
        return dict(username=session['username'])
    return dict(username=None)

@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
        return render_template('home.html', username=username)
    return redirect(url_for('login'))

@app.route('/logout', methods=["POST"])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/uistore')
def indexpage():
    return render_template('index.html')

@app.route('/katalog')
def katalog():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT name, harga FROM produk')
    products = cursor.fetchall()
    cursor.close()
    
    return render_template('katalog.html', products=products)

@app.route('/profil')
def profil():
    return render_template('profil.html')

@app.route('/daftar')
def daftar():
    return render_template('regist.html')


if __name__ == '__main__':
    app.run(debug=True)