from sql_alchemy import banco

class ProdutoModel(banco.Model):
    
    __tablename__ = 'produtos'
    
    id = banco.Column(banco.Integer, primary_key = True)
    price = banco.Column(banco.Float(precision=2))
    image = banco.Column(banco.String(400))
    brand = banco.Column(banco.String(100))
    title = banco.Column(banco.String(100))
    reviewScore = banco.Column(banco.Float(precision=2))
    
    def __init__(self, id, price, image, brand, title, reviewScore):
        self.id = id
        self.price = price
        self.image = image
        self.brand = brand
        self.title = title
        self.reviewScore = reviewScore
        
    def json(self):
        return {
            'id': self.id,
            'price': self.price,
            'image': self.image, 
            'brand': self.brand,
            'title': self.title,
            'reviewScore': self.reviewScore
        }
        
    @classmethod    
    def find_produto(cls, id):
        produto = cls.query.filter_by(id=id).first()
        if produto:
            return produto
        return None
    
    def save_produto(self):
        banco.session.add(self)
        banco.session.commit()
        
    def update_produto(self, price, image, brand, title, reviewScore):
        self.price = price
        self.image = image
        self.brand = brand
        self.title = title
        self.reviewScore = reviewScore
        
    def delete_produto(self):
        banco.session.delete(self)
        banco.session.commit()