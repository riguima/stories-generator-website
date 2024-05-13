from flask import abort, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from sqlalchemy import select
from datetime import timedelta

from stories_generator_website.database import Session
from stories_generator_website.forms import LoginForm
from stories_generator_website.models import Product, User, Configuration
from stories_generator_website.utils import get_today_date


def init_app(app):
    def remove_old_promotions(username):
        with Session() as session:
            query = select(Product).where(Product.username == username)
            products = [p for p in session.scalars(query).all() if p.create_datetime.date() < get_today_date() - timedelta(days=7)]
            for product in products:
                session.delete(product)
            session.commit()
    
    @app.get('/')
    def index():
        return redirect('https://promodegrupo.com.br/')

    @app.get('/<string:username>')
    def user_page(username):
        remove_old_promotions(username)
        with Session() as session:
            query = select(Product).where(Product.username == username)
            if (
                request.args.get('website')
                and request.args.get('website') != 'all'
            ):
                query = query.where(Product.website == request.args['website'])
            if request.args.get('search'):
                query = query.where(Product.name.like(request.args['search']))
            query = query.order_by(Product.create_datetime.desc())
            products = session.scalars(query).all()
            query = select(Configuration).where(Configuration.username == username)
            configuration = session.scalars(query).first()
            return render_template(
                'index.html',
                products=products,
                username=username,
                current_page='index',
                configuration=configuration,
            )

    @app.get('/<string:username>/promocoes-do-dia')
    def today_promotions(username):
        remove_old_promotions(username)
        with Session() as session:
            query = (
                select(Product)
                .where(Product.username == username)
            )
            products = [p for p in session.scalars(query).all() if p.create_datetime.date() == get_today_date()]
            query = select(Configuration).where(Configuration.username == username)
            configuration = session.scalars(query).first()
            return render_template(
                'index.html',
                products=products,
                username=username,
                current_page='today_promotions',
                configuration=configuration,
            )

    @app.get('/<string:username>/produto/<int:product_id>')
    def product(username, product_id):
        remove_old_promotions(username)
        with Session() as session:
            query = select(Product).where(Product.id == product_id)
            product = session.scalars(query).first()
            query = (
                select(Product)
                .where(Product.username == username)
            )
            products = [p for p in session.scalars(query).all() if p.create_datetime.date() == get_today_date()]
            query = select(Configuration).where(Configuration.username == username)
            configuration = session.scalars(query).first()
            if product:
                return render_template('product.html', product=product, today_products=products[:8], username=username, configuration=configuration)
            else:
                return abort(404)

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
            success_message=request.args.get('success_message'),
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
