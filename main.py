import adal
import pyodbc
import struct
import json

def read_config():
    config = {}
    with open("./config/config.json") as config_file:
        config = json.load(config_file)
    return config

def get_token(tenant_id, client_id):
    context = adal.AuthenticationContext(f"https://login.microsoftonline.com/{tenant_id}")
    user_code_response = context.acquire_user_code('https://database.windows.net/', client_id)

    print(user_code_response['message'])

    token = context.acquire_token_with_device_code("https://database.windows.net/", user_code_response, client_id)

    return token

def create_connection(access_token, database_server, database_name):

    DRIVER_NAME = "ODBC Driver 17 for SQL Server"

    connString = f"Driver={DRIVER_NAME};SERVER={database_server};DATABASE={database_name}"

    #get bytes from token obtained
    tokenb = bytes(access_token, "UTF-8")
    exptoken = b''

    for i in tokenb:
        exptoken += bytes({i})
        exptoken += bytes(1)
    tokenstruct = struct.pack("=i", len(exptoken)) + exptoken

    SQL_COPT_SS_ACCESS_TOKEN = 1256 

    conn = pyodbc.connect(connString, attrs_before = { SQL_COPT_SS_ACCESS_TOKEN: tokenstruct})

    return conn

def print_rows(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PEOPLE")
    row = cursor.fetchone()
    while row:
        print (str(row[0]) + " " + str(row[1]))
        row = cursor.fetchone()

def main():
    print("Reading Config")
    config = read_config()

    client_id = config['client_id']
    tenant_id = config['tenant_id']

    print("Getting Token")
    token = get_token(tenant_id, client_id)

    database_name = config['database_name']
    database_server = config['database_server']
    
    print("Connecting to Database")
    conn = create_connection(token["accessToken"], database_server, database_name)

    print("Printing Rows")
    print_rows(conn)

if __name__ == '__main__':
    main()