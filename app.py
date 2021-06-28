from resources.produto import Produto, Produtos
from flask import Flask, jsonify
from flask_restful import Api
from resources.cliente import Cliente, ClienteConfirm, ClienteFavoritos, ClienteLogin, ClienteLogout, ClienteRegister, Clientes
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db' #se quiseer mudar o banco, muda apenas essa linha
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'

api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def cria_banco():
    banco.create_all()
 
@jwt.token_in_blocklist_loader
def verifica_blocklist(self, token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'message': 'Voce esta deslogado'}), 401
        
api.add_resource(Clientes, '/client')
api.add_resource(ClienteRegister, '/client')
api.add_resource(Cliente, '/client/<int:cliente_id>')
api.add_resource(ClienteFavoritos, '/client/<int:cliente_id>/lista/<int:product_id>')
api.add_resource(ClienteConfirm, '/confirmation/<string:email>')
api.add_resource(ClienteLogin, '/login')
api.add_resource(ClienteLogout, '/logout')
api.add_resource(Produtos, '/products')
api.add_resource(Produto, '/product/<int:id>')


if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)