from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy import case, or_
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import pandas as pd
from dotenv import load_dotenv
from functools import wraps

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sua-chave-secreta-aqui')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///esquadrias.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modelos do Banco de Dados
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')  # admin, supervisor, user
    is_active = db.Column(db.Boolean, default=True)
    # Permissões específicas
    can_view_obras = db.Column(db.Boolean, default=True)
    can_create_obras = db.Column(db.Boolean, default=False)
    can_edit_obras = db.Column(db.Boolean, default=False)
    can_delete_obras = db.Column(db.Boolean, default=False)
    
    can_view_esquadrias = db.Column(db.Boolean, default=True)
    can_create_esquadrias = db.Column(db.Boolean, default=False)
    can_edit_esquadrias = db.Column(db.Boolean, default=False)
    can_delete_esquadrias = db.Column(db.Boolean, default=False)
    
    can_view_materiais = db.Column(db.Boolean, default=True)
    can_create_materiais = db.Column(db.Boolean, default=False)
    can_edit_materiais = db.Column(db.Boolean, default=False)
    can_delete_materiais = db.Column(db.Boolean, default=False)
    can_movimentar_estoque = db.Column(db.Boolean, default=False)
    
    can_view_manutencao = db.Column(db.Boolean, default=False)
    can_create_manutencao = db.Column(db.Boolean, default=False)
    can_edit_manutencao = db.Column(db.Boolean, default=False)
    can_delete_manutencao = db.Column(db.Boolean, default=False)
    
    can_view_entrega = db.Column(db.Boolean, default=False)
    can_create_entrega = db.Column(db.Boolean, default=False)
    can_edit_entrega = db.Column(db.Boolean, default=False)
    can_delete_entrega = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def has_permission(self, permission):
        """Verifica se o usuário tem uma permissão específica"""
        if self.role == 'admin':
            return True
        
        # Verificar se o atributo existe e não é None
        value = getattr(self, permission, None)
        if value is None:
            # Se não está definido, aplicar permissões padrão baseadas no role
            self.set_permissions_for_role(self.role)
            value = getattr(self, permission, False)
        
        return bool(value)
    
    def is_admin(self):
        """Verifica se o usuário é administrador"""
        return self.role == 'admin'
    
    def set_permissions_for_role(self, role):
        """Define permissões padrão baseadas no role"""
        if role == 'admin':
            # Admin tem todas as permissões
            for field in self.__table__.columns:
                if field.name.startswith('can_'):
                    setattr(self, field.name, True)
        elif role == 'supervisor':
            # Supervisor tem permissões de visualização e algumas de edição
            self.can_view_obras = True
            self.can_create_obras = True
            self.can_edit_obras = True
            self.can_view_esquadrias = True
            self.can_create_esquadrias = True
            self.can_edit_esquadrias = True
            self.can_view_materiais = True
            self.can_create_materiais = True
            self.can_edit_materiais = True
            self.can_movimentar_estoque = True
            self.can_view_manutencao = True
            self.can_create_manutencao = True
            self.can_edit_manutencao = True
            self.can_view_entrega = True
            self.can_create_entrega = True
            self.can_edit_entrega = True
        else:  # user
            # Usuário comum tem apenas permissões básicas de visualização
            self.can_view_obras = True
            self.can_view_esquadrias = True
            self.can_view_materiais = True

class Obra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    endereco = db.Column(db.Text, nullable=False)
    cliente = db.Column(db.String(200), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_prevista = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='Em Andamento')
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Esquadria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    obra_id = db.Column(db.Integer, db.ForeignKey('obra.id'), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    dimensoes = db.Column(db.String(100), nullable=False)
    material = db.Column(db.String(100), nullable=False)
    cor = db.Column(db.String(50))
    quantidade = db.Column(db.Integer, default=1)
    status = db.Column(db.String(50), default='Pendente')
    data_producao = db.Column(db.Date)
    data_entrega = db.Column(db.Date)
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    obra = db.relationship('Obra', backref=db.backref('esquadrias', lazy=True))

class MaterialEmbalagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)  # plástico filme, bolha, papelão, etc.
    descricao = db.Column(db.Text)
    quantidade_estoque = db.Column(db.Integer, default=0)
    quantidade_minima = db.Column(db.Integer, default=10)
    unidade = db.Column(db.String(20), default='un')
    preco_unitario = db.Column(db.Float, default=0.0)
    fornecedor = db.Column(db.String(200))
    especificacoes = db.Column(db.Text)  # tamanho, cor, etc.
    status_alerta = db.Column(db.String(20), default='normal')  # normal, atencao, critico
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com movimentações
    movimentacoes = db.relationship('MovimentacaoEstoque', backref='material', lazy=True, cascade='all, delete-orphan')

class MovimentacaoEstoque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('material_embalagem.id'), nullable=False)
    tipo_movimentacao = db.Column(db.String(50), nullable=False)  # entrada, saida, ajuste
    quantidade = db.Column(db.Integer, nullable=False)
    quantidade_anterior = db.Column(db.Integer, nullable=False)
    quantidade_atual = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(200))
    observacoes = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    usuario = db.relationship('User', backref='movimentacoes')

class ManutencaoCaminhao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(10), nullable=False)
    data_manutencao = db.Column(db.Date, nullable=False)
    tipo_manutencao = db.Column(db.String(100), nullable=False)  # preventiva, corretiva, etc.
    descricao = db.Column(db.Text, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    km_veiculo = db.Column(db.Integer)
    fornecedor_servico = db.Column(db.String(200))
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProgramacaoEntrega(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_expedicao = db.Column(db.String(50), nullable=False)
    obra_id = db.Column(db.Integer, db.ForeignKey('obra.id'), nullable=False)
    percentual_liberacao = db.Column(db.Integer, nullable=False)  # 1 a 100
    data_carregamento = db.Column(db.Date, nullable=False)
    data_entrega = db.Column(db.Date, nullable=False)
    caminhoneiro = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default='Programado')  # Programado, Carregado, Entregue, Cancelado
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    obra = db.relationship('Obra', backref=db.backref('programacoes_entrega', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Decorator para verificar permissões

def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if not current_user.has_permission(permission) and not current_user.is_admin():
                flash('Você não tem permissão para acessar esta funcionalidade.', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_admin():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if not current_user.is_admin():
                flash('Acesso negado. Apenas administradores podem acessar esta funcionalidade.', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Funções auxiliares para controle de estoque
def atualizar_status_alerta(material):
    """Atualiza o status de alerta do material baseado no estoque"""
    if material.quantidade_estoque <= 0:
        material.status_alerta = 'critico'
    elif material.quantidade_estoque <= material.quantidade_minima:
        material.status_alerta = 'atencao'
    else:
        material.status_alerta = 'normal'
    db.session.commit()

def registrar_movimentacao(material_id, tipo, quantidade, motivo=None, observacoes=None):
    """Registra uma movimentação de estoque"""
    material = MaterialEmbalagem.query.get(material_id)
    if not material:
        return False
    
    quantidade_anterior = material.quantidade_estoque
    
    if tipo == 'entrada':
        material.quantidade_estoque += quantidade
    elif tipo == 'saida':
        if material.quantidade_estoque >= quantidade:
            material.quantidade_estoque -= quantidade
        else:
            return False  # Estoque insuficiente
    elif tipo == 'ajuste':
        material.quantidade_estoque = quantidade
    
    # Atualizar status de alerta
    atualizar_status_alerta(material)
    
    # Registrar movimentação
    movimentacao = MovimentacaoEstoque(
        material_id=material_id,
        tipo_movimentacao=tipo,
        quantidade=quantidade,
        quantidade_anterior=quantidade_anterior,
        quantidade_atual=material.quantidade_estoque,
        motivo=motivo,
        observacoes=observacoes,
        usuario_id=current_user.id
    )
    
    db.session.add(movimentacao)
    db.session.commit()
    return True

def obter_alertas_estoque():
    """Retorna lista de materiais com alertas de estoque"""
    materiais_criticos = MaterialEmbalagem.query.filter_by(status_alerta='critico').all()
    materiais_atencao = MaterialEmbalagem.query.filter_by(status_alerta='atencao').all()
    
    return {
        'criticos': materiais_criticos,
        'atencao': materiais_atencao,
        'total_criticos': len(materiais_criticos),
        'total_atencao': len(materiais_atencao)
    }

# Rotas
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form['username']  # Pode ser username ou email
        password = request.form['password']
        
        # Buscar usuário por username ou email usando OR
        user = User.query.filter(
            or_(
                User.username == login_input,
                User.email == login_input
            )
        ).first()
        
        if user and user.check_password(password) and user.is_active:
            login_user(user)
            return redirect(url_for('dashboard'))
        elif user and not user.is_active:
            flash('Sua conta está desativada. Entre em contato com o administrador.', 'error')
        else:
            flash('Usuário, e-mail ou senha inválidos', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Estatísticas do dashboard
    total_obras = Obra.query.count()
    total_esquadrias = Esquadria.query.count()
    pendentes = Esquadria.query.filter_by(status='Pendente').count()
    produzidas = Esquadria.query.filter_by(status='Produzida').count()
    entregues = Esquadria.query.filter_by(status='Entregue').count()
    
    # Estatísticas de materiais de embalagem
    total_materiais = MaterialEmbalagem.query.count()
    estoque_baixo = MaterialEmbalagem.query.filter(
        MaterialEmbalagem.quantidade_estoque <= MaterialEmbalagem.quantidade_minima
    ).count()
    
    # Alertas de estoque detalhados
    alertas = obter_alertas_estoque()
    
    # Valor total do estoque
    valor_total_estoque = db.session.query(
        db.func.sum(MaterialEmbalagem.quantidade_estoque * MaterialEmbalagem.preco_unitario)
    ).scalar() or 0
    
    # Movimentações recentes
    movimentacoes_recentes = MovimentacaoEstoque.query.order_by(
        MovimentacaoEstoque.created_at.desc()
    ).limit(10).all()
    
    # Materiais por tipo
    materiais_por_tipo = db.session.query(
        MaterialEmbalagem.tipo,
        db.func.count(MaterialEmbalagem.id).label('quantidade')
    ).group_by(MaterialEmbalagem.tipo).all()
    
    # Estatísticas de manutenção de caminhões
    total_manutencoes = ManutencaoCaminhao.query.count()
    valor_total_manutencoes = db.session.query(db.func.sum(ManutencaoCaminhao.valor_total)).scalar() or 0
    
    # Estatísticas de programação de entrega
    total_programacoes = ProgramacaoEntrega.query.count()
    programacoes_hoje = ProgramacaoEntrega.query.filter(
        ProgramacaoEntrega.data_carregamento == datetime.now().date()
    ).count()
    
    # Obras recentes
    obras_recentes = Obra.query.order_by(Obra.created_at.desc()).limit(5).all()
    
    # Estatísticas de esquadrias produzidas e entregues por obra
    esquadrias_por_obra = db.session.query(
        Obra.id,
        Obra.nome,
        db.func.sum(case([(Esquadria.status == 'Produzida', Esquadria.quantidade)], else_=0)).label('total_produzidas'),
        db.func.sum(case([(Esquadria.status == 'Entregue', Esquadria.quantidade)], else_=0)).label('total_entregues'),
        db.func.sum(Esquadria.quantidade).label('total_esquadrias_obra')
    ).join(Esquadria).group_by(Obra.id, Obra.nome).order_by(Obra.nome).all()
    
    return render_template('dashboard.html',
                         total_obras=total_obras,
                         total_esquadrias=total_esquadrias,
                         pendentes=pendentes,
                         produzidas=produzidas,
                         entregues=entregues,
                         total_materiais=total_materiais,
                         estoque_baixo=estoque_baixo,
                         alertas=alertas,
                         valor_total_estoque=valor_total_estoque,
                         movimentacoes_recentes=movimentacoes_recentes,
                         materiais_por_tipo=materiais_por_tipo,
                         total_manutencoes=total_manutencoes,
                         valor_total_manutencoes=valor_total_manutencoes,
                         total_programacoes=total_programacoes,
                         programacoes_hoje=programacoes_hoje,
                         obras_recentes=obras_recentes,
                         esquadrias_por_obra=esquadrias_por_obra)

@app.route('/obras')
@login_required
@require_permission('can_view_obras')
def obras():
    obras = Obra.query.order_by(Obra.created_at.desc()).all()
    return render_template('obras.html', obras=obras)

@app.route('/obras/nova', methods=['GET', 'POST'])
@login_required
@require_permission('can_create_obras')
def nova_obra():
    if request.method == 'POST':
        obra = Obra(
            nome=request.form['nome'],
            endereco=request.form['endereco'],
            cliente=request.form['cliente'],
            data_inicio=datetime.strptime(request.form['data_inicio'], '%Y-%m-%d').date(),
            data_prevista=datetime.strptime(request.form['data_prevista'], '%Y-%m-%d').date(),
            observacoes=request.form.get('observacoes', '')
        )
        db.session.add(obra)
        db.session.commit()
        flash('Obra criada com sucesso!', 'success')
        return redirect(url_for('obras'))
    
    return render_template('nova_obra.html')

@app.route('/esquadrias')
@login_required
@require_permission('can_view_esquadrias')
def esquadrias():
    esquadrias = Esquadria.query.join(Obra).order_by(Esquadria.created_at.desc()).all()
    return render_template('esquadrias.html', esquadrias=esquadrias)

@app.route('/esquadrias/nova', methods=['GET', 'POST'])
@login_required
@require_permission('can_create_esquadrias')
def nova_esquadria():
    if request.method == 'POST':
        esquadria = Esquadria(
            obra_id=request.form['obra_id'],
            tipo=request.form['tipo'],
            dimensoes=request.form['dimensoes'],
            material=request.form['material'],
            cor=request.form.get('cor', ''),
            quantidade=int(request.form['quantidade']),
            observacoes=request.form.get('observacoes', '')
        )
        db.session.add(esquadria)
        db.session.commit()
        flash('Esquadria criada com sucesso!', 'success')
        return redirect(url_for('esquadrias'))
    
    obras = Obra.query.all()
    return render_template('nova_esquadria.html', obras=obras)

@app.route('/materiais')
@login_required
@require_permission('can_view_materiais')
def materiais():
    materiais = MaterialEmbalagem.query.order_by(MaterialEmbalagem.nome).all()
    alertas = obter_alertas_estoque()
    return render_template('materiais.html', materiais=materiais, alertas=alertas)

@app.route('/materiais/movimentacao/<int:id>', methods=['GET', 'POST'])
@login_required
@require_permission('can_movimentar_estoque')
def movimentacao_estoque(id):
    material = MaterialEmbalagem.query.get_or_404(id)
    
    if request.method == 'POST':
        tipo = request.form['tipo']
        quantidade = int(request.form['quantidade'])
        motivo = request.form.get('motivo', '')
        observacoes = request.form.get('observacoes', '')
        
        if registrar_movimentacao(id, tipo, quantidade, motivo, observacoes):
            flash(f'Movimentação registrada com sucesso!', 'success')
            return redirect(url_for('materiais'))
        else:
            flash('Erro ao registrar movimentação. Verifique se há estoque suficiente.', 'error')
    
    movimentacoes = MovimentacaoEstoque.query.filter_by(material_id=id).order_by(
        MovimentacaoEstoque.created_at.desc()
    ).limit(20).all()
    
    return render_template('movimentacao_estoque.html', 
                         material=material, 
                         movimentacoes=movimentacoes)

@app.route('/materiais/alertas')
@login_required
def alertas_estoque():
    alertas = obter_alertas_estoque()
    return render_template('alertas_estoque.html', alertas=alertas)

@app.route('/api/estoque/status')
@login_required
def api_estoque_status():
    """API para verificar status do estoque (usado para notificações em tempo real)"""
    alertas = obter_alertas_estoque()
    return jsonify({
        'criticos': len(alertas['criticos']),
        'atencao': len(alertas['atencao']),
        'materiais_criticos': [{
            'id': m.id,
            'nome': m.nome,
            'quantidade': m.quantidade_estoque,
            'minima': m.quantidade_minima
        } for m in alertas['criticos']],
        'materiais_atencao': [{
            'id': m.id,
            'nome': m.nome,
            'quantidade': m.quantidade_estoque,
            'minima': m.quantidade_minima
        } for m in alertas['atencao']]
    })

@app.route('/materiais/novo', methods=['GET', 'POST'])
@login_required
@require_permission('can_create_materiais')
def novo_material():
    if request.method == 'POST':
        material = MaterialEmbalagem(
            nome=request.form['nome'],
            tipo=request.form['tipo'],
            descricao=request.form.get('descricao', ''),
            quantidade_estoque=int(request.form['quantidade_estoque']),
            quantidade_minima=int(request.form['quantidade_minima']),
            unidade=request.form.get('unidade', 'un'),
            preco_unitario=float(request.form.get('preco_unitario', 0)),
            fornecedor=request.form.get('fornecedor', ''),
            especificacoes=request.form.get('especificacoes', '')
        )
        db.session.add(material)
        db.session.commit()
        flash('Material criado com sucesso!', 'success')
        return redirect(url_for('materiais'))
    
    return render_template('novo_material.html')

@app.route('/materiais/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@require_permission('can_edit_materiais')
def editar_material(id):
    material = MaterialEmbalagem.query.get_or_404(id)
    
    if request.method == 'POST':
        material.nome = request.form['nome']
        material.tipo = request.form['tipo']
        material.descricao = request.form.get('descricao', '')
        material.quantidade_estoque = int(request.form['quantidade_estoque'])
        material.quantidade_minima = int(request.form['quantidade_minima'])
        material.unidade = request.form.get('unidade', 'un')
        material.preco_unitario = float(request.form.get('preco_unitario', 0))
        material.fornecedor = request.form.get('fornecedor', '')
        material.especificacoes = request.form.get('especificacoes', '')
        
        # Atualizar status de alerta
        atualizar_status_alerta(material)
        
        db.session.commit()
        flash('Material atualizado com sucesso!', 'success')
        return redirect(url_for('materiais'))
    
    return render_template('editar_material.html', material=material)

@app.route('/materiais/excluir/<int:id>', methods=['POST'])
@login_required
@require_permission('can_delete_materiais')
def excluir_material(id):
    material = MaterialEmbalagem.query.get_or_404(id)
    
    # Verificar se existem movimentações associadas
    movimentacoes = MovimentacaoEstoque.query.filter_by(material_id=id).count()
    if movimentacoes > 0:
        flash('Não é possível excluir este material pois existem movimentações de estoque associadas.', 'error')
        return redirect(url_for('materiais'))
    
    db.session.delete(material)
    db.session.commit()
    flash('Material excluído com sucesso!', 'success')
    return redirect(url_for('materiais'))

# Rotas para Manutenção de Caminhões
@app.route('/manutencao-caminhoes')
@login_required
@require_permission('can_view_manutencao')
def manutencao_caminhoes():
    manutencoes = ManutencaoCaminhao.query.order_by(ManutencaoCaminhao.data_manutencao.desc()).all()
    return render_template('manutencao_caminhoes.html', manutencoes=manutencoes)

@app.route('/manutencao-caminhoes/nova', methods=['GET', 'POST'])
@login_required
@require_permission('can_create_manutencao')
def nova_manutencao():
    if request.method == 'POST':
        manutencao = ManutencaoCaminhao(
            placa=request.form['placa'],
            data_manutencao=datetime.strptime(request.form['data_manutencao'], '%Y-%m-%d').date(),
            tipo_manutencao=request.form['tipo_manutencao'],
            descricao=request.form['descricao'],
            valor_total=float(request.form['valor_total']),
            km_veiculo=int(request.form.get('km_veiculo', 0)) if request.form.get('km_veiculo') else None,
            fornecedor_servico=request.form.get('fornecedor_servico', ''),
            observacoes=request.form.get('observacoes', '')
        )
        db.session.add(manutencao)
        db.session.commit()
        flash('Manutenção registrada com sucesso!', 'success')
        return redirect(url_for('manutencao_caminhoes'))
    
    return render_template('nova_manutencao.html')

@app.route('/manutencao-caminhoes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_manutencao(id):
    manutencao = ManutencaoCaminhao.query.get_or_404(id)
    
    if request.method == 'POST':
        manutencao.placa = request.form['placa']
        manutencao.data_manutencao = datetime.strptime(request.form['data_manutencao'], '%Y-%m-%d').date()
        manutencao.tipo_manutencao = request.form['tipo_manutencao']
        manutencao.descricao = request.form['descricao']
        manutencao.valor_total = float(request.form['valor_total'])
        manutencao.km_veiculo = int(request.form.get('km_veiculo', 0)) if request.form.get('km_veiculo') else None
        manutencao.fornecedor_servico = request.form.get('fornecedor_servico', '')
        manutencao.observacoes = request.form.get('observacoes', '')
        
        db.session.commit()
        flash('Manutenção atualizada com sucesso!', 'success')
        return redirect(url_for('manutencao_caminhoes'))
    
    return render_template('editar_manutencao.html', manutencao=manutencao)

@app.route('/manutencao-caminhoes/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_manutencao(id):
    manutencao = ManutencaoCaminhao.query.get_or_404(id)
    db.session.delete(manutencao)
    db.session.commit()
    flash('Manutenção excluída com sucesso!', 'success')
    return redirect(url_for('manutencao_caminhoes'))

# Rota para importar esquadrias via Excel
@app.route('/esquadrias/importar', methods=['GET', 'POST'])
@login_required
def importar_esquadrias():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Nenhum arquivo selecionado', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('Nenhum arquivo selecionado', 'error')
            return redirect(request.url)
        
        if file and file.filename.endswith(('.xlsx', '.xls')):
            try:
                # Ler o arquivo Excel
                df = pd.read_excel(file)
                
                # Colunas obrigatórias esperadas
                colunas_obrigatorias = ['obra_id', 'tipo', 'dimensoes', 'material', 'quantidade']
                
                # Verificar se as colunas obrigatórias estão presentes
                for coluna in colunas_obrigatorias:
                    if coluna not in df.columns:
                        flash(f'Coluna obrigatória "{coluna}" não encontrada no arquivo', 'error')
                        return redirect(request.url)
                
                # Importar esquadrias
                importadas = 0
                for index, row in df.iterrows():
                    # Verificar se a obra existe
                    obra = Obra.query.get(int(row['obra_id']))
                    if not obra:
                        continue
                    
                    esquadria = Esquadria(
                        obra_id=int(row['obra_id']),
                        tipo=str(row['tipo']),
                        dimensoes=str(row['dimensoes']),
                        material=str(row['material']),
                        cor=str(row.get('cor', '')),
                        quantidade=int(row['quantidade']),
                        observacoes=str(row.get('observacoes', ''))
                    )
                    db.session.add(esquadria)
                    importadas += 1
                
                db.session.commit()
                flash(f'{importadas} esquadrias importadas com sucesso!', 'success')
                
            except Exception as e:
                flash(f'Erro ao importar arquivo: {str(e)}', 'error')
        else:
            flash('Formato de arquivo inválido. Use .xlsx ou .xls', 'error')
        
        return redirect(url_for('esquadrias'))
    
    obras = Obra.query.all()
    return render_template('importar_esquadrias.html', obras=obras)

# Rotas para Programação de Entrega
@app.route('/programacao-entrega')
@login_required
@require_permission('can_view_entrega')
def programacao_entrega():
    programacoes = ProgramacaoEntrega.query.join(Obra).order_by(ProgramacaoEntrega.data_carregamento.desc()).all()
    return render_template('programacao_entrega.html', programacoes=programacoes)

@app.route('/programacao-entrega/nova', methods=['GET', 'POST'])
@login_required
@require_permission('can_create_entrega')
def nova_programacao():
    if request.method == 'POST':
        programacao = ProgramacaoEntrega(
            numero_expedicao=request.form['numero_expedicao'],
            obra_id=request.form['obra_id'],
            percentual_liberacao=int(request.form['percentual_liberacao']),
            data_carregamento=datetime.strptime(request.form['data_carregamento'], '%Y-%m-%d').date(),
            data_entrega=datetime.strptime(request.form['data_entrega'], '%Y-%m-%d').date(),
            caminhoneiro=request.form['caminhoneiro'],
            status=request.form.get('status', 'Programado'),
            observacoes=request.form.get('observacoes', '')
        )
        db.session.add(programacao)
        db.session.commit()
        flash('Programação de entrega criada com sucesso!', 'success')
        return redirect(url_for('programacao_entrega'))
    
    obras = Obra.query.all()
    return render_template('nova_programacao.html', obras=obras)

@app.route('/programacao-entrega/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_programacao(id):
    programacao = ProgramacaoEntrega.query.get_or_404(id)
    
    if request.method == 'POST':
        programacao.numero_expedicao = request.form['numero_expedicao']
        programacao.obra_id = request.form['obra_id']
        programacao.percentual_liberacao = int(request.form['percentual_liberacao'])
        programacao.data_carregamento = datetime.strptime(request.form['data_carregamento'], '%Y-%m-%d').date()
        programacao.data_entrega = datetime.strptime(request.form['data_entrega'], '%Y-%m-%d').date()
        programacao.caminhoneiro = request.form['caminhoneiro']
        programacao.status = request.form['status']
        programacao.observacoes = request.form.get('observacoes', '')
        
        db.session.commit()
        flash('Programação atualizada com sucesso!', 'success')
        return redirect(url_for('programacao_entrega'))
    
    obras = Obra.query.all()
    return render_template('editar_programacao.html', programacao=programacao, obras=obras)

@app.route('/programacao-entrega/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_programacao(id):
    programacao = ProgramacaoEntrega.query.get_or_404(id)
    db.session.delete(programacao)
    db.session.commit()
    flash('Programação excluída com sucesso!', 'success')
    return redirect(url_for('programacao_entrega'))

@app.route('/usuarios')
@login_required
@require_admin()
def usuarios():
    usuarios = User.query.filter(User.id != current_user.id).all()  # Não mostrar o próprio usuário na lista
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/novo', methods=['GET', 'POST'])
@login_required
@require_admin()
def novo_usuario():
    if request.method == 'POST':
        # Verificar se usuário já existe
        existing_user = User.query.filter_by(username=request.form['username']).first()
        if existing_user:
            flash('Nome de usuário já existe!', 'error')
            return render_template('novo_usuario.html')
        
        existing_email = User.query.filter_by(email=request.form['email']).first()
        if existing_email:
            flash('Email já cadastrado!', 'error')
            return render_template('novo_usuario.html')
        
        user = User(
            username=request.form['username'],
            email=request.form['email'],
            role=request.form['role']
        )
        user.set_password(request.form['password'])
        
        # Definir permissões baseadas no role
        user.set_permissions_for_role(request.form['role'])
        
        # Aplicar permissões específicas se fornecidas
        for permission in ['can_view_obras', 'can_create_obras', 'can_edit_obras', 'can_delete_obras',
                          'can_view_esquadrias', 'can_create_esquadrias', 'can_edit_esquadrias', 'can_delete_esquadrias',
                          'can_view_materiais', 'can_create_materiais', 'can_edit_materiais', 'can_delete_materiais',
                          'can_movimentar_estoque', 'can_view_manutencao', 'can_create_manutencao', 
                          'can_edit_manutencao', 'can_delete_manutencao', 'can_view_entrega', 
                          'can_create_entrega', 'can_edit_entrega', 'can_delete_entrega']:
            if permission in request.form:
                setattr(user, permission, True)
        
        db.session.add(user)
        db.session.commit()
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('usuarios'))
    
    return render_template('novo_usuario.html')

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@require_admin()
def editar_usuario(id):
    user = User.query.get_or_404(id)
    
    # Não permitir editar outro admin
    if user.role == 'admin' and user.id != current_user.id:
        flash('Não é possível editar outro administrador!', 'error')
        return redirect(url_for('usuarios'))
    
    if request.method == 'POST':
        # Verificar se username já existe em outro usuário
        existing_user = User.query.filter_by(username=request.form['username']).filter(User.id != id).first()
        if existing_user:
            flash('Nome de usuário já existe!', 'error')
            return render_template('editar_usuario.html', user=user)
        
        # Verificar se email já existe em outro usuário
        existing_email = User.query.filter_by(email=request.form['email']).filter(User.id != id).first()
        if existing_email:
            flash('Email já cadastrado!', 'error')
            return render_template('editar_usuario.html', user=user)
        
        user.username = request.form['username']
        user.email = request.form['email']
        
        # Apenas permitir mudança de role se não for admin ou se for o próprio usuário
        if user.role != 'admin' or user.id == current_user.id:
            user.role = request.form['role']
            user.set_permissions_for_role(request.form['role'])
        
        # Aplicar permissões específicas
        for permission in ['can_view_obras', 'can_create_obras', 'can_edit_obras', 'can_delete_obras',
                          'can_view_esquadrias', 'can_create_esquadrias', 'can_edit_esquadrias', 'can_delete_esquadrias',
                          'can_view_materiais', 'can_create_materiais', 'can_edit_materiais', 'can_delete_materiais',
                          'can_movimentar_estoque', 'can_view_manutencao', 'can_create_manutencao', 
                          'can_edit_manutencao', 'can_delete_manutencao', 'can_view_entrega', 
                          'can_create_entrega', 'can_edit_entrega', 'can_delete_entrega']:
            setattr(user, permission, permission in request.form)
        
        # Se a senha foi fornecida, atualizar
        if request.form.get('password'):
            user.set_password(request.form['password'])
        
        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('usuarios'))
    
    return render_template('editar_usuario.html', user=user)

@app.route('/usuarios/excluir/<int:id>', methods=['POST'])
@login_required
@require_admin()
def excluir_usuario(id):
    user = User.query.get_or_404(id)
    
    # Não permitir excluir a si mesmo ou outros admins
    if user.id == current_user.id:
        flash('Você não pode excluir sua própria conta!', 'error')
        return redirect(url_for('usuarios'))
    
    if user.role == 'admin':
        flash('Não é possível excluir administradores!', 'error')
        return redirect(url_for('usuarios'))
    
    db.session.delete(user)
    db.session.commit()
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('usuarios'))

@app.route('/usuarios/ativar-desativar/<int:id>', methods=['POST'])
@login_required
@require_admin()
def ativar_desativar_usuario(id):
    user = User.query.get_or_404(id)
    
    # Não permitir desativar a si mesmo
    if user.id == current_user.id:
        flash('Você não pode desativar sua própria conta!', 'error')
        return redirect(url_for('usuarios'))
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'ativado' if user.is_active else 'desativado'
    flash(f'Usuário {status} com sucesso!', 'success')
    return redirect(url_for('usuarios'))

@app.route('/admin/update-permissions')
@login_required
@require_admin()
def update_permissions():
    """Rota temporária para atualizar permissões de usuários existentes"""
    try:
        users = User.query.all()
        updated = False
        
        for user in users:
            if user.role == 'admin':
                # Garantir que admin tenha todas as permissões
                user.set_permissions_for_role('admin')
                # Garantir que is_active seja True se não estiver definido
                if not hasattr(user, 'is_active') or user.is_active is None:
                    user.is_active = True
                updated = True
                print(f"Permissões de admin atualizadas para: {user.username}")
        
        if updated:
            db.session.commit()
            flash('Permissões atualizadas com sucesso!', 'success')
        else:
            flash('Nenhuma permissão precisou ser atualizada.', 'info')
            
    except Exception as e:
        flash(f'Erro ao atualizar permissões: {str(e)}', 'error')
    
    return redirect(url_for('usuarios'))

# Função para criar usuário admin padrão
def create_admin_user():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@sistema.com',
            role='admin'
        )
        admin.set_password('admin123')
        admin.set_permissions_for_role('admin')
        db.session.add(admin)
        db.session.commit()
        print("Usuário admin criado: admin / admin123")
    else:
        # Se o admin já existe, garantir que ele tenha todas as permissões
        admin.role = 'admin'  # Garantir que role seja admin
        admin.is_active = True  # Garantir que esteja ativo
        admin.set_permissions_for_role('admin')  # Aplicar todas as permissões
        db.session.commit()
        print("Usuário admin existente atualizado com todas as permissões")

def create_example_users():
    """Cria usuários de exemplo para demonstração"""
    # Criar supervisor
    supervisor = User.query.filter_by(username='supervisor').first()
    if not supervisor:
        supervisor = User(
            username='supervisor',
            email='supervisor@sistema.com',
            role='supervisor'
        )
        supervisor.set_password('super123')
        supervisor.set_permissions_for_role('supervisor')
        db.session.add(supervisor)
        print("Usuário supervisor criado: supervisor / super123")
    
    # Criar usuário comum
    usuario = User.query.filter_by(username='usuario').first()
    if not usuario:
        usuario = User(
            username='usuario',
            email='usuario@sistema.com',
            role='user'
        )
        usuario.set_password('user123')
        usuario.set_permissions_for_role('user')
        db.session.add(usuario)
        print("Usuário comum criado: usuario / user123")
    
    db.session.commit()

def update_existing_users_permissions():
    """Atualiza permissões de usuários existentes que não têm as novas colunas preenchidas"""
    users = User.query.all()
    updated = False
    for user in users:
        # Verificar se o usuário precisa ter suas permissões atualizadas
        # Se o usuário admin não tem permissões definidas, atualizar
        if user.role == 'admin':
            # Garantir que admin tenha todas as permissões
            user.set_permissions_for_role('admin')
            updated = True
            print(f"Permissões de admin atualizadas para: {user.username}")
        elif not hasattr(user, 'is_active') or user.can_view_obras is None:
            # Atualizar para usuários que não têm as novas colunas
            user.set_permissions_for_role(user.role)
            if not hasattr(user, 'is_active'):
                user.is_active = True
            updated = True
            print(f"Permissões atualizadas para usuário: {user.username} (role: {user.role})")
    
    if updated:
        db.session.commit()
        print("Permissões de usuários existentes atualizadas com sucesso!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin_user()
        create_example_users()
        update_existing_users_permissions()
    
    # Configuração para deploy no Render
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(debug=debug, host='0.0.0.0', port=port)
