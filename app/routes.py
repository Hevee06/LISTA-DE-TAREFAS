from flask import render_template, redirect, url_for, request, flash, Blueprint
from app import db
from app.models import Tarefa

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    tarefas = Tarefa.query.order_by(Tarefa.ordem).all()
    return render_template('index.html', tarefas=tarefas)

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    tarefa = Tarefa.query.get(id)
    if request.method == 'POST':
        novo_nome = request.form['nome']
        
        if Tarefa.query.filter_by(nome=novo_nome).first() and novo_nome != tarefa.nome:
            flash('Erro: Já existe uma tarefa com este nome.', 'error')
            return render_template('edit.html', tarefa=tarefa)

        tarefa.nome = novo_nome
        tarefa.custo = float(request.form['custo'])
        tarefa.data_limite = request.form['data_limite']
        
        db.session.commit()
        flash('Tarefa editada com sucesso!')
        return redirect(url_for('main.index'))
    
    return render_template('edit.html', tarefa=tarefa)

@bp.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    tarefa = Tarefa.query.get(id)
    db.session.delete(tarefa)
    db.session.commit()
    flash('Tarefa excluída com sucesso!')
    return redirect(url_for('main.index'))

@bp.route('/incluir', methods=['GET', 'POST'])
def incluir():
    if request.method == 'POST':
        nome = request.form['nome']

        if Tarefa.query.filter_by(nome=nome).first():
            flash('Erro: Já existe uma tarefa com este nome.', 'error')
            return redirect(url_for('main.incluir'))

        custo = float(request.form['custo'])
        data_limite = request.form['data_limite']
        ordem = Tarefa.query.count() + 1

        nova_tarefa = Tarefa(nome=nome, custo=custo, data_limite=data_limite, ordem=ordem)
        try:
            db.session.add(nova_tarefa)
            db.session.commit()
            flash('Tarefa adicionada com sucesso!')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao adicionar tarefa: ' + str(e), 'error')

    return render_template('incluir.html')

@bp.route('/reordenar/<int:id>/<direcao>', methods=['POST'])
def reordenar(id, direcao):
    tarefa = Tarefa.query.get(id)
    if not tarefa:
        flash('Tarefa não encontrada.', 'error')
        return redirect(url_for('main.index'))

    if direcao == 'subir':
        vizinha = Tarefa.query.filter(Tarefa.ordem < tarefa.ordem).order_by(Tarefa.ordem.desc()).first()
        if vizinha:
            tarefa.ordem, vizinha.ordem = vizinha.ordem, tarefa.ordem
    elif direcao == 'descer':
        vizinha = Tarefa.query.filter(Tarefa.ordem > tarefa.ordem).order_by(Tarefa.ordem).first()
        if vizinha:
            tarefa.ordem, vizinha.ordem = vizinha.ordem, tarefa.ordem

    db.session.commit()
    return redirect(url_for('main.index'))
