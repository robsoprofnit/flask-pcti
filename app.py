from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from sqlalchemy.orm import query
from sqlalchemy.orm.query import Query
from wtforms import StringField, SubmitField, PasswordField, FloatField, IntegerField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets import TextArea


# Create a flask instace
app = Flask(__name__)

# Add Database
# [DEFAULT DB]
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pcti.db"

# [PRODUCTION DB]
# app.config['SQLALCHEMY_DATABASE_URI'
#           ] = 'mysql+pymysql://root:bolinho123@localhost/our_users'

# [Secret Key]
app.config["SECRET_KEY"] = "my super secret key"

# Initialize Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Create Variavel Model
class Variavel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(1028), nullable=False)
    tag = db.Column(db.String(50), nullable=False)
    id_dimensao = db.Column(db.Integer, nullable=False)
    delete_ = db.Column(db.Boolean, nullable=False)


# Create Dimensões Model
class Dimensoes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(1028), nullable=False)
    delete_ = db.Column(db.Boolean, nullable=False)


# Create Sub-Indicadores Model
class Sub_indicadores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(1028), nullable=False)
    id_dimensao = db.Column(db.Integer, nullable=False)
    delete_ = db.Column(db.Boolean, nullable=False)


# Create Email Model
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    delete_ = db.Column(db.Boolean, nullable=False)


# Create Respostas Model
class Respostas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resposta = db.Column(db.String(255), nullable=False)
    data_resposta = db.Column(db.DateTime, default=datetime.utcnow)
    tag = db.Column(db.String(50), nullable=False)
    id_ano_base = db.Column(db.Integer, nullable=False)
    id_instituicao = db.Column(db.Integer, nullable=False)
    id_respondido_por = db.Column(db.Integer, nullable=False)
    id_variavel = db.Column(db.Integer, nullable=False)
    delete_ = db.Column(db.Boolean, nullable=False)


# Create Pessoa Model
class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf_cnpj = db.Column(db.String(50), nullable=False)
    razao_social = db.Column(db.String(255), nullable=False)
    nome_social = db.Column(db.String(255), nullable=False)
    id_email = db.Column(db.Integer, nullable=False)
    id_tipo_pessoa = db.Column(db.Integer, nullable=False)
    id_uf = db.Column(db.Integer, nullable=False)
    delete_ = db.Column(db.Boolean, nullable=False)


# Create Tipo pessoa Model
class Tipo_pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    delete_ = db.Column(db.Boolean, nullable=False)


# Create Ano Base Model
class Ano_base(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.String(4), nullable=False)
    delete_ = db.Column(db.Boolean, nullable=False)


# Create Região Model


class Regiao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    delete_ = db.Column(db.Boolean, nullable=False)


# Create Uf Model
class Uf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    sigla = db.Column(db.String(2), nullable=False, unique=True)
    id_regiao = db.Column(db.Integer, nullable=False)
    delete_ = db.Column(db.Boolean, nullable=False)


# Create Municipio Model
class Municipio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    id_uf = db.Column(db.Integer, nullable=False)
    delete_ = db.Column(db.Boolean, nullable=False)


# Create Users Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(200), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    id_pessoa = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    delete_ = db.Column(db.Boolean, nullable=False)

    @property
    def password(self):
        raise AttributeError("passowrd is not a readeble attribute!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


# Create a User Form Class
class UserForm(FlaskForm):
    usuario = StringField("Usuario", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField(
        "Senha",
        validators=[
            DataRequired(),
            EqualTo("password_hash2", message="Senha não corresponde."),
        ],
    )
    password_hash2 = PasswordField("Confirmar Senha", validators=[DataRequired()])
    submit = SubmitField("Submeter")


class PasswordForm(FlaskForm):
    usuario = StringField("Usuário", validators=[DataRequired()])
    password_hash = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Salvar")


class PessoaForm(FlaskForm):
    nome = StringField("Nome e sobrenome", validators=[DataRequired()])
    cpf_cnpj = StringField("CPF ou CNPJ", validators=[DataRequired()])
    razao_social = StringField("Razão Social")
    nome_social = StringField("Nome Social")
    id_email = IntegerField("E-mail", validators=[DataRequired()])
    id_tipo_pessoa = IntegerField(
        "Pessoa Física ou Jurídica", validators=[DataRequired()]
    )
    id_uf = IntegerField("UF", validators=[DataRequired()])
    submit = SubmitField("Salvar")


class TipoPessoaForm(FlaskForm):
    nome = StringField("Tipo de Pessoa", validators=[DataRequired()])
    submit = SubmitField("Submeter")


class VariavelForm(FlaskForm):
    nome = StringField("Nome da Variável", validators=[DataRequired()])
    descricao = StringField("Descrição da Variável", validators=[DataRequired()])
    tag = StringField("TAG da Variável", validators=[DataRequired()])
    id_dimensao = IntegerField("Dimensão da Variável", validators=[DataRequired()])
    submit = SubmitField("Submeter")


class DimensaoForm(FlaskForm):
    nome = StringField("Nome da Dimensão", validators=[DataRequired()])
    descricao = StringField(
        "Descrições e Informações da Dimensão",
        validators=[DataRequired()],
        widget=TextArea(),
    )
    submit = SubmitField("Submeter")


class SubIndicadorForm(FlaskForm):
    nome = StringField("Nome do sub-indicador", validators=[DataRequired()])
    descricao = StringField("Descrição do sub-indicador", validators=[DataRequired()])
    id_dimensao = IntegerField("Dimensão", validators=[DataRequired()])
    submit = SubmitField("Submeter")


class RespostasForm(FlaskForm):

    id_ano_base = IntegerField("Ano Base")
    id_instituicao = IntegerField("Instituição", validators=[DataRequired()])
    id_respondido_por = IntegerField(
        "Responsável pela resposta", validators=[DataRequired()]
    )
    dimensao = IntegerField("Dimensão", validators=[DataRequired()])
    subdimensao = IntegerField("Sub-Dimensão", validators=[DataRequired()])
    id_variavel = IntegerField("Variável da dimensão", validators=[DataRequired()])
    id_uf = IntegerField("Estado", validators=[DataRequired()])
    resposta = FloatField("Valor", validators=[DataRequired()])
    tag = StringField("#TAG", validators=[DataRequired()])

    submit = SubmitField("Submeter")


class AnoBaseForm(FlaskForm):
    ano = StringField("Informe o Ano Base", validators=[DataRequired()])
    submit = SubmitField("Submeter")


class SetAnoBaseForm(FlaskForm):
    id_ano_base = IntegerField("Ano Base")
    ano = StringField("Informe o Ano Base", validators=[DataRequired()])
    submit = SubmitField("Submeter")


class RegiaoForm(FlaskForm):
    nome = StringField("Região Geográfica", validators=[DataRequired()])
    submit = SubmitField("Submeter")


class UfFrom(FlaskForm):
    nome = StringField("Nome Unidade Federativa", validators=[DataRequired()])
    sigla = StringField("Sigla UF", validators=[DataRequired()])
    id_regiao = IntegerField("Região Geográfica", validators=[DataRequired()])
    submit = SubmitField("Submeter")


class MunicipioFrom(FlaskForm):
    nome = StringField("Nome do Município", validators=[DataRequired()])
    id_uf = IntegerField("UF", validators=[DataRequired()])
    submit = SubmitField("Submeter")


# Create a route decorator
@app.route("/")
def index():
    return render_template("index.html")


# Criar Páginas de Erros Customizadadas
# URL Inválida
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Erro do Servidor Interno
@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500


@app.route("/admin")
def admin():
    return render_template("index.html")


@app.route("/dimensoes")
def dimensoes():
    return render_template("dimensoes.html")


# Add Recrusos Aplicados Page
@app.route("/respostas", methods=["GET", "POST"])
def respostas():
    form = RespostasForm()
    if form.validate_on_submit():
        resposta = Respostas(
            resposta=form.resposta.data,
            tag=form.tag.data,
            id_ano_base=form.id_ano_base.data,
            id_instituicao=form.id_instituicao.data,
            id_respondido_por=form.id_respondido_por.data,
            id_variavel=form.id_variavel.data,
            delete_=0,
        )
        # Clear the form
        form = RespostasForm(formdata=None)
        # Add tipo pergunta to database
        db.session.add(resposta)
        db.session.commit()
        # Return message
        flash("Dados cadastrados com sucesso!")
    # Redirect to the webpage
    list_uf = Uf.query.order_by(Uf.id)
    list_ano = Ano_base.query.order_by(Ano_base.ano)
    list_instituicao = Pessoa.query.filter(Pessoa.id_tipo_pessoa == "2")
    list_pessoa = Pessoa.query.filter(Pessoa.id_tipo_pessoa == "1")
    list_variavel = Variavel.query.order_by(Variavel.id_dimensao | Variavel.tag)
    return render_template(
        "respostas.html",
        list_uf=list_uf,
        list_ano=list_ano,
        list_instituicao=list_instituicao,
        list_pessoa=list_pessoa,
        list_variavel=list_variavel,
        form=form,
    )


@app.route("/estado", methods=["GET", "POST"])
def get_estado():
    cursor = Uf.query.order_by()
    query = "select * from uf"
    cursor.execute(query)
    uf = cursor.fetchall()
    return render_template("respostas.html", uf=uf)


@app.route("/recursos_humanos")
def recursos_humanos():
    colours = ["Red", "Blue", "Black", "Orange"]
    return render_template("dm2_recursos_humanos.html", colours=colours)


@app.route("/bolsas_formacao")
def bolsas_formacao():
    return render_template("dm3_bolsas_formacao.html")


@app.route("/producao_cientifica")
def producao_cientifica():
    return render_template("dm4_producao_cientifica.html")


@app.route("/patentes")
def patentes():
    return render_template("dm5_patentes.html")


@app.route("/inovacao")
def inovacao():
    return render_template("dm6_inovacao.html")


# Teste Password Page
@app.route("/test_pw", methods=["GET", "POST"])
def test_pw():
    usuario = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    # Validate Form
    if form.validate_on_submit():
        usuario = form.usuario.data
        password = form.password_hash.data
        # Clear Form
        form.usuario.data = ""
        form.password_hash.data = ""
        # Lookup User By Email
        pw_to_check = Users.query.filter_by(usuario=usuario).first()
        # Check Hashad Password
        passed = check_password_hash(pw_to_check.password_hash, password)
    return render_template(
        "test_pw.html",
        usuario=usuario,
        password=password,
        pw_to_check=pw_to_check,
        passed=passed,
        form=form,
    )


# Criate Pessoa Page
@app.route("/add-pessoa", methods=["GET", "POST"])
def add_pessoa():
    form = PessoaForm()
    if form.validate_on_submit():
        pessoa = Pessoa(
            nome=form.nome.data,
            cpf_cnpj=form.cpf_cnpj.data,
            razao_social=form.razao_social.data,
            nome_social=form.nome_social.data,
            id_email=form.id_email.data,
            id_tipo_pessoa=form.id_tipo_pessoa.data,
            id_uf=form.id_uf,
            delete_=0,
        )
        # Clear the form
        form = PessoaForm(formdata=None)
        # Add tipo pergunta to database
        db.session.add(pessoa)
        db.session.commit()
        # Return message
        flash("Pessoa cadastrada com sucesso!")
    # Redirect to the webpage
    return render_template("add_pessoa.html", form=form)


# Criate User Page
@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    usuario = None
    form = UserForm()
    # Validate Form
    if form.validate_on_submit():
        usuario = Users.query.filter_by(email=form.email.data).first()
        if usuario is None:
            # Hash the password
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            usuario = Users(
                usuario=form.usuario.data,
                password_hash=hashed_pw,
                id_pessoa=1,
                email=form.email.data,
                delete_=0,
            )
            db.session.add(usuario)
            db.session.commit()
        usuario = form.usuario.data
        form.usuario.data = ""
        form.email.data = ""
        form.password_hash.data = ""
        flash("Usuário cadastrado com sucesso!")
    our_users = Users.query.order_by(Users.id)
    return render_template(
        "add_user.html", form=form, usuario=usuario, our_users=our_users
    )


# Update Database Record
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    form = UserForm()
    usuario_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        usuario_to_update.usuario = request.form["usuario"]
        usuario_to_update.email = request.form["email"]
        usuario_to_update.password_hash = generate_password_hash(
            request.form["password_hash"], "sha256"
        )
        try:
            db.session.commit()
            flash("Usuário atualizado com sucesso")
            return render_template(
                "update.html", form=form, usuario_to_update=usuario_to_update, id=id
            )
        except Users.UpdateError:
            flash("Usuário não pode ser atualizado... tente novamente!")
            return render_template(
                "update.html", form=form, usuario_to_update=usuario_to_update
            )
    else:
        return render_template(
            "update.html", form=form, usuario_to_update=usuario_to_update, id=id
        )


# Delete Database Record
@app.route("/delete/<int:id>")
def delete(id):
    usuario = None
    form = UserForm()
    usuario_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(usuario_to_delete)
        db.session.commit()
        flash("Usuário removido com sucesso")
        our_users = Users.query.order_by(Users.id)
        return render_template(
            "add_user.html", form=form, usuario=usuario, our_users=our_users
        )
    except Users.UpdateError:
        flash("Usuário não pode ser deletado... tente novamente!")
        return render_template(
            "add_user.html", form=form, usuario=usuario, our_users=our_users
        )


# Add Sub-Indicador Page
@app.route("/add-sub-indicador", methods=["GET", "POST"])
def add_sub_indicador():
    form = SubIndicadorForm()
    if form.validate_on_submit():
        subindicador = Sub_indicadores(
            nome=form.nome.data,
            descricao=form.descricao.data,
            id_dimensao=form.id_dimensao.data,
            delete_=0,
        )
        # Clear the form
        form = SubIndicadorForm(formdata=None)
        # Add tipo pergunta to database
        db.session.add(subindicador)
        db.session.commit()
        # Return message
        flash("Sub-Indicador gravado com sucesso!")
    # Redirect to the webpage
    return render_template("add_sub_indicador.html", form=form)


# Add Dimensão Page
@app.route("/add-dimensao", methods=["GET", "POST"])
def add_dimensao():
    form = DimensaoForm()
    if form.validate_on_submit():
        dimensao = Dimensoes(
            nome=form.nome.data, descricao=form.descricao.data, delete_=0
        )
        # Clear the form
        form = DimensaoForm(formdata=None)
        # Add tipo pergunta to database
        db.session.add(dimensao)
        db.session.commit()
        # Return message
        flash("Dimensão gravada com sucesso!")
    # Redirect to the webpage
    return render_template("add_dimensao.html", form=form)


# Add Variável da Dimensão Page
@app.route("/add-variavel", methods=["GET", "POST"])
def add_variavel():
    form = VariavelForm()
    if form.validate_on_submit():
        variavel = Variavel(
            nome=form.nome.data,
            descricao=form.descricao.data,
            tag=form.tag.data,
            id_dimensao=form.id_dimensao.data,
            delete_=0,
        )
        # Clear the form
        form = VariavelForm(formdata=None)
        # Save data
        db.session.add(variavel)
        db.session.commit()
        # Return message
        flash("Variável de dimensão gravada com sucesso!")
    # Redirect to the webpage
    return render_template("add_variavel.html", form=form)


# Add Tipo Pessoa Page
@app.route("/add-tipo-pessoa", methods=["GET", "POST"])
def add_tipo_pessoa():
    form = TipoPessoaForm()
    if form.validate_on_submit():
        tipopessoa = Tipo_pessoa(nome=form.nome.data, delete_=0)
        # Clear the form
        form = TipoPessoaForm(formdata=None)
        # Add tipo pergunta to database
        db.session.add(tipopessoa)
        db.session.commit()
        # Return message
        flash("Tipo de pessoa cadastrado com sucesso!")
    # Redirect to the webpage
    return render_template("add_tipo_pessoa.html", form=form)


# Add Ano Base Page
@app.route("/add-ano", methods=["GET", "POST"])
def add_ano():
    form = AnoBaseForm()
    if form.validate_on_submit():
        ano = Ano_base(ano=form.ano.data, delete_=0)
        # Clear the form
        form = AnoBaseForm(formdata=None)
        # Add tipo pergunta to database
        db.session.add(ano)
        db.session.commit()
        # Return message
        flash("Ano base cadastrado com sucesso!")
    # Redirect to the webpage
    return render_template("add_ano.html", form=form)


# Set Ano Base Page
@app.route("/set-ano-base", methods=["GET", "POST"])
def set_ano_base():
    ano_base = None
    form = SetAnoBaseForm()
    ano_base = Ano_base.query.order_by(Ano_base.ano.desc())
    if request.method == "POST":
        ano_base.id_ano_base = request.form["ano_selecionado"]
        flash("ID Ano: {}".format(ano_base.id_ano_base))
    return render_template("set_ano_base.html", ano_base=ano_base, form=form)


# Add Região Geográfica Page
@app.route("/add-regiao", methods=["GET", "POST"])
def add_regiao():
    form = RegiaoForm()
    if form.validate_on_submit():
        regiao = Regiao(nome=form.nome.data, delete_=0)
        # Clear the form
        form = RegiaoForm(formdata=None)
        # Add tipo pergunta to database
        db.session.add(regiao)
        db.session.commit()
        # Return message
        flash("Região cadastrada com sucesso!")
    # Redirect to the webpage
    return render_template("add_regiao.html", form=form)


# Add UF Page
@app.route("/add-uf", methods=["GET", "POST"])
def add_uf():
    form = UfFrom()
    if form.validate_on_submit():
        uf = Uf(
            nome=form.nome.data,
            sigla=form.sigla.data,
            id_regiao=form.id_regiao.data,
            delete_=0,
        )
        # Clear the form
        form = UfFrom(formdata=None)
        # Add tipo pergunta to database
        db.session.add(uf)
        db.session.commit()
        # Return message
        flash("UF cadastrada com sucesso!")
    # Redirect to the webpage
    list_uf = Uf.query.order_by(Uf.id)
    return render_template("add_uf.html", form=form, list_uf=list_uf)


# Add Município Page
@app.route("/add-municipio", methods=["GET", "POST"])
def add_municipio():
    form = MunicipioFrom()
    if form.validate_on_submit():
        municipio = Municipio(nome=form.nome.data, id_uf=form.id_uf.data, delete_=0)
        # Clear the form
        form = MunicipioFrom(formdata=None)
        # Add tipo pergunta to database
        db.session.add(municipio)
        db.session.commit()
        # Return message
        flash("Município cadastrado com sucesso!")
    # Redirect to the webpage
    return render_template("add_municipio.html", form=form)
