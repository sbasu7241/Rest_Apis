from flask import Flask,jsonify,request
from flask_restful import Api,Resource
from pymongo import MongoClient
import bcrypt


client = MongoClient("mongodb://db:27017")

database = client["BankApi"]
users = database["Users"]

app = Flask(__name__)

api = Api(app)

def UserExist(username):
	if users.find({"Username":username}).count() == 0:
		return False
	else
		return True

def verifyPw(username,password):

	if not UserExist(username):
		return False
	else:
		hashedpw = users.find({"Username":username})[0]["Password"]
		
		if bcrypt.checkpw(password.encode('utf-8'),hashedpw):
			return True
		else:
			return False
			
class Register(Resource):
	def post(self):
		postedData = request.get_json()

		username = postedData["username"]
		password = postedData["password"]

		if UserExist(username):
			retJson = {'status':301,'msg':"Invalid Username"}
			return jsonify(retJson)
		
		hashed_pw = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

		#Insert username and password into database

		users.insert({"Username":username,"Password":password,"Own":0,"Debt":0})

		retJson = ({"status":200,"msg":"You successfully signed up for the api"})

		return jsonify(retJson)

def cashWithUser(username):
	
	cash = users.find({"Username":username})[0]["Own"]
	return cash

def debtWithUser(username):
	
	debt = users.find({"Username":username})[0]["Debt"]
	return debt

def generateReturnDictionary(status, msg):
	retJson = {"status": status,"msg": msg}
	return retJson

def verifyCredentials(username,password):

	if not UserExist(username):
	        return generateReturnDictionary(301, "Invalid Username"), True
	
	correct_pw = verifyPw(username, password)

	if not correct_pw:
		return generateReturnDictionary(302, "Incorrect Password"), True

	return None, False

def updateAccount(username,balance):
	
	users.update({"Username":username},{"$set":{"Own":balance}})


def updateDebt(username, balance):
    users.update({"Username": username},{"$set":{"Debt": balance}})


class Add(Resource):
	def post(self):
		postedData = request.get_json()

	username = postedData["username"]
	password = postedData["password"]
	money = postedData["amount"]

	retJson, error = verifyCredentials(username, password)
	if error:
		return jsonify(retJson)	

	if money<=0:
		return jsonify(generateReturnDictionary(304,"The money amount entered must be greater than 0"))

	cash = cashWithUser(username)
	money -= 1 #Transaction Fee

	#Add transaction fee to Bank account

	bank_cash = cashwithUser("BANK")
	updateAccount("BANK",bank_cash+1)


	# Add remaining to user
	updateAccount(username, cash+money)

	return jsonify(generateReturnDictionary(200, "Amount Added Successfully to account"))

class Balance(Resource):
	
	def post(self):
		postedData = request.get_json()

		username = postedData["username"]
		password = postedData["password"]

		retJson, error = verifyCredentials(username, password)
		if error:
			return jsonify(retJson)

		retJson = users.find({"Username":username},{"Password":0,"_id":0})[0]
		
		return jsonify(retJson)








	








	





			

		
		








	

























		
		














# Add resources

api.add_resource(Register,"/register")		
api.add_resource(Add,"/add")			
#api.add_resource(Transfer,"/transfer")
#api.add_resource(CheckBalance,"/checkBal")
#api.add_resource(TakeLoan,"/takeLoan")
#api.add_resource(PayLoan,"/payLoan")














































if __name__=="__main__":
	app.run(host="0.0.0.0")
