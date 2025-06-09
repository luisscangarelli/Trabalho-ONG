from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(20))
    tipo_usuario = db.Column(db.String(20), default='usuario')  # 'usuario' ou 'admin'
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    inscricoes = db.relationship('Inscricao', backref='usuario', lazy=True)
    doacoes = db.relationship('Doacao', backref='usuario', lazy=True)

    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha, senha)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'tipo_usuario': self.tipo_usuario,
            'ativo': self.ativo,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None
        }


class Projeto(db.Model):
    __tablename__ = 'projetos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    unidade = db.Column(db.String(50))  # Dendê, Jacarezinho, etc.
    idade_minima = db.Column(db.Integer)
    idade_maxima = db.Column(db.Integer)
    vagas_disponiveis = db.Column(db.Integer, default=0)
    vagas_ocupadas = db.Column(db.Integer, default=0)
    data_inicio = db.Column(db.Date)
    data_fim = db.Column(db.Date)
    status = db.Column(db.String(20), default='ativo')  # 'ativo', 'inativo', 'finalizado'
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    inscricoes = db.relationship('Inscricao', backref='projeto', lazy=True)

    @property
    def vagas_restantes(self):
        return self.vagas_disponiveis - self.vagas_ocupadas

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'unidade': self.unidade,
            'idade_minima': self.idade_minima,
            'idade_maxima': self.idade_maxima,
            'vagas_disponiveis': self.vagas_disponiveis,
            'vagas_ocupadas': self.vagas_ocupadas,
            'vagas_restantes': self.vagas_restantes,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'data_fim': self.data_fim.isoformat() if self.data_fim else None,
            'status': self.status
        }


class Inscricao(db.Model):
    __tablename__ = 'inscricoes'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable=False)

    nome_responsavel = db.Column(db.String(100))  # Para menores de idade
    telefone_responsavel = db.Column(db.String(20))
    observacoes = db.Column(db.Text)

    status = db.Column(db.String(20), default='pendente')  # 'pendente', 'aprovada', 'rejeitada'
    data_inscricao = db.Column(db.DateTime, default=datetime.utcnow)
    data_resposta = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'usuario': self.usuario.nome if self.usuario else None,
            'projeto': self.projeto.nome if self.projeto else None,
            'nome_responsavel': self.nome_responsavel,
            'telefone_responsavel': self.telefone_responsavel,
            'observacoes': self.observacoes,
            'status': self.status,
            'data_inscricao': self.data_inscricao.isoformat() if self.data_inscricao else None,
            'data_resposta': self.data_resposta.isoformat() if self.data_resposta else None
        }


class Evento(db.Model):
    __tablename__ = 'eventos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    data_evento = db.Column(db.DateTime, nullable=False)
    local = db.Column(db.String(200))
    unidade = db.Column(db.String(50))
    tipo = db.Column(db.String(50))  # 'workshop', 'festa', 'reunião', etc.
    publico = db.Column(db.Boolean, default=True)  # True = público, False = interno
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'data_evento': self.data_evento.isoformat() if self.data_evento else None,
            'local': self.local,
            'unidade': self.unidade,
            'tipo': self.tipo,
            'publico': self.publico
        }


class Doacao(db.Model):
    __tablename__ = 'doacoes'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)  # Pode ser anônima

    # Dados da doação
    nome_doador = db.Column(db.String(100))  # Para doações anônimas
    email_doador = db.Column(db.String(100))
    telefone_doador = db.Column(db.String(20))

    tipo_doacao = db.Column(db.String(20), nullable=False)  # 'dinheiro', 'material', 'alimento'
    valor = db.Column(db.Numeric(10, 2))  # Para doações em dinheiro
    descricao = db.Column(db.Text)  # Descrição de materiais/alimentos

    projeto_destino = db.Column(db.String(100))  # Projeto específico ou geral
    status = db.Column(db.String(20), default='registrada')  # 'registrada', 'recebida', 'processada'

    data_doacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_recebimento = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'nome_doador': self.nome_doador or (self.usuario.nome if self.usuario else 'Anônimo'),
            'email_doador': self.email_doador,
            'telefone_doador': self.telefone_doador,
            'tipo_doacao': self.tipo_doacao,
            'valor': float(self.valor) if self.valor else None,
            'descricao': self.descricao,
            'projeto_destino': self.projeto_destino,
            'status': self.status,
            'data_doacao': self.data_doacao.isoformat() if self.data_doacao else None
        }


class Contato(db.Model):
    __tablename__ = 'contatos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    assunto = db.Column(db.String(150), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)

    # Dados de controle
    respondida = db.Column(db.Boolean, default=False)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    data_resposta = db.Column(db.DateTime)
    resposta = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'assunto': self.assunto,
            'mensagem': self.mensagem,
            'respondida': self.respondida,
            'data_envio': self.data_envio.isoformat() if self.data_envio else None,
            'resposta': self.resposta
        }


class Voluntario(db.Model):
    __tablename__ = 'voluntarios'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    areas_interesse = db.Column(db.Text)
    disponibilidade = db.Column(db.Text)
    experiencia = db.Column(db.Text)
    unidade_preferencia = db.Column(db.String(50))

    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento
    usuario = db.relationship('Usuario', backref='voluntario_info')

    def to_dict(self):
        return {
            'id': self.id,
            'usuario': self.usuario.nome if self.usuario else None,
            'areas_interesse': self.areas_interesse,
            'disponibilidade': self.disponibilidade,
            'experiencia': self.experiencia,
            'unidade_preferencia': self.unidade_preferencia,
            'ativo': self.ativo,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None
        }