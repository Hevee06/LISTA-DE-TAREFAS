from app import db

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    custo = db.Column(db.Float, nullable=False)
    data_limite = db.Column(db.String(10), nullable=False)
    ordem = db.Column(db.Integer, unique=True, nullable=False)
