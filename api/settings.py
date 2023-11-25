import os

JWT_SECRET = os.getenv('JWT_SECRET', 'SECRET')
DB_FILE = os.getenv('DB_FILE', './database')
OPA_URL = os.getenv('OPA_URL', 'http://localhost:8181')

