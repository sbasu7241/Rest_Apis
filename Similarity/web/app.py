from flask import Flask,jsonify,request
from flask_restful import Api,Resource
from pymongo import MongoClient
import bcrypt
""
app = Flask(__name__)

api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client["SimilarityDB"]
users = db["Users"]

def UserExist(username):
	if users.find({"Username":username}).count()==0:
		return False
	else:
		return True


class Register(Resource):
	def post(self):
		postedData = request.get_json()
		
		username = postedData["Username"]
		password = postedData["Password"]
		
		if UserExist(username):
			retJson={'status':301,'msg':"Invalid Username"}
			return jsonify(retJson)
		
		hashed_pw = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
		
		#Store username and pw into the database

		users.insert_one({"Username":username,"Password":hashed_pw,"Tokens":10})		

 		retJson = {"status": 200,"msg": "You successfully signed up for the API"}

		return jsonify(retJson)

class Detect(Resource):
	def post(self):
		
		#Step 1 get the posted data		
		postedData = request.get_json()
	
		#Step 2 is to read the data
		username = postedData["username"]
		password = postedData["password"]
		text1 = postedData["text1"]
		text2 = postedData["text2"]

		
		if not UserExist(username):
			retJson={'status':301,'msg':"Invalid Username"}
			return jsonify(retJson)

		#Step 3 verify username password match
		correct_pw = VerifyPassword(username, password)

		if not correct_pw:
			retJson={'status':302,'msg':"Incorrect Password"}
			return jsonify(retJson)

		#Step 4 Verify user has enough tokens
		
		num_tokens = countTokens(username)
		
		if num_tokens <= 0:
			retJson = {'status':303,'msg':"You are out of tokens, please refill!"}
			return jsonify(retJson)

		#Calculate edit distance between text1, text2

		import spacy
		nlp = spacy.load('en_core_web_sm')
		text1 = nlp(text1)
		text2 = nlp(text2)

		# Ratio is a number from 0 and 1 the closer to 1, the more similar text1
		# text2 are
	
		ratio = text1.similarity(text2)
		
		retJson={"status":200,"similarity":ratio,"msg":"Similarity score is stored successfully"}
		
		current_tokens = countTokens(username)
		
		users.update({"Username":username},{$set:{"Tokens":current_tokens-1}})
	
		return jsonify(retJson)





		

		





		



def VerifyPassword(username,password):
	if not UserExist(username):
		return False

	hashed_pw = users.find({"Username":username})[0]["Password"]

	if bcrypt.checkpw(password,hashed_pw):
		return True
	else:
		return False
	
def CountTokens(username):

	tokens = tokens.find({"Username":username})[0]["Tokens"]
	return tokens







		
			
		





