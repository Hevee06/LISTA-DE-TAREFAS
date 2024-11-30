from flask import render_template, redirect, url_for, request, flash, Blueprint

bp = Blueprint('main', __name__)

tarefas = [
    {'id': 1, 'nome': 'Tarefa 1', 'custo': 10.0, 'data_limite': '2024-12-01', 'ordem': 1},
    {'id': 2, 'nome': 'Tarefa 2', 'custo': 2000.0, 'data_limite': '2024-12-05', 'ordem': 2},
    {'id': 3, 'nome': 'Tarefa 3', 'custo': 15.0, 'data_limite': '2024-12-10', 'ordem': 3},
]

@bp.route('/')
def index():
    tarefas_ordenadas = sorted(tarefas, key=lambda t: t['ordem'])
    return render_template('index.html', tarefas=tarefas_ordenadas)

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    tarefa = next((t for t in tarefas if t['id'] == id), None)
    if not tarefa:
        flash('Tarefa não encontrada.', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        novo_nome = request.form['nome']
        
        if any(t['nome'] == novo_nome for t in tarefas) and novo_nome != tarefa['nome']:
            flash('Erro: Já existe uma tarefa com este nome.', 'error')
            return render_template('edit.html', tarefa=tarefa)

        tarefa['nome'] = novo_nome
        tarefa['custo'] = float(request.form['custo'])
        tarefa['data_limite'] = request.form['data_limite']
        
        flash('Tarefa editada com sucesso!')
        return redirect(url_for('main.index'))

    return render_template('edit.html', tarefa=tarefa)

@bp.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    global tarefas
    tarefas = [t for t in tarefas if t['id'] != id]
    flash('Tarefa excluída com sucesso!')
    return redirect(url_for('main.index'))

@bp.route('/incluir', methods=['GET', 'POST'])
def incluir():
    if request.method == 'POST':
        nome = request.form['nome']

        if any(t['nome'] == nome for t in tarefas):
            flash('Erro: Já existe uma tarefa com este nome.', 'error')
            return redirect(url_for('main.incluir'))

        custo = float(request.form['custo'])
        data_limite = request.form['data_limite']
        ordem = len(tarefas) + 1

        nova_tarefa = {'id': len(tarefas) + 1, 'nome': nome, 'custo': custo, 'data_limite': data_limite, 'ordem': ordem}
        tarefas.append(nova_tarefa)
        
        flash('Tarefa adicionada com sucesso!')
        return redirect(url_for('main.index'))

    return render_template('incluir.html')

@bp.route('/reordenar/<int:id>/<direcao>', methods=['POST'])
def reordenar(id, direcao):
    tarefa = next((t for t in tarefas if t['id'] == id), None)
    if not tarefa:
        flash('Tarefa não encontrada.', 'error')
        return redirect(url_for('main.index'))

    ordem_atual = tarefa['ordem']
    
    if direcao == 'subir':
        vizinha = next((t for t in tarefas if t['ordem'] == ordem_atual - 1), None)
        if vizinha:
            tarefa['ordem'], vizinha['ordem'] = vizinha['ordem'], tarefa['ordem']
    
    elif direcao == 'descer':
        vizinha = next((t for t in tarefas if t['ordem'] == ordem_atual + 1), None)
        if vizinha:
            tarefa['ordem'], vizinha['ordem'] = vizinha['ordem'], tarefa['ordem']

    tarefas.sort(key=lambda t: t['ordem'])
    flash('Ordem das tarefas alterada!')
    return redirect(url_for('main.index'))
