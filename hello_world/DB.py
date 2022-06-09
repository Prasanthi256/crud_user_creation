import pymysql

class DB(object):
    def __init__(self, host, db_user, db_password,db_name,port):
        self.conn = pymysql.connect(host=host, user=db_user, passwd=db_password, db=db_name, port=int(port),connect_timeout=5)
        print("SUCCESS: Connection to RDS MySQL instance succeeded")

    def __del__(self):
        self.conn.close()
        print("SUCCESS: Connection to RDS MySQL instance closed")

    def query(self, sql):
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            self.conn.commit()
            return cursor.fetchall()