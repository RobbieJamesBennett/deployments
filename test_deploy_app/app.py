from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from sqlalchemy import create_engine
import pandas as pd
import secrets
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
# SQL Login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Save the credentials in Flask's session
        session['username'] = username
        session['password'] = password
        # Redirect the user to the page where you want to show the SQL data
        return redirect(url_for('show_data'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/data')
def show_data():
    # Get the credentials from Flask's session
    username = session.get('username')
    password = session.get('password')

    if not username or not password:
        # If the credentials are not present in the session, redirect the user to the login page
        return redirect(url_for('login'))

    # Use the credentials to create a SQLAlchemy engine
    conn_str = f"mssql+pyodbc://{username}:{password}@server_name/database_name?driver=SQL Server"
    engine = create_engine(conn_str)
    df = pd.read_sql("SELECT * FROM test_table", engine)
    return render_template('data.html', data=df.to_html())

if __name__ == '__main__':
    app.run(debug=True)





