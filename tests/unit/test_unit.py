import  requests
import json
#from hello_world import app,rds_config



class  Testapi:

	def  test_get_all_users(self):
		response=requests.get("https://iwy1rvvzjf.execute-api.ap-south-1.amazonaws.com/Prod/hello")
		print(response.json())
		data = response.headers.get('Content-Type')
		assert response.status_code == 200
		assert data == "application/json"

	def test_get_user(self):
		payload={
		"emailid": "krish.a@gmail.com",
		"firstname": "krishna",
		"lastname": "kumar",
		"user_id": 8
		}
		params={"name":"krishna"}
		response_get_user = requests.get("https://iwy1rvvzjf.execute-api.ap-south-1.amazonaws.com/Prod/user",params=params)
		assert response_get_user.json() == payload

	def test_get_user_nodata(self):
		payload={
		"message": "No data  for that  users"
		}
		params={"name":"sweety"}
		response = requests.get("https://iwy1rvvzjf.execute-api.ap-south-1.amazonaws.com/Prod/user",params=params)
		assert response.json() == payload

	def test_exist_user(self):
		data= {
		"firstname":"penny",
		"lastname":"k",
		"emailid":"penny.k@gmail.com",
		"password":"penny"
		}
		message = {"message": "User entry already exists"}
		headers={"Content-Type": "application/json"}
		response_exist_user=requests.post("https://iwy1rvvzjf.execute-api.ap-south-1.amazonaws.com/Prod/create",headers=headers,json=data)
		assert response_exist_user.status_code == 200
		assert response_exist_user.json() == message

	def  test_create_user(self):
		data= {
		"firstname":"ravi",
		"lastname":"kumar",
		"emailid":"ravi.kumar@gmail.com",
		"password":"ravi1"
		}
		message = {"message": "User entry was  created "}
		headers={"Content-Type": "application/json"}
		response_create_user=requests.post("https://iwy1rvvzjf.execute-api.ap-south-1.amazonaws.com/Prod/create",headers=headers,json=data)
		assert response_create_user.status_code == 200

	def test_update_user(self):
		data = {"lastname": "Kumar"}
		message = {"message": "user details updated successfully"}
		headers= {"Content-Type": "application/json"}
		response_update_user= requests.post("https://iwy1rvvzjf.execute-api.ap-south-1.amazonaws.com/Prod/update/4",headers=headers,json=data)
		assert  response_update_user.status_code == 200

	def test_delete_user(self):
		response_delete_user= requests.delete(" https://iwy1rvvzjf.execute-api.ap-south-1.amazonaws.com/Prod/userdelete/18")
		assert response_delete_user.status_code == 200














