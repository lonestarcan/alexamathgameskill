from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
	#the Alexa session ID
	id = db.Column(db.String(100), primary_key = True) 
	#the math question
	question = db.Column(db.Text)
	#the math answer
	answer = db.Column(db.Integer)
	
	def __init__(self, user_id):
		self.id = user_id
		self.question = "What is 0 plus 0?"
		self.answer = 0
