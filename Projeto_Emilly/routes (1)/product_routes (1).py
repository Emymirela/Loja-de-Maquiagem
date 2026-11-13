from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from services.product_service import (create_product, get_products, get_product_by_id,
                                      get_products_by_user, update_product, delete_product)
from .auth_decorator import login_required

product_bp = Blueprint('product', __name__, url_prefix='/produto', template_folder='templates')

@product_bp.route('/cadastro', methods=['GET', 'POST'])
@login_required
def cadastrar_produto():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        marca = request.form.get('marca', '').strip()
        categoria = request.form.get('categoria', '').strip()
        tom_cor = request.form.get('tom_cor', '').strip()
        descricao = request.form.get('descricao', '').strip()
        preco = request.form.get('preco')
        quantidade = request.form.get('quantidade')
        usuario_id = session.get('user_id')

        try:
            create_product(
                nome=nome,
                marca=marca,
                categoria=categoria,
                tom_cor=tom_cor,
                descricao=descricao,
                preco=float(preco),
                quantidade=int(quantidade),
                usuario_id=usuario_id
            )
            flash("Produto de maquiagem cadastrado com sucesso!", "success")
            return redirect(url_for('product.listar_produtos'))
        except (ValueError, TypeError) as e:
            flash(f"Erro ao cadastrar produto: {e}", "danger")

    return render_template('cadastro_produto.html')

@product_bp.route('/listar', methods=['GET'])
@login_required
def listar_produtos():
    usuario_id = session.get('user_id')
    produtos = get_products_by_user(usuario_id)
    return render_template('listar_produtos.html', produtos=produtos)

@product_bp.route('/editar/<int:produto_id>', methods=['GET', 'POST'])
@login_required
def editar_produto(produto_id):
    produto = get_product_by_id(produto_id)
    if not produto:
        flash("Produto de maquiagem não encontrado.", "danger")
        return redirect(url_for('product.listar_produtos'))

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        marca = request.form.get('marca', '').strip()
        categoria = request.form.get('categoria', '').strip()
        tom_cor = request.form.get('tom_cor', '').strip()
        descricao = request.form.get('descricao', '').strip()
        preco = request.form.get('preco')
        quantidade = request.form.get('quantidade')

        try:
            update_product(
                produto_id=produto_id,
                nome=nome,
                marca=marca,
                categoria=categoria,
                tom_cor=tom_cor,
                descricao=descricao,
                preco=float(preco),
                quantidade=int(quantidade)
            )
            flash("Produto de maquiagem atualizado com sucesso!", "success")
            return redirect(url_for('product.listar_produtos'))
        except (ValueError, TypeError) as e:
            flash(f"Erro ao atualizar produto: {e}", "danger")

    return render_template('editar_produto.html', produto=produto)

@product_bp.route('/deletar/<int:produto_id>', methods=['GET', 'POST'])
@login_required
def deletar_produto(produto_id):
    try:
        delete_product(produto_id)
        flash("Produto de maquiagem deletado com sucesso.", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for('product.listar_produtos'))
