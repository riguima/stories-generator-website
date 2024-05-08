from flask import render_template
from sqlalchemy import select

from stories_generator_website.database import Session
from stories_generator_website.models import Product


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
