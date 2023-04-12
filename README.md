Required python packages:  
fastapi pymongo python-dotenv bcrypt jwt fpdf uvicorn

You should have a .env file with the two following fields. dbName is the name of the database in mongodb and MONGO_URI is the connection string for mongodb.  
dbName=""  
MONGO_URI=""

launch with:  
python3 -m uvicorn main:app --host 0.0.0.0
