from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from models import db, Usuario, Projeto, Inscricao, Evento, Doacao, Contato, Voluntario
from datetime import datetime, date
import os

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Configuração MySQL XAMPP
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/nacodes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'nacodes-secret-key-2025'

# Inicializar banco
db.init_app(app)


@app.route('/')
def index():
    """Página inicial -  kevin"""
    projetos_ativos = Projeto.query.filter_by(status='ativo').limit(3).all()
    eventos_proximos = Evento.query.filter(
        Evento.data_evento >= datetime.now(),
        Evento.publico == True
    ).order_by(Evento.data_evento).limit(3).all()

    return render_template('index.html',
                           projetos=projetos_ativos,
                           eventos=eventos_proximos)


# === NOVAS ROTAS  ===

@app.route('/sobre')
def sobre():
    """Página Sobre Nós - baseada no design do Figma"""
    return render_template('sobre.html')


@app.route('/educacao')
def educacao():
    """Página Educação (antiga Cursos) - foco na creche escola"""
    projetos_educacionais = Projeto.query.filter_by(status='ativo').all()
    return render_template('educacao.html', projetos=projetos_educacionais)


@app.route('/servicos')
def servicos():
    """Página de Serviços oferecidos pela ONG"""
    return render_template('servicos.html')


@app.route('/doacao')
def doacao():
    """Página de Doação - baseada no design do Figma"""
    return render_template('doacao.html')


@app.route('/unidade/<nome>')
def unidade_detalhe(nome):
    """Página específica de cada unidade"""
    unidades_info = {
        'dende': {
            'nome': 'Unidade Dendê',
            'endereco': 'Morro do Dendê, Rio de Janeiro - RJ',
            'servicos': ['Aula de judô', 'Aula de ballet', 'Brinquedoteca', 'Psicomotricidade', 'Ambiente estruturado'],
            'descricao': 'Nossa unidade no Morro do Dendê oferece um ambiente acolhedor e estruturado para o desenvolvimento das crianças.'
        },
        'jacarezinho': {
            'nome': 'Unidade Jacarézinho',
            'endereco': 'Jacarézinho, Rio de Janeiro - RJ',
            'servicos': ['Educação infantil', 'Atividades recreativas', 'Reforço escolar'],
            'descricao': 'No Jacarézinho, promovemos educação de qualidade e atividades que estimulam o desenvolvimento.'
        },
        'tuiuti': {
            'nome': 'Unidade Tuiuti',
            'endereco': 'Morro do Tuiuti, Rio de Janeiro - RJ',
            'servicos': ['Creche', 'Atividades culturais', 'Apoio pedagógico'],
            'descricao': 'A unidade do Tuiuti é um espaço de aprendizado e crescimento para toda a comunidade.'
        }
    }

    unidade = unidades_info.get(nome.lower())
    if not unidade:
        flash('Unidade não encontrada!', 'error')
        return redirect(url_for('index'))

    return render_template('unidade.html', unidade=unidade)


# === ROTAS EXISTENTES (mantidas) ===

@app.route('/projetos')
def projetos():
    """Lista todos os projetos ativos"""
    projetos = Projeto.query.filter_by(status='ativo').all()
    return render_template('projetos.html', projetos=projetos)


@app.route('/projeto/<int:id>')
def projeto_detalhe(id):
    """Detalhes de um projeto específico"""
    projeto = Projeto.query.get_or_404(id)
    return render_template('projeto_detalhe.html', projeto=projeto)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email=email, ativo=True).first()

        if usuario and usuario.check_senha(senha):
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            session['usuario_tipo'] = usuario.tipo_usuario

            flash(f'Bem-vindo(a), {usuario.nome}!', 'success')

            # Redirecionar baseado no tipo de usuário
            if usuario.tipo_usuario == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                # Usuário comum vai para o perfil ou página que estava tentando acessar
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('perfil_usuario'))
        else:
            flash('Email ou senha incorretos!', 'error')

    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form.get('telefone', '')
        senha = request.form['senha']
        confirma_senha = request.form['confirma_senha']

        # Validações básicas
        if senha != confirma_senha:
            flash('Senhas não coincidem!', 'error')
            return render_template('cadastro.html')

        if Usuario.query.filter_by(email=email).first():
            flash('Email já cadastrado!', 'error')
            return render_template('cadastro.html')

        # Criar usuário
        usuario = Usuario(
            nome=nome,
            email=email,
            telefone=telefone
        )
        usuario.set_senha(senha)

        db.session.add(usuario)
        db.session.commit()

        flash('Cadastro realizado com sucesso! Você já está logado.', 'success')

        # Fazer login automático após cadastro
        session['usuario_id'] = usuario.id
        session['usuario_nome'] = usuario.nome
        session['usuario_tipo'] = usuario.tipo_usuario

        return redirect(url_for('perfil_usuario'))

    return render_template('cadastro.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))


@app.route('/perfil')
def perfil_usuario():
    """Área do usuário logado"""
    if 'usuario_id' not in session:
        flash('Faça login para acessar seu perfil!', 'warning')
        return redirect(url_for('login'))

    usuario = Usuario.query.get(session['usuario_id'])
    inscricoes = Inscricao.query.filter_by(usuario_id=usuario.id).all()
    doacoes = Doacao.query.filter_by(usuario_id=usuario.id).all()

    return render_template('perfil.html',
                           usuario=usuario,
                           inscricoes=inscricoes,
                           doacoes=doacoes)


@app.route('/inscrever/<int:projeto_id>', methods=['GET', 'POST'])
def inscrever_projeto(projeto_id):
    """Inscrição em projeto específico"""
    if 'usuario_id' not in session:
        flash('Faça login para se inscrever!', 'warning')
        return redirect(url_for('login'))

    projeto = Projeto.query.get_or_404(projeto_id)
    usuario_id = session['usuario_id']

    # Verificar se já está inscrito
    inscricao_existente = Inscricao.query.filter_by(
        usuario_id=usuario_id,
        projeto_id=projeto_id
    ).first()

    if inscricao_existente:
        flash('Você já está inscrito neste projeto!', 'warning')
        return redirect(url_for('projeto_detalhe', id=projeto_id))

    if request.method == 'POST':
        inscricao = Inscricao(
            usuario_id=usuario_id,
            projeto_id=projeto_id,
            nome_responsavel=request.form.get('nome_responsavel'),
            telefone_responsavel=request.form.get('telefone_responsavel'),
            observacoes=request.form.get('observacoes')
        )

        db.session.add(inscricao)
        db.session.commit()

        flash('Inscrição realizada com sucesso! Aguarde aprovação.', 'success')
        return redirect(url_for('perfil_usuario'))

    return render_template('inscricao.html', projeto=projeto)


@app.route('/voluntario', methods=['GET', 'POST'])
def cadastro_voluntario():
    """Cadastro como voluntário"""
    if 'usuario_id' not in session:
        flash('Faça login para se voluntariar!', 'warning')
        return redirect(url_for('login'))

    usuario_id = session['usuario_id']

    # Verificar se já é voluntário
    voluntario_existente = Voluntario.query.filter_by(usuario_id=usuario_id).first()

    if request.method == 'POST':
        if voluntario_existente:
            # Atualizar dados
            voluntario_existente.areas_interesse = request.form['areas_interesse']
            voluntario_existente.disponibilidade = request.form['disponibilidade']
            voluntario_existente.experiencia = request.form['experiencia']
            voluntario_existente.unidade_preferencia = request.form['unidade_preferencia']
            voluntario_existente.ativo = True
        else:
            # Criar novo
            voluntario = Voluntario(
                usuario_id=usuario_id,
                areas_interesse=request.form['areas_interesse'],
                disponibilidade=request.form['disponibilidade'],
                experiencia=request.form['experiencia'],
                unidade_preferencia=request.form['unidade_preferencia']
            )
            db.session.add(voluntario)

        db.session.commit()
        flash('Cadastro de voluntário atualizado com sucesso!', 'success')
        return redirect(url_for('perfil_usuario'))

    return render_template('voluntario.html', voluntario=voluntario_existente)


@app.route('/contato', methods=['GET', 'POST'])
def contato():
    """Formulário de contato"""
    if request.method == 'POST':
        contato = Contato(
            nome=request.form['nome'],
            email=request.form['email'],
            telefone=request.form.get('telefone'),
            assunto=request.form['assunto'],
            mensagem=request.form['mensagem']
        )

        db.session.add(contato)
        db.session.commit()

        flash('Mensagem enviada com sucesso!', 'success')
        return redirect(url_for('contato'))

    return render_template('contato.html')


@app.route('/doacoes', methods=['GET', 'POST'])
def doacoes():
    """Página de doações com formulário"""
    if request.method == 'POST':
        doacao = Doacao(
            usuario_id=session.get('usuario_id'),
            nome_doador=request.form['nome_doador'],
            email_doador=request.form['email_doador'],
            telefone_doador=request.form.get('telefone_doador'),
            tipo_doacao=request.form['tipo_doacao'],
            valor=request.form.get('valor') if request.form['tipo_doacao'] == 'dinheiro' else None,
            descricao=request.form.get('descricao'),
            projeto_destino=request.form.get('projeto_destino', 'Geral')
        )

        db.session.add(doacao)
        db.session.commit()

        flash('Doação registrada com sucesso!', 'success')
        return redirect(url_for('doacao'))  # Mudança aqui: redireciona para /doacao

    return render_template('doacoes.html')


@app.route('/eventos')
def eventos():
    """Lista de eventos públicos"""
    eventos = Evento.query.filter(
        Evento.publico == True,
        Evento.data_evento >= datetime.now()
    ).order_by(Evento.data_evento).all()

    return render_template('eventos.html', eventos=eventos)


# --- ÁREA ADMINISTRATIVA ---

@app.route('/admin')
def admin_dashboard():
    """Dashboard administrativo"""
    if session.get('usuario_tipo') != 'admin':
        flash('Acesso negado!', 'error')
        return redirect(url_for('index'))

    # Estatísticas básicas
    stats = {
        'total_usuarios': Usuario.query.count(),
        'inscricoes_pendentes': Inscricao.query.filter_by(status='pendente').count(),
        'projetos_ativos': Projeto.query.filter_by(status='ativo').count(),
        'contatos_nao_respondidos': Contato.query.filter_by(respondida=False).count(),
        'voluntarios_ativos': Voluntario.query.filter_by(ativo=True).count()
    }

    return render_template('admin/dashboard.html', stats=stats)


@app.route('/admin/inscricoes')
def admin_inscricoes():
    """Gerenciar inscrições"""
    if session.get('usuario_tipo') != 'admin':
        flash('Acesso negado!', 'error')
        return redirect(url_for('index'))

    inscricoes = Inscricao.query.order_by(Inscricao.data_inscricao.desc()).all()
    return render_template('admin/inscricoes.html', inscricoes=inscricoes)


@app.route('/admin/aprovar_inscricao/<int:id>')
def aprovar_inscricao(id):
    """Aprovar inscrição"""
    if session.get('usuario_tipo') != 'admin':
        return jsonify({'error': 'Acesso negado'}), 403

    inscricao = Inscricao.query.get_or_404(id)
    inscricao.status = 'aprovada'
    inscricao.data_resposta = datetime.utcnow()

    # Atualizar vagas do projeto
    projeto = inscricao.projeto
    projeto.vagas_ocupadas += 1

    db.session.commit()

    flash('Inscrição aprovada com sucesso!', 'success')
    return redirect(url_for('admin_inscricoes'))


# Corrigir formulário de inscrição da home COM TURMA
@app.route('/inscricao_rapida', methods=['POST'])
def inscricao_rapida():
    """Inscrição rápida do formulário da home"""
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        unidade = request.form['unidade']
        turma = request.form['turma']  # NOVO CAMPO

        # Se usuário não estiver logado, redireciona para cadastro
        if 'usuario_id' not in session:
            flash('Faça login ou cadastre-se primeiro para se inscrever!', 'warning')
            return redirect(url_for('cadastro'))

        # Buscar projeto da creche na unidade selecionada
        projeto = Projeto.query.filter_by(
            nome='Creche Educacional',
            unidade=unidade,
            status='ativo'
        ).first()

        if not projeto:
            flash('No momento não temos vagas disponíveis nesta unidade.', 'warning')
            return redirect(url_for('index'))

        # Verificar se já está inscrito
        inscricao_existente = Inscricao.query.filter_by(
            usuario_id=session['usuario_id'],
            projeto_id=projeto.id
        ).first()

        if inscricao_existente:
            flash('Você já possui uma inscrição para esta unidade!', 'warning')
            return redirect(url_for('index'))

        # Criar inscrição COM INFO DA TURMA
        inscricao = Inscricao(
            usuario_id=session['usuario_id'],
            projeto_id=projeto.id,
            observacoes=f"Inscrição via formulário da home - Nome criança: {nome} - Telefone: {telefone} - Turma solicitada: {turma}"
        )

        db.session.add(inscricao)
        db.session.commit()

        flash(f'Inscrição realizada com sucesso para {turma}! Aguarde nosso contato.', 'success')
        return redirect(url_for('index'))


# Corrigir links dos botões do carrossel
@app.route('/unidades')
def unidades():
    """Página listando todas as unidades"""
    unidades_info = {
        'dende': {
            'nome': 'Unidade Dendê',
            'endereco': 'Morro do Dendê, Rio de Janeiro - RJ',
            'servicos': ['Aula de judô', 'Aula de ballet', 'Brinquedoteca', 'Psicomotricidade'],
            'descricao': 'Nossa unidade no Morro do Dendê oferece um ambiente acolhedor e estruturado.'
        },
        'jacarezinho': {
            'nome': 'Unidade Jacarézinho',
            'endereco': 'Jacarézinho, Rio de Janeiro - RJ',
            'servicos': ['Curso de informática', 'Educação infantil', 'Reforço escolar'],
            'descricao': 'No Jacarézinho, promovemos educação de qualidade e atividades de desenvolvimento.'
        },
        'tuiuti': {
            'nome': 'Unidade Tuiuti',
            'endereco': 'Morro do Tuiuti, Rio de Janeiro - RJ',
            'servicos': ['Oficina de arte', 'Creche', 'Atividades culturais'],
            'descricao': 'A unidade do Tuiuti é um espaço de aprendizado e crescimento comunitário.'
        },
        'mare': {
            'nome': 'Unidade Maré',
            'endereco': 'Parque União (Maré), Rio de Janeiro - RJ',
            'servicos': ['Projetos sociais', 'Atividades juvenis', 'Apoio familiar'],
            'descricao': 'Na Maré, atuamos com projetos de desenvolvimento social e cultural.'
        },
        'bancarios': {
            'nome': 'Unidade Bancários',
            'endereco': 'Bancários (Ilha do Governador), Rio de Janeiro - RJ',
            'servicos': ['Qualificação profissional', 'Cursos técnicos', 'Empreendedorismo'],
            'descricao': 'Nos Bancários, focamos na capacitação profissional e geração de renda.'
        }
    }
    return render_template('unidades.html', unidades=unidades_info)


def criar_tabelas():
    """Criar todas as tabelas no banco"""
    with app.app_context():
        db.create_all()

        # Criar usuário admin padrão se não existir
        admin = Usuario.query.filter_by(email='admin@nacodes.com').first()
        if not admin:
            admin = Usuario(
                nome='Administrador NACODES',
                email='admin@nacodes.com',
                tipo_usuario='admin'
            )
            admin.set_senha('admin123')
            db.session.add(admin)

        # Criar alguns projetos de exemplo
        if Projeto.query.count() == 0:
            projetos_exemplo = [
                Projeto(
                    nome='Creche Educacional',
                    descricao='Educação infantil para crianças de 2 a 5 anos',
                    unidade='Dendê',
                    idade_minima=2,
                    idade_maxima=5,
                    vagas_disponiveis=30,
                    data_inicio=date(2025, 2, 1),
                    data_fim=date(2025, 12, 15)
                ),
                Projeto(
                    nome='Curso de Informática',
                    descricao='Curso básico de informática para jovens',
                    unidade='Jacarezinho',
                    idade_minima=14,
                    idade_maxima=25,
                    vagas_disponiveis=20,
                    data_inicio=date(2025, 3, 1),
                    data_fim=date(2025, 8, 30)
                ),
                Projeto(
                    nome='Oficina de Arte',
                    descricao='Desenvolvimento de habilidades artísticas',
                    unidade='Tuiuti',
                    idade_minima=8,
                    idade_maxima=16,
                    vagas_disponiveis=15,
                    data_inicio=date(2025, 2, 15),
                    data_fim=date(2025, 11, 30)
                )
            ]

            for projeto in projetos_exemplo:
                db.session.add(projeto)

        db.session.commit()
        print("✅ Tabelas criadas e dados de exemplo inseridos!")


if __name__ == '__main__':
    criar_tabelas()
    app.run(debug=True, host='127.0.0.1', port=5000)
