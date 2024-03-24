from flask import Flask, request, jsonify,session
from flask_mysqldb import MySQL
import hashlib
app = Flask(__name__)
app.secret_key = 'ecommerce'
# MySQL bağlantısı
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Admin1224.'
app.config['MYSQL_DB'] = 'ecommerce'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Sonuçları sözlük olarak almak için

mysql = MySQL(app)

def check_password_login(plain_password, hashed_password):
 
    hashed_input_password = hashlib.sha256(plain_password.encode()).hexdigest()
    return hashed_input_password == hashed_password

# Yeni iş ilanı oluşturma
@app.route('/', methods=['GET'])
def open():
    return "Hello"


@app.route('/jobs', methods=['POST'])
def create_job():
    data = request.get_json()
    title = data['title']
    description = data['description']
    salary = data['salary']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO jobs (title, description, salary) VALUES (%s, %s, %s)", (title, description, salary))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "Job created successfully"})

# Tüm iş ilanlarını listeleme
@app.route('/jobs', methods=['GET'])
def get_jobs():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()
    cursor.close()
    return jsonify(jobs)

# Belirli bir iş ilanını getirme
@app.route('/jobs/<int:id>', methods=['GET'])
def get_job(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM jobs WHERE id = %s", (id,))
    job = cursor.fetchone()
    cursor.close()
    return jsonify(job)

# Bir iş ilanını güncelleme
@app.route('/jobs/<int:id>', methods=['PUT'])
def update_job(id):
    data = request.get_json()
    title = data['title']
    description = data['description']
    salary = data['salary']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE jobs SET title = %s, description = %s, salary = %s WHERE id = %s", (title, description, salary, id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "Job updated successfully"})

# Bir iş ilanını silme
@app.route('/jobs/<int:id>', methods=['DELETE'])
def delete_job(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM jobs WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "Job deleted successfully"})

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
        """print(check_password_login(user['password'], password))"""
       # print(user['password'],password,check_password_login(user['password'], password))
        if user and check_password_login(hashed_password=user['password'], plain_password=password):
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

if __name__ == '__main__':
    app.run(debug=True)
    
#functions
