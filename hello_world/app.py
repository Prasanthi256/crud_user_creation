import json
import rds_config
import  pymysql
import traceback
#import connection
from flask import request
from flask_lambda import FlaskLambda
app = FlaskLambda(__name__)

username = rds_config.db_username
password = rds_config.db_password
name = rds_config.db_name
endpoint= rds_config.db_endpoint
host=rds_config.db_host



@app.route('/hello')
def index():
	try:
		conn = pymysql.connect(host=endpoint, user=username, passwd=password, db=name, port=int(host),connect_timeout=5)
		print("SUCCESS: Connection to RDS MySQL instance succeeded")
		connection = conn.cursor()
		connection.execute("select user_id,firstname,lastname,emailid from users")
		col_names =('user_id','firstname','lastname','emailid')
		rows=connection.fetchall()
		query_result = [{col_names:row for col_names,row in zip(col_names,row)}for row in rows]
		if len(rows) == 0 :
			query_result = {"message" : "No user entry"}
	except Exception as e:
		print(e)
	finally:
		connection.close()
		conn.close()
	return (
		json.dumps(query_result, indent=4, sort_keys=True),
		200,
		{'Content-Type': 'application/json'}
		)


@app.route('/user',methods =['GET'])
def get_user():
	args = request.args
	firstname=args.get("name")
	try:
		conn = pymysql.connect(host=endpoint, user=username, passwd=password, db=name, port=int(host),connect_timeout=5)
		print("SUCCESS: Connection to RDS MySQL instance succeeded")
		connection = conn.cursor()
		connection.execute("select firstname,lastname,emailid,user_id from users where  firstname like %s",firstname)
		rows=connection.fetchall()
		col =('firstname','lastname','emailid','user_id')
		if  len(rows) == 1:
			query_result = dict(zip(col,rows[0]))
		else:
			query_result = {"message" : "No data  for that  users"}
	except Exception:
		print(traceback.format_exc())
	finally:
		connection.close()
		conn.close()
	return (
		json.dumps(query_result,indent=4, sort_keys=True),
		200,
		{'Content-Type': 'application/json'}
	)

@app.route('/create',methods = ['POST'])
def  create_user():
	res=(request.json)
	firstname= res['firstname']
	lastname= res['lastname']
	emailid=res['emailid']
	user_password=res['password']
	try:
		conn = pymysql.connect(host=endpoint, user=username, passwd=password, db=name, port=int(host),connect_timeout=5)
		print("SUCCESS: Connection to RDS MySQL instance succeeded")
		connection = conn.cursor()
		connection.execute("select count(*) from users  where firstname= %s" ,firstname)
		rows = connection.fetchall()
		if (rows[0][0]) == 1 :
			res={"message":"User entry already exists"}
		else:
			connection.execute("insert  into users(firstname,lastname,emailid,password) values (%s, %s, %s, MD5(%s))",(firstname,lastname,emailid,user_password))
			conn.commit()
			res={"message":"User entry was  created "}
	except Exception as e:
		print(e)
	finally:
		connection.close()
		conn.close()
	return (
		json.dumps(res,indent = 4,sort_keys=True),
		200,
		{'Content-Type': 'application/json'})

@app.route('/userdelete/<int:id>', methods= ['DELETE'])
def  delete_user(id):
	try:
		conn = pymysql.connect(host=endpoint, user=username, passwd=password, db=name, port=int(host),connect_timeout=5)
		print("SUCCESS: Connection to RDS MySQL instance succeeded")
		connection = conn.cursor()
		connection.execute("delete from users where  user_id = %s",id)
		conn.commit()
	except Exception as e:
		print(e)
	finally:
		connection.close()
		conn.close()
	return (
		json.dumps({"message": "user entry  deleted successfully"})		
	)
@app.route('/update/<int:id>', methods = ['POST'])
def  update_user(id):
	try:

		res=request.json
		key = list(res.keys())[0]
		print(key)
		conn = pymysql.connect(host=endpoint, user=username, passwd=password, db=name, port=int(host),connect_timeout=5)
		print("SUCCESS: Connection to RDS MySQL instance succeeded")
		connection=conn.cursor()
		connection.execute("select count(*) from users where user_id = %s",id)
		rows=connection.fetchall()
		if rows[0][0] == 0:
			result = {'message' : "No entry exists  for that user_id"}
		else:
			connection.execute("update  users  set " +key + " = %s where user_id = %s ",(res[key],id))
			conn.commit()
			result = {"message" : "user details updated  successfully"}
	except Exception as e:
		print(e)
	finally:
		connection.close()
		conn.close()
	return(
		json.dumps(result)
		)


