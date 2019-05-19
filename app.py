#import the flask library
from flask import Flask, render_template
#Get the SDK for Alexa 
from flask_ask import Ask, statement, question, session
#Get the SDK for Google Home
#import the database object and 
from models import db, Users
#import os module to get environment variable
import os
#import random to generate questions
import random
#This is a new comment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db.init_app(app)

#Connecting Website to Amazon Alexa
ask = Ask(app,'/game')

#This generates a random question for the user
def ask_a_question():
	user_id = session.user.userId
	user = Users.query.filter_by(id = user_id).first()
	if user == None:
		#Create a new user
		new_user = Users(user_id)
		db.session.add(new_user)
		db.session.commit()
		user = Users.query.filter_by(id = user_id).first()
	
	#Generate a question type
	question_type = random.randint(1,4)
	
	if question_type == 1:
		#Provide an addition question
		number_one = random.randint(1,20)
		number_two = random.randint(1,20)
		addition_answer = number_one + number_two
		user.answer = addition_answer
		user.question = 'Question: What is {} plus {}?'.format(number_one, number_two)
		db.session.commit()
		return user.question
	
	elif question_type == 2:
		#Provide a subtraction question
		number_one = random.randint(1,20)
		subtraction_answer = random.randint(1,20)
		number_two = number_one + subtraction_answer
		user.answer = subtraction_answer
		user.question = 'Question: What is {} minus {}?'.format(number_two, number_one)
		db.session.commit()
		return user.question
	
	elif question_type == 3:
		#Provide a multplication question
		number_one = random.randint(1,12)
		number_two = random.randint(1,12)
		multiplication_answer = number_one * number_two
		user.answer = multiplication_answer
		user.question = 'Question: What is {} times {}?'.format(number_one, number_two)
		db.session.commit()
		return user.question
	
	else:
		#Provide a division question
		number_one = random.randint(1,12)
		division_answer = random.randint(1,12)
		number_two = division_answer * number_one
		user.answer = division_answer
		user.question = 'Question: What is {} divided by {}?'.format(number_two, number_one)
		db.session.commit()
		return user.question

#This is a math game
#This checks if the user's question is correct or incorrect.
def answer_a_question(user_answer):
	user_id = session.user.userId
	user = Users.query.filter_by(id = user_id).first()
	if user.answer == user_answer:
		resp = 'Correct. The answer is {}. Would you like another question?'.format(user.answer)
	else:
		resp = 'Incorrect. The answer is {}. Would you like another question?'.format(user.answer)
	return resp

#This repeats the question to the user.
def repeat_a_question():
	user_id = session.user.userId
	user = Users.query.filter_by(id = user_id).first()
	return user.question

def generate_random_string(min_int, max_int):
	char_bank = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
	return_string = ""
	random_length = random.randint(min_int,max_int)
	for x in range(random_length):
		return_string += char_bank[random.randint(0, len(char_bank) - 1)]
	return return_string

#AMAZON ALEXA 
@ask.launch
def launch_skill():
	welcome_message = 'Welcome. Would you like a math problem?'
	return question(welcome_message)

@ask.intent('AskQuestionIntent')
def offer_question():
	question_message = ask_a_question()
	return question(question_message)

@ask.intent('AnswerQuestionIntent', convert = {'numberAnswer':int})
def offer_answer(numberAnswer):
	answer_message = answer_a_question(numberAnswer)
	return question(answer_message)

@ask.intent('RepeatQuestionIntent')
def offer_repeat_question():
	question_message = repeat_a_question()
	return question(question_message)

@ask.intent('NoIntent')
def offer_close():
	close_message = 'Thank you. Goodbye.'
	return statement(close_message)


@app.route('/')
def index():
	return 'Hello World'

if __name__ == '__main__':
	app.run(debug = True)
