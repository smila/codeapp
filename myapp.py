#install the following dependencies (flask,flask-sqlalchemy, flask-marshmallow, marshmallow-sqlalchemy)
#flask ===> web framework built with a small core 
#flask-SQLAlchemy ===> an extension for Flask that adds support for SQLAlchemy to your application
#flask-marshmallow ===> an object serialization/deserialization library
#OS  ===> The OS module in python provides functions for interacting with the operating system. It will be used to set base url for our database

#import dependencies
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#init app
app = Flask(__name__)

#define base directory
basedir = os.path.abspath(os.path.dirname(__file__))

#Setup Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'web_api.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initialize SQLAlchemy
db = SQLAlchemy(app)

#initialize Marshmallow
ma = Marshmallow(app)

#code Class/Model
class Codes(db.Model):

	#create fields
	id = db.Column(db.Integer, primary_key=True)
	category_code = db.Column(db.String(200))
	diagnosis_code = db.Column(db.String(200))
	full_code = db.Column(db.String(200))
	abv_description = db.Column(db.String(200))
	full_description = db.Column(db.String(200))
	disease = db.Column(db.String(200))

	#initialise or constructor
	def __init__(self, category_code, diagnosis_code, full_code, abv_description, full_description, disease ):
		self.category_code = category_code
		self.diagnosis_code = diagnosis_code
		self.full_code = full_code
		self.abv_description = abv_description
		self.full_description = full_description
		self.disease = disease

#create code schema
class CodeSchema(ma.Schema):
	#indicate fields you want to show
	class Meta:
		fields = ('id', 'category_code', 'diagnosis_code', 'full_code', 'abv_description', 'full_description', 'disease')

#initialize schema
#for single row
code_schema = CodeSchema(strict=True)
#for many rows
codes_schema = CodeSchema(many=True, strict=True) 


#create a code
#create a route and restrict it to POST method
@app.route('/code', methods=['POST'])
def add_code():
	category_code = request.json['category_code']
	diagnosis_code = request.json['diagnosis_code']
	full_code = request.json['full_code']
	abv_description = request.json['abv_description']
	full_description = request.json['full_description']
	disease = request.json['disease']

	#receive new entry
	new_code = Codes(category_code, diagnosis_code, full_code, abv_description, full_description, disease)

	#store data into table
	db.session.add(new_code)
	db.session.commit()

	return code_schema.jsonify(new_code)

#get all codes
@app.route('/code', methods=['GET'])
def get_codes():
	all_codes = Codes.query.all()
	result = codes_schema.dump(all_codes)
	return jsonify(result.data)

#get single code
@app.route('/code/<id>', methods=['GET'])
def get_code(id):
	code = Codes.query.get(id)
	result = code_schema.dump(code)
	return jsonify(result.data)

#update a code
@app.route('/code/<id>', methods=['PUT'])
def update_code(id):
	fetch_codes = Codes.query.get(id)

	category_code = request.json['category_code']
	diagnosis_code = request.json['diagnosis_code']
	full_code = request.json['full_code']
	abv_description = request.json['abv_description']
	full_description = request.json['full_description']
	disease = request.json['disease']

	fetch_codes.category_code = category_code
	fetch_codes.diagnosis_code = diagnosis_code
	fetch_codes.full_code = full_code
	fetch_codes.abv_description = abv_description
	fetch_codes.full_description = full_description
	fetch_codes.disease = disease

	db.session.commit()

	return code_schema.jsonify(fetch_codes)


#delete code
@app.route('/code/<id>', methods=['DELETE'])
def delete_code(id):
	code = Codes.query.get(id)
	db.session.delete(code)
	db.session.commit()

	result = code_schema.dump(code)
	return jsonify(result.data)


# Run Server
if __name__ == '__main__':
	app.run(debug=True)