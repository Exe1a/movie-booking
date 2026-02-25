with open(".env", 'w') as file:
    file.write('\
POSTGRESQL_URL = "postgresql+psycopg://postgres:password@localhost:5432/postgres"\n\
SECRET_JWT_KEY = "SUPER_SECRET_JWT_KEY"\n\
DATABASE_RESET_KEY = "database_key"\n\
REDIS_HOST = "localhost"\n\
REDIS_PORT = "6479"\n\
')
print(f"File {file.name} was created")