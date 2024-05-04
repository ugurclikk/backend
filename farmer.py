from flask import Flask, request, jsonify, session
from flask_mysqldb import MySQL
import hashlib

app = Flask(__name__)
app.secret_key = 'farmer'

# MySQL bağlantısı
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Admin1224.'
app.config['MYSQL_DB'] = 'Farmer'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Sonuçları sözlük olarak almak için

mysql = MySQL(app)



class Products:
    def __init__(self):
        pass

    def get_products(self):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.close()
        return products

    def add_product(self, name, image, planting_date, irrigation_frequency, chemicals, fertilizers, application_interval):
        cursor = mysql.connection.cursor()
        chemicals_str = ','.join(chemicals)
        fertilizers_str = ','.join(fertilizers)
        cursor.execute("INSERT INTO products (name, image, planting_date, irrigation_frequency, chemicals, fertilizers, application_interval) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                    (name, image, planting_date, irrigation_frequency, chemicals_str, fertilizers_str, application_interval))
        mysql.connection.commit()
        cursor.close()



def check_password_login(plain_password, hashed_password):
    hashed_input_password = hashlib.sha256(plain_password.encode()).hexdigest()
    return hashed_input_password == hashed_password

# Yeni iş ilanı oluşturma
@app.route('/', methods=['GET'])
def open():
    return "anan"

# Kullanıcı kaydı
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        password = data['password']
        # Şifre hashleme
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, firstname, lastname, email, password) VALUES (%s, %s, %s, %s, %s)", (username, firstname, lastname, email, hashed_password))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": "User registered successfully"})

# Kullanıcı girişi
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        password = data['password']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        if user and check_password_login(plain_password=password, hashed_password=user['password']):
            session['user_id'] = user['id']  # Oturum açıkken kullanıcıyı kimlik doğrulama
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"message": "Invalid username or password"})

# Kullanıcı çıkışı
@app.route('/logout', methods=['GET'])
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"})

# Kullanıcının kimliğini doğrulama
@app.route('/verify', methods=['GET'])
def verify():
    if 'user_id' in session:
        return jsonify({"authenticated": True})
    else:
        return jsonify({"authenticated": False})
products = Products()

# Ürünleri getirme
@app.route('/products', methods=['GET'])
def get_products():
    all_products = products.get_products()
    return jsonify(all_products)

# Yeni ürün ekleme
@app.route('/products', methods=['POST'])
def add_new_product():
    data = request.get_json()
    name = data['name']
    image = data['image']
    planting_date = data['planting_date']
    irrigation_frequency = data['irrigation_frequency']
    chemicals = data['chemicals']
    fertilizers = data['fertilizers']
    application_interval = data['application_interval']

    products.add_product(name, image, planting_date, irrigation_frequency, chemicals, fertilizers, application_interval)
    return jsonify({"message": "Product added successfully"})



if __name__ == '__main__':
    app.run(debug=True)