from datetime import timedelta
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
# Especificamos el tipo de base SQL y su ruta.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# TODO incluir la secret_key en un .env
app.secret_key = 'miguel'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
jwt = JWT(app, authenticate, identity)

# Función para customizar la respuesta de jwt
@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
                    'access_token': access_token.decode('utf-8'),
                    'user_id': identity.id
                   })


api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    # Declaramos aquí la importación porque los resources tb lo importarían
    # y creamos redundacia al importar desde varios sitios.
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
