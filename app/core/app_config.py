from dotenv import load_dotenv
import os



load_dotenv()

#Server Details
PORT_NUMBER = os.getenv('PORT')

#Postgres
DATABASE_URL = os.getenv('DATABASE_URL')
