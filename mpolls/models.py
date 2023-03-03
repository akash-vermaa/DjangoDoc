from pymongo import MongoClient, errors
from DjangoDoc.settings import DATABASES
from bson.json_util import loads, dumps
from django.utils import timezone
import datetime

def Use(collection_name):
	db_name= 'testDB'
	try:
		client = MongoClient(DATABASES['mongodb']['HOST'])
		collection = client[db_name][collection_name]

		return collection
	except:
		print("Something went wrong")

	finally:
		client.close()

class Question:
	collection_name = 'questions'

	def __init__(self, question_text, pub_date, choice_names):
		self.question_text = question_text
		self.pub_date = pub_date
		self.choices = [{'choice_name': choice_name, 'votes':0} for choice_name in choice_names]

	def was_published_recently(self):
		now = timezone.now()
		return now >= self.pub_date >= now - datetime.timedelta(days=30)

	def __str__(self):
		return {
			'question_text': self.question_text,
			'pub_date': self.pub_date,
			'choices': self.choices
		}

	def toJSON(self):
		return {
			'question_text': self.question_text,
			'pub_date': self.pub_date,
			'choices': self.choices
		}

	def save(self):
		collection = Use(Question.collection_name)
		out = collection.insert_one(dumps({
				"question_id":{"$inc":1},
				'question_text': self.question_text,
				'pub_date': self.pub_date,
				'choices': self.choices
			}))
		print(out)


	@staticmethod
	def get(query={}):

		collection = Use(Question.collection_name)

		try:
			return [data for data in collection.find(query)]

		except:
			print("Unable to read data")

	@staticmethod
	def all():
		collection = Use(Question.collection_name)

		try:
			return [data for data in collection.find({})]

		except:
			print("Unable to read data")

	
		




