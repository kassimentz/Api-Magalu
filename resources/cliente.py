from models.produtos_favoritos import ProdutosFavoritosModel
from models.produto import ProdutoModel
from models.cliente import ClienteModel
from flask import make_response, render_template
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
import traceback
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('nome', type=str)
atributos.add_argument('email', type=str, required=True, help="O campo 'email' nao pode ser deixado em branco")
atributos.add_argument('ativado', type=bool)

class Clientes(Resource):
    def get(self):
        
        clientes = []
        for cliente in ClienteModel.query.all():
            produtos_cliente = []
            favoritos = ProdutosFavoritosModel.find_produtos_by_cliente(cliente.cliente_id)
            if favoritos:
                for favorito in favoritos:
                    produto = ProdutoModel.find_produto(favorito.produto_id)
                    produtos_cliente.append(produto.json())
                    
            cli = {
                'cliente_id': cliente.cliente_id,
                'nome': cliente.nome,
                'email': cliente.email,
                'ativado': cliente.ativado,
                'favoritos': produtos_cliente
            }
            
            clientes.append(cli)
        return {'clientes': clientes}
        

    
class Cliente(Resource):
    
    def get(self, cliente_id):
        cliente = ClienteModel.find_cliente(cliente_id)
        if cliente:
            #return cliente.json()
            produtos_cliente = []
            favoritos = ProdutosFavoritosModel.find_produtos_by_cliente(cliente_id)
            if favoritos:
                for favorito in favoritos:
                    produto = ProdutoModel.find_produto(favorito.produto_id)
                    produtos_cliente.append(produto.json())
            
            return {
                    'cliente_id': cliente_id,
                    'nome': cliente.nome,
                    'email': cliente.email,
                    'ativado': cliente.ativado,
                    'favoritos': produtos_cliente
                }, 200
                
                
        return {'message' : 'Usuario nao encontrado'}, 404
    
    @jwt_required()
    def put(self, cliente_id):
        dados = atributos.parse_args()

        cliente_encontrado = ClienteModel.find_cliente(cliente_id)
        if cliente_encontrado:
            cliente_encontrado.update_cliente(dados.get('nome'), dados.get('email'))
            cliente_encontrado.save_cliente()
            return cliente_encontrado.json(), 200
        cliente = ClienteModel(**dados)
        try:
            cliente.sava_cliente()
        except:
            return {'message': 'Um erro interno aconteceu tentando salvar o cliente'}, 500 #internal server error
        return cliente.json(), 201
            
    @jwt_required()
    def delete(self, cliente_id):
        cliente = ClienteModel.find_cliente(cliente_id)
        if cliente:
            try:
                cliente.delete_cliente()
            except:
                return {'message': 'Um erro interno aconteceu tentando deletar o cliente'}, 500 #internal server error
            return {'message': 'Cliente deletado'}        
        return {'message': 'Cliente não encontrado'}
    
class ClienteRegister(Resource):
    #/clientes
    def post(self):
        dados = atributos.parse_args()
        
        if not dados.get('email') or dados.get('email') is None:
            return {"message": "o campo email deve ser informado"}, 400
        
        if ClienteModel.find_by_email(dados['email']):
            return {"message": "o email '{}' ja existe".format(dados['email'])}, 400
        
        
        cliente = ClienteModel(**dados)
        cliente.ativado = False
        try:
            cliente.save_cliente()
            cliente.send_confirmation_email()
        except:
            cliente.delete_cliente()
            traceback.print_exc()
            return {'message': 'Um erro interno aconteceu tentando salvar o cliente'}, 500 #internal server error
        
        return {'message': 'Cliente criado com sucesso'}, 201
        
class ClienteLogin(Resource):
    
    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        
        cliente = ClienteModel.find_by_email(dados['email'])
        if cliente:
            if cliente.ativado: 
                token_de_acesso = create_access_token(identity=cliente.cliente_id)
                return {'access_token': token_de_acesso},200
            return {'message': 'Cliente nao confirmado'}, 400
        return {'message': 'Email nao encontrado'}, 401
    
class ClienteLogout(Resource):
    
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] #JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Deslogado com sucesso'}, 200
    
class ClienteConfirm(Resource):
    #raiz_do_site/confirmacao/{email}
    @classmethod
    def get(cls, email):
        cliente = ClienteModel.find_by_email(email)
        
        if not cliente:
            return {"message": "Cliente '{}' nao encontrado".format(email)}, 404
        
        cliente.ativado = True
        cliente.save_cliente()
        
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('cliente_confirm.html', email=cliente.email, cliente=cliente.nome), 200, headers)
    
    
class ClienteFavoritos(Resource):
    #/cliente/{client_id}/lista/{product_id}
    @jwt_required()
    def post(self, cliente_id, product_id):
        
        cliente = ClienteModel.find_cliente(cliente_id)
        if cliente:
            produto = ProdutoModel.find_produto(product_id)
            if produto is None:
                return {"message": "o produto id '{}' nao existe na base de dados".format(product_id)}, 400
            
            produto_existente = ProdutosFavoritosModel.find_produtos_by_cliente_and_product(cliente_id, product_id)
            if produto_existente:
                return {"message": "o produto id '{}' ja esta nos favoritos deste cliente".format(product_id)}, 400
            else:
                novo_favorito = ProdutosFavoritosModel(cliente_id, product_id)
                try:
                    novo_favorito.save_produto_favorito()
                except:
                    return {'message': 'Um erro interno aconteceu tentando adicionar o produto'}, 500 #internal server error
                
            return {'message': 'Produto adicionado com sucesso'}, 201
        else:
            return {"message": "Cliente id '{}' nao existe na base de dados".format(product_id)}, 400
            

        
            
        
            
        
            
