from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

# Configuración de la base de datos MongoDB
app.config["MONGO_URI"] = 'mongodb+srv://almacenstack:gLTGWd6uK1Ugq6Vo@cluster0.u8ukb.mongodb.net/testing'

# "mongodb://localhost:27017/python1"

mongo = PyMongo(app)
# Definir una ruta de ejemplo
@app.route('/')
def home():
    return jsonify({"message": "Welcome to your backend with Flask!"})

@app.route('/all-tasks', methods=['GET'])
def allTasks():
    tasks = mongo.db.tasks.find()
    output = [{
        'id': str(t['_id']),
        'title': t['title'],
        'text': t['text'],
        'done': t['done']
    } for t in tasks]
    return jsonify(output)

# Post
@app.route('/add-task', methods=['POST'])
def addTask():
    # Obtener datos del request
    title = request.json['title']
    text = request.json['text']
    done = request.json['done']
    
    # Insertar en MongoDB
    register = {'title': title, 'text': text, 'done': done}
    mongo.db.tasks.insert_one({'title': title, 'text': text, 'done': done})
    
    return jsonify({'title': title, 'text': text, 'done': done}), 201

@app.route('/get-add-task/<title>/<text>')
def get_addTask(title, text):
    # Obtener datos del request
    # nombre = name
    # email = mail
    
    # Insertar en MongoDB
    mongo.db.tasks.insert_one({'title': title, 'text': text, 'done': False})
    
    return jsonify({'message': "Task añadida con éxito", "title": title, "text": text, "done": False}), 201

# Delete
@app.route('/del-task', methods=['DELETE'])
def delTask():
    title = request.json['title']
    mongo.db.tasks.delete_one({"title": title})
    return jsonify({'deleted': True})

@app.route('/get-del-task/<title>', methods=['GET'])
def get_delTask(title):
    mongo.db.tasks.delete_one({"title": title})
    return jsonify({'deleted': True})

# Update 
@app.route('/put-task', methods=['PUT'])
def putTask():
    title = request.json['title']
    data = request.get_json()
    updates = {}
    # if 'title' in data:
    #     updates['title'] = data['title']
        
    if 'text' in data:
        updates['text'] = data['text']

    if 'done' in data:
        updates['done'] = data['done']
        
    result = mongo.db.tasks.update_one(
        {'title': title,}, 
        {'$set': updates}
    )
    if result.matched_count > 0:
        return jsonify({"message": "Tarea actualizada exitosamente."}), 200
    else:
        return jsonify({"error": "No se encontró la tarea."}), 404

# @app.route('/comments', methods=['GET'])
# def getcomments():
#     comm = mongo.db.comments.find()
#     # output = [{'hello': hh['hello']} for hh in h]
#     output = [{
#         'id': str(user['_id']),
#         'name': user['name'], 
#         'email': user['email'],
#         'movie_id': str(user['movie_id']),
#         'text': user['text'],
#         'date': user['date'],
#     } for user in comm]
#     return jsonify(output)

# @app.route('/home', methods=['GET'])
# def gohome():
#     h = mongo.db.home.find()
#     output = [{'hello': hh['hello']} for hh in h]
#     return jsonify(output)

#__________
#Ruta para agregar un resgistro desde un GET
# @app.route('/addget/<nombre>/<email>',)
# def add_get(nombre, email):
#     # Obtener datos del request
#     # nombre = name
#     # email = mail
    
#     # Insertar en MongoDB
#     mongo.db.usuarios.insert_one({'nombre': nombre, 'email': email})
    
#     return jsonify({'message': "Usuario añadido con éxito", "nombre": nombre, "email": email}), 201
# #__________

# @app.route('/add', methods=['POST'])
# def add_user():
#     # Obtener datos del request
#     nombre = request.json['nombre']
#     email = request.json['email']
    
#     # Insertar en MongoDB
#     mongo.db.usuarios.insert_one({'nombre': nombre, 'email': email})
    
#     return jsonify(message="Usuario añadido con éxito"), 201

# @app.route('/usuarios', methods=['GET'])
# def get_users():
#     usuarios = mongo.db.usuarios.find()
#     output = [{'nombre': user['nombre'], 'email': user['email']} for user in usuarios]
    
#     return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)
