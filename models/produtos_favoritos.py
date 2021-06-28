from sql_alchemy import banco
from sqlalchemy import and_

class ProdutosFavoritosModel(banco.Model):
    
    __tablename__ = 'produtos_favoritos'
    
    id = banco.Column(banco.Integer, primary_key = True)
    cliente_id = banco.Column(banco.Integer)
    produto_id = banco.Column(banco.Integer)
    
    
    def __init__(self, cliente_id, produto_id):
        self.cliente_id = cliente_id
        self.produto_id = produto_id

        
    def json(self):
        return {
            'cliente_id': self.cliente_id,
            'produto_id': self.produto_id,
        }
        
    @classmethod    
    def find_produtos_by_cliente(cls, cliente_id):
        produtos = cls.query.filter_by(cliente_id=cliente_id).all()
        if produtos:
            return produtos
        return None
    
    @classmethod    
    def find_produtos_by_cliente_and_product(cls, cliente_id, produto_id):
        cliente = cls.query.filter_by(cliente_id=cliente_id).all()
        if cliente:
            produtos = cls.query.filter_by(cliente_id=cliente_id, produto_id=produto_id).all()
            if produtos:
                return produtos
            return None
        else:
            return None
    
    def save_produto_favorito(self):
        banco.session.add(self)
        banco.session.commit()
        
        