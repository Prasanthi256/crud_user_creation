import json
import rds_config
import  pymysql
import traceback
#import connection
from DB import DB
from flask import request
from flask_lambda import FlaskLambda
app = FlaskLambda(__name__)

username = rds_config.db_username
password = rds_config.db_password
name = rds_config.db_name
endpoint= rds_config.db_endpoint
host=rds_config.db_host

db=DB(endpoint,username,password,name,host)


@app.route('/hello')
def index():
	rows=db.query("select user_id,firstname,lastname,emailid from users")
	col_names =('user_id','firstname','lastname','emailid')
	query_result = [{col_names:row for col_names,row in zip(col_names,row)}for row in rows]
	if len(rows) == 0 :
		query_result = {"message" : "No user entry"}
	return (
		json.dumps(query_result,indent=4, sort_keys=True),
		200,
		{'Content-Type': 'application/json'}
	)

@app.route('/user',methods =['GET'])
def get_user():
	args = request.args
	firstname=args.get("name")
	rows=db.query("select firstname,lastname,emailid,user_id from users where  firstname like '%s'"%(firstname))
	col =('firstname','lastname','emailid','user_id')
	if  len(rows) == 1:
		query_result = dict(zip(col,rows[0]))
	else:
		query_result = {"message" : "No data  for that  users"}
	return json_message(query_result)


@app.route('/create',methods = ['POST'])
def  create_user():
	res=(request.json)
	firstname= res['firstname']
	lastname= res['lastname']
	emailid=res['emailid']
	user_password=res['password']
	rows=db.query("select count(*) from users  where firstname= '%s'" %(firstname))
	if (rows[0][0]) == 1 :
		res={"message":"User entry already exists"}
	else:
		result=db.query("insert  into users(firstname,lastname,emailid,password) values ('%s', '%s', '%s', 'MD5(%s)')" %(firstname,lastname,emailid,user_password))
		res={"message":"User entry was  created "}
	return json_message(res)


@app.route('/userdelete/<int:id>', methods= ['DELETE'])
def  delete_user(id):
	res=db.query("delete from users where  user_id = %s" %(id))
	return json_message({"message": "user entry  deleted successfully"})


@app.route('/update/<int:id>', methods = ['POST'])
def  update_user(id):
	res=request.json
	key = list(res.keys())[0]
	print(key)
	rows=db.query("select count(*) from users where user_id = %s" %(id))
	if rows[0][0] == 0:
		result = {'message' : "No entry exists  for that user_id"}
	else:
		res=db.query("update  users  set " +key + " = '%s' where user_id = %s " %(res[key],id))
		result = {"message" : "user details updated  successfully"}

	return json_message(result)

def  json_message(data,response_code=200):
	return (
		json.dumps(data,indent=4, sort_keys=True),
		response_code,
		{'Content-Type': 'application/json'}
	)
