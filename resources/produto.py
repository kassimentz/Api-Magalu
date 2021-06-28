from models.produto import ProdutoModel
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
import sqlite3

#/product/?page=10
path_params = reqparse.RequestParser()
path_params.add_argument('page', type=float)

class Produtos(Resource):
    def get(self):
        dados = path_params.parse_args()
        if dados.get('page'):
            per_page = 10 #assumi que cada pagina contem 10 itens
            filtrados = ProdutoModel.query.paginate(dados.get('page'), per_page, error_out=False)
            return {'products': [produto.json() for produto in filtrados.items]}
        else:
            return {'products': [produto.json() for produto in ProdutoModel.query.all()]}
    
    
    
class Produto(Resource):
    
    atributos = reqparse.RequestParser()
    atributos.add_argument('price', type=float, required=True, help="O campo 'price' deve ser informado")
    atributos.add_argument('image', type=str, required=True, help="o campo 'image' deve ser informado")
    atributos.add_argument('brand', type=str)
    atributos.add_argument('title', type=str, required=True, help="O campo 'title' deve ser informado")
    atributos.add_argument('reviewScore', type=float)
    
        
    def get(self, id):
        produto = ProdutoModel.find_produto(id)
        if produto:
            return produto.json()
        return {'message' : 'Produto não encontrado'}, 404
            
    @jwt_required()
    def post(self, id):
        
        if ProdutoModel.find_produto(id):
            return {"message":"Produto ID '{}' ja existe.".format(id)}, 400
        
        dados = Produto.atributos.parse_args()
        produto = ProdutoModel(id, **dados)
        
        try:
            produto.save_produto()
        except:
            return {'message': 'Um erro interno ocorreu enquanto tentava salvar o produto'}, 500 #internal server error
        return produto.json(), 200
    
    @jwt_required()
    def put(self, id):
        dados = Produto.atributos.parse_args()
        produto_encontrado = ProdutoModel.find_produto(id)
        if produto_encontrado:
            produto_encontrado.update_produto(**dados)
            produto_encontrado.save_produto()
            return produto_encontrado.json(), 200
        produto = ProdutoModel(id, **dados)
        try:
            produto.save_produto()
        except:
            return {'message': 'Um erro interno ocorreu enquanto tentava salvar o produto'}, 500 #internal server error
        return produto.json(), 201
    
    @jwt_required()
    def delete(self, id):
        produto = ProdutoModel.find_produto(id)
        if produto:
            try:
                produto.delete_produto()
            except:
                return {'message': 'Um erro interno ocorreu enquanto tentava deletar o produto'}, 500 #internal server error
            return {'message': 'Produto deletado'}        
        return {'message': 'Produto nao encontrado'}