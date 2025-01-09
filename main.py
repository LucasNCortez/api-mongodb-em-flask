from flask import Flask, request, jsonify
from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import json

# Conexão com o MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client.test
collection = db.users

# Inicialização da aplicação Flask
app = Flask(__name__)

# Função auxiliar para serializar o usuário, convertendo ObjectId em string
def serialize_user(user):
    user["_id"] = str(user["_id"])
    return user

# Rota para criar um novo usuário
@app.route("/users", methods=["POST"])
def create_user():
    try:
        user_data = request.json
        result = collection.insert_one(user_data)
        # Retorna o ID do usuário criado com status 201
        return jsonify({"_id": str(result.inserted_id)}), 201
    except PyMongoError as e:
        return jsonify({"error": str(e)}), 500

# Rota para obter usuários com filtros e projeção
@app.route("/users", methods=["GET"])
def get_users():
    try:
        query_param = request.args.get("query")
        fields_param = request.args.get("fields")
        query = {}
        if query_param:
            query = json.loads(query_param)

        projection = {}
        if fields_param:
            fields = fields_param.split(',')
            for field in fields:
                if field.startswith('-'):
                    projection[field[1:]] = 0  # Excluir campo
                else:
                    projection[field] = 1  # Incluir campo

        users = list(collection.find(query, projection))
        return jsonify([serialize_user(user) for user in users]), 200
    except PyMongoError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rota para obter um usuário específico pelo ID
@app.route("/users/<string:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        # Busca o usuário na coleção pelo ID
        user = collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(serialize_user(user)), 200
    except PyMongoError as e:
        return jsonify({"error": str(e)}), 500
    except Exception:
        return jsonify({"error": "Invalid ID"}), 400

# Rota para atualizar um usuário existente
@app.route("/users/<string:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        user_data = request.json
        result = collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": user_data}
        )
        if result.matched_count == 0:
            return jsonify({"error": "User not found"}), 404
        # Retorna status 204 em caso de sucesso
        return '', 204
    except PyMongoError as e:
        return jsonify({"error": str(e)}), 500
    except Exception:
        return jsonify({"error": "Invalid ID"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
