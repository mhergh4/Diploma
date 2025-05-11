import os
import google.generativeai as genai

# Flask Configuration
SECRET_KEY = 'itsMySecretKey'

# MySQL Configuration
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'mhersql'
MYSQL_DATABASE = 'my_shop'

# Email Configuration
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'auth.myshop.world@gmail.com'
MAIL_PASSWORD = 'hixa igxg upbj dedk'
MAIL_DEFAULT_SENDER = 'auth.myshop.world@gmail.com'

# Gemini API Key
GOOGLE_API_KEY = "AIzaSyDIfoNBe4MbyUShcjV0kA3Pup0gxhuQ1uA"
genai.configure(api_key=GOOGLE_API_KEY)