from flask import Flask,jsonify,request
app = Flask(__name__)

@app.route('/')
def helloworld():
	return "Hello World"

@app.route('/hithere')
def ho_there():
	age = 2*5
	retjson = {
			"Name":"Soumyadeep Basu",
			"Age":age,
			"Phones":[
			{
				"phonename": "Iphone8",
				"phoneNumber": 7003120498

			},
			{
				"phonename": "Lenovo",
				"phoneNumber": 9433093321	

			}

				]
		 }
	return jsonify(retjson)
			
@app.route('/postjson', methods = ['POST'])
def postJsonHandler():
    
	content = request.get_json()

	if "y" not in content:
		return "ERROR",305

	x = content["x"]
	y = content["y"]
	
	z = x+y

	return jsonify({"z":z})		

if __name__=="__main__":
	app.run(debug=True)
