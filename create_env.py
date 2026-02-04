with open(".env", 'w') as file:
    file.write('DATABASE_URL = "postgresql+psycopg://postgres:password@localhost:5432/postgres"\n')
    file.write('SECRET_JWT_KEY = "SUPER_SECRET_JWT_KEY"\n')
    file.write('DATABASE_RESET_KEY = "database_key"\n')
print(f"File {file.name} was created")