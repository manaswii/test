from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
app.config['SECRET_KEY'] = 'eb97415eb47c3aa517abb5ebd50327f3'

from application import app, db
from flask import render_template, redirect, url_for, flash
from forms import CreateUserForm
from models import Data

@app.route('/')
def index():
    data = Data.query.all()
    return render_template('index.html', data=data)

@app.route('/checkout', methods=['GET', 'POST'])
def create_customer():
    form = CreateUserForm()

    if form.validate_on_submit():
        new_data = Data(
            email = form.email.data,
            state = form.state.data,
            postalcode = form.postalcode.data,
            contact = form.contact.data,
            paymentmethod = form.paymentmethod.data,
            cardholder = form.cardholder.data,
            cardnumber = form.cardnumber.data,
            expiry = form.expiry.data,
            cvc = form.cvc.data,
        )
        db.session.add(new_data)
        db.session.commit()

        flash(f'Data has been submitted!')
        return redirect(url_for('index'))

    return render_template('checkout.html', form=form)