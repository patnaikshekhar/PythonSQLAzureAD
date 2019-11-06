import adal
import pyodbc
import struct
import json

config = {}
with open("config.json") as config_file:
    config = json.load(config_file)

CLIENT_ID = config['client_id']
TENANT_ID = config['tenant_id']
DATABASE_NAME = config['database_name']
DATABASE_SERVER = config['database_server']
DRIVER_NAME = "ODBC Driver 17 for SQL Server"

context = adal.AuthenticationContext(f"https://login.microsoftonline.com/{TENANT_ID}")
user_code_response = context.acquire_user_code('https://database.windows.net', CLIENT_ID)

print(user_code_response['message'])

token = context.acquire_token_with_device_code("https://database.windows.net", user_code_response, CLIENT_ID)

connString = f"Driver={DRIVER_NAME};SERVER={DATABASE_SERVER};DATABASE={DATABASE_NAME}"

#get bytes from token obtained
tokenb = bytes(token["accessToken"], "UTF-8")
exptoken = b''

for i in tokenb:
    exptoken += bytes({i})
    exptoken += bytes(1)
tokenstruct = struct.pack("=i", len(exptoken)) + exptoken

SQL_COPT_SS_ACCESS_TOKEN = 1256 

conn = pyodbc.connect(connString, attrs_before = { SQL_COPT_SS_ACCESS_TOKEN: tokenstruct})

cursor = conn.cursor()
cursor.execute("SELECT * FROM PEOPLE")
row = cursor.fetchone()
while row:
    print (str(row[0]) + " " + str(row[1]))
    row = cursor.fetchone()