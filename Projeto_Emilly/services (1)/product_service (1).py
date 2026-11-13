from models.models import Produto, Maquiagem, db

def create_product(nome: str, marca: str = "", categoria: str = "Outros", tom_cor: str = "", 
                   descricao: str = "", preco: float = 0.0, quantidade: int = 0, usuario_id: int = 0) -> Produto:
    if not nome or preco is None or quantidade is None:
        raise ValueError("Por favor, preencha todos os campos obrigatórios.")

    produto = Produto(
        nome=nome,
        marca=marca or '',
        categoria=categoria or 'Outros',
        tom_cor=tom_cor or '',
        descricao=descricao or '',
        preco=float(preco),
        quantidade=int(quantidade),
        usuario_id=usuario_id
    )
    db.session.add(produto)
    db.session.commit()
    return produto

def get_products() -> list[Produto]:
    return db.session.query(Produto).limit(50).all()

def get_product_by_id(produto_id: int) -> Produto:
    return db.session.query(Produto).filter_by(id=produto_id).first()

def get_products_by_user(usuario_id: int) -> list[Produto]:
    return db.session.query(Produto).filter_by(usuario_id=usuario_id).all()

def update_product(produto_id: int, nome: str, marca: str = "", categoria: str = "Outros", 
                   tom_cor: str = "", descricao: str = "", preco: float = 0.0, quantidade: int = 0) -> Produto:
    produto = get_product_by_id(produto_id)
    if not produto:
        raise ValueError("Produto de maquiagem não encontrado.")

    if not nome or preco is None or quantidade is None:
        raise ValueError("Por favor, preencha todos os campos obrigatórios.")

    produto.nome = nome
    produto.marca = marca or ''
    produto.categoria = categoria or 'Outros'
    produto.tom_cor = tom_cor or ''
    produto.descricao = descricao or ''
    produto.preco = float(preco)
    produto.quantidade = int(quantidade)
    db.session.commit()
    return produto

def delete_product(produto_id: int) -> None:
    produto = get_product_by_id(produto_id)
    if not produto:
        raise ValueError("Produto de maquiagem não encontrado.")

    db.session.delete(produto)
    db.session.commit()

# Aliases de compatibilidade semântica para uso como Maquiagem
create_maquiagem = create_product
get_maquiagens = get_products
get_maquiagem_by_id = get_product_by_id
get_maquiagens_by_user = get_products_by_user
update_maquiagem = update_product
delete_maquiagem = delete_product
