from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

        # Migração automática para garantir as colunas de maquiagem na tabela produtos
        try:
            with db.engine.connect() as conn:
                res = conn.execute(text("PRAGMA table_info(produtos)")).fetchall()
                colunas = [row[1] for row in res]
                if colunas:
                    if 'marca' not in colunas:
                        conn.execute(text("ALTER TABLE produtos ADD COLUMN marca VARCHAR(100) DEFAULT ''"))
                    if 'categoria' not in colunas:
                        conn.execute(text("ALTER TABLE produtos ADD COLUMN categoria VARCHAR(50) DEFAULT 'Outros'"))
                    if 'tom_cor' not in colunas:
                        conn.execute(text("ALTER TABLE produtos ADD COLUMN tom_cor VARCHAR(50) DEFAULT ''"))
                    conn.commit()

                # Garante view/tabela de compatibilidade para consultas como 'maquiagens'
                conn.execute(text("CREATE VIEW IF NOT EXISTS maquiagens AS SELECT * FROM produtos"))
                conn.commit()
        except Exception:
            pass

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefone = db.Column(db.String(20), nullable=True)
    senha = db.Column(db.String(100), nullable=False)
    produtos = db.relationship('Produto', backref='usuario', lazy=True)

    @property
    def maquiagens(self):
        """Alias amigável para a lista de produtos de maquiagem do usuário."""
        return self.produtos

class Produto(db.Model):
    """Modelo representando produtos de Maquiagem."""
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)                         # Ex: Batom Matte, Base Velvet
    marca = db.Column(db.String(100), nullable=False, default='')           # Ex: MAC, Ruby Rose, Bruna Tavares
    categoria = db.Column(db.String(50), nullable=False, default='Outros')  # Ex: Lábios, Rosto, Olhos
    tom_cor = db.Column(db.String(50), nullable=True, default='')           # Ex: Nude Rosé, Bege Médio, Preto
    descricao = db.Column(db.String(255), nullable=True)                    # Acabamento, textura, fórmula
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

# Alias de classe para permitir importação e instanciação como 'Maquiagem'
Maquiagem = Produto
