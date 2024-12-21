import cohere
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Set a secret key for CSRF protection


class Form(FlaskForm):
    text = StringField('Enter text to search', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = Form()
    co = cohere.Client('wJsfZMI6Q8KjPa4rcWYajCgaWZFLEzf8RtK1S5B8')  # Your Cohere API key

    if form.validate_on_submit():
        text = form.text.data
        try:
            # Try using a general valid model like 'command-xlarge'
            response = co.generate(
                model='command-xlarge',  # Replace with a valid model name
                prompt=text,
                max_tokens=300,
                temperature=0.9,
                k=0,
                p=0.75,
                stop_sequences=[],
                return_likelihoods='NONE'
            )
            output = response.generations[0].text
            return render_template('home.html', form=form, output=output)
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return render_template('home.html', form=form, output=None)


if __name__ == "__main__":
    app.run(debug=True)


