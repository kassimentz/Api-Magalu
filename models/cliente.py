from flask import request, url_for
from sql_alchemy import banco
from requests import post

MAILGUN_DOMAIN = 'sandboxde6b5cb3b89f44919f194e726522ed92.mailgun.org'
MAILGUN_API_KEY = 'c40694e37117df35eb9909e0ddb60523-1f1bd6a9-30b0b809'
FROM_TITLE = 'NO-REPLY'
FROM_EMAIL = 'no-reply@apiteste.com'

class ClienteModel(banco.Model):
    
    __tablename__ = 'clientes'
    
    cliente_id = banco.Column(banco.Integer, primary_key = True)
    nome = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    ativado = banco.Column(banco.Boolean, default=False)
    
    def __init__(self, nome, email, ativado):
        self.nome = nome
        self.email = email
        self.ativado = ativado
        
    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for('clienteconfirm', email=self.email)
        return post('https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN),
                    auth=('api', MAILGUN_API_KEY),
                    data={'from': '{}<{}>'.format(FROM_TITLE, FROM_EMAIL),
                          'to': self.email,
                          'subject':'Confirmacao de cadastro',
                          'text': 'Confirme seu cadastro clicando no link a seguir: {}'.format(link),
                          'html':'<html><p>\
                              Confirme seu cadastro clicando no link a seguir: <a href="{}"> CONFIRMAR EMAIL</a>\
                                  </p></html>'.format(link)
                        }
                    )
        
    
    def json(self):
        return {
            'cliente_id': self.cliente_id,
            'nome': self.nome,
            'email': self.email,
            'ativado': self.ativado
        }
        
    @classmethod    
    def find_cliente(cls, cliente_id):
        cliente = cls.query.filter_by(cliente_id=cliente_id).first()
        if cliente:
            return cliente
        return None
    
    @classmethod
    def find_by_nome(cls, nome):
        cliente = cls.query.filter_by(nome=nome).first()
        if cliente:
            return cliente
        return None
    
    @classmethod
    def find_by_email(cls, email):
        cliente = cls.query.filter_by(email=email).first()
        if cliente:
            return cliente
        return None
    
    
    def save_cliente(self):
        banco.session.add(self)
        banco.session.commit()
        
        
    def delete_cliente(self):
        banco.session.delete(self)
        banco.session.commit()
        
    def update_cliente(self, nome, email):
        self.nome = nome
        self.email = email
        