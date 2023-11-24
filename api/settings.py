import os

JWT_SECRET = os.getenv('JWT_SECRET', 'SECRET')
DB_FILE = os.getenv('DB_FILE', './database')

