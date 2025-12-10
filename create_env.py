with open(".env", 'w') as file:
    file.write('DATABASE_URL = "postgresql+psycopg://postgres:password@localhost:5432/postgres"')
print(f"File {file.name} was created") 