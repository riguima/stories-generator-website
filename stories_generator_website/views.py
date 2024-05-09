from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from sqlalchemy import select

from stories_generator_website.database import Session
from stories_generator_website.forms import LoginForm
from stories_generator_website.models import Product, User


def init_app(app):
    @app.get('/<string:username>')
    def index(username):
        with Session() as session:
            query = select(Product).where(Product.username == username)
            products = session.scalars(query).all()
            return render_template('index.html', products=products)

    @app.get('/produto/<int:product_id>')
    def product(product_id):
        with Session() as session:
            query = select(Product).where(Product.id == product_id)
            product = session.scalars(query).first()
            return render_template('product.html', product_id=product)

    @app.route('/cadastro', methods=['GET', 'POST'])
    def register():
        form = LoginForm()
        if form.validate_on_submit():
            with Session() as session:
                query = select(Product).where(
                    Product.username == request.form['username']
                )
                products = session.scalars(query).all()
                if products:
                    user = User(
                        username=request.form['username'],
                        password=request.form['password'],
                    )
                    session.add(user)
                    session.commit()
                    return redirect(url_for('login'))
                else:
                    return redirect(
                        url_for('login', error_message='Usuário Inválido')
                    )
        return render_template(
            'register.html',
            error_message=request.args.get('error_message'),
            form=form,
        )

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            with Session() as session:
                query = (
                    select(User)
                    .where(User.username == request.form['username'])
                    .where(User.is_admin == True)
                )
                user_model = session.scalars(query).first()
                if (
                    user_model
                    and user_model.password == request.form['password']
                    and user_model.is_admin
                ):
                    user_model.authenticated = True
                    session.commit()
                    login_user(user_model)
                    return redirect('/admin')
                else:
                    return redirect(
                        url_for(
                            'login',
                            error_message='Usuário ou Senha inválidos!',
                        )
                    )
        return render_template(
            'login.html',
            error_message=request.args.get('error_message'),
            form=form,
        )

    @app.get('/logout')
    def logout():
        try:
            with Session() as session:
                query = select(User).where(
                    User.username == current_user.username
                )
                user_model = session.scalars(query).first()
                if user_model:
                    user_model.authenticated = False
                    session.commit()
        except AttributeError:
            pass
        logout_user()
        return redirect(url_for('login'))
