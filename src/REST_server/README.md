This project is an asynchronous HTTP web server over Python3 using asynchio module. It includes a REST web interface (without GUI) providing database management features. MySQL has been used as database for this project<br />

The folder has 7 files whose details are mentioned below:<br />


* aiomysql_client.py : This is the file the actually connects with database and executes the SQL query. It includes a class whose object is created in CES_API_DB.py <br />

* api_server.py : It is the actual asynchronous web server which listens to HTTP query on defined domain and port and calls the relevant function <br />

* CES_API_DB.py : It is the basic processing unit of system which creates SQL queries that are then forwarded to aiomysql_client.py for execution. It also validates the data by providing data to Validator.py<br />

* errorsfile.py : It is a class to custom define an error and deal with the error code and message<br />

* Validator.py : It validates in input fields to comply with the constraints<br />

* cert.pem : It is a certificate used when SSL needs to be implemented and queries are forced to go through HTTPS<br />

* key.key : It is a key used when SSL needs to be implemented and queries are forced to go through HTTPS<br />






