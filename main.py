import csv

from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Regexp

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

bootstrap = Bootstrap5(app)


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------
class CafeForm(FlaskForm):
	cafe = StringField('Coffee Name', validators=[DataRequired(message='Please enter the cofee name here.')])
	location = StringField('Google Maps Link (URL)',
						   validators=[DataRequired(message='Please enter the location URL here.'), Regexp(
							   r'(https:\/\/maps.app.goo.gl\/[\w]+)|(^https:\/\/www.google.com\/maps\/)',
							   message='Please enter a valid location URL.')])
	open = StringField('Open (eg. 08:30am)',
					   validators=[DataRequired(message='Please enter the opening time here.'),
								   Regexp(r"(([0]?[\d])|([1][0-2]))(:([0-5][\d]))?(am|AM|pm|PM)",
										  message='Please enter a valid time here.')])
	close = StringField('Close (eg. 7:30pm)',
						validators=[DataRequired(message='Please enter the closing time here.'),
									Regexp(r"(([0]?[\d])|([1][0-2]))(:([0-5][\d]))?(am|AM|pm|PM)",
										   message='Please enter a valid time here.')])
	# open = DateTimeLocalField('Open', validators=[DataRequired()])
	# close = DateTimeLocalField('Close', validators=[DataRequired()])
	coffee_rating = SelectField('Coffee Rating',
								choices=['Rate the Coffee', '✘', '☕️', '☕️☕️','☕️☕️☕️', '☕️☕️☕️☕️', '☕️☕️☕️☕️☕️'],
								validators=[DataRequired()])
	wifi_rating = SelectField('Wi-Fi Rating',
							  choices=['Rate the Wi-Fi', '✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'],
							  validators=[DataRequired()])
	power_rating = SelectField('Power Outlet Rating',
							   choices=['Rate the Power Outlet', '✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'],
							   validators=[DataRequired()])
	submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
	return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
	form = CafeForm()
	if request.method == 'GET':
		return render_template('add.html', form=form)
	elif request.method == 'POST' and form.validate_on_submit():
		# print("True")
		# Exercise:
		# Make the form write a new row into cafe-data.csv
		# with   if form.validate_on_submit()
		row = [form.cafe.data, form.location.data, form.open.data, form.close.data, form.coffee_rating.data,
			   form.wifi_rating.data, form.power_rating.data]
		with open('cafe-data.csv', 'a', newline='', encoding='utf-8') as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow(row)
		return redirect('./cafes')
	else:
		return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
	with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
		csv_data = csv.reader(csv_file, delimiter=',')
		list_of_rows = []
		for row in csv_data:
			list_of_rows.append(row)
	return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
	app.run(debug=True)
