import streamlit as st
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker

# Define database connection details
DB_SERVER = 'SHREYASONKUSARE\\SQLEXPRESS'   # Replace with your SQL Server name
DB_DATABASE = 'test'   # Replace with your database name
DB_USER = 'sa'   # Replace with your username
DB_PASSWORD = 'admin123'   # Replace with your password

# Create a database engine
connection_string = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(connection_string)

# Create table metadata
metadata = MetaData()
users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(50), nullable=False),
    Column('age', Integer, nullable=False),
    Column('salary', Integer, nullable=False),
)

# Create table if not exists
metadata.create_all(engine)

# Function to insert data into the database
def insert_user(name, age, salary):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        insert_query = users_table.insert().values(name=name, age=age, salary=salary)
        session.execute(insert_query)
        session.commit()
        return "User added successfully!"
    except Exception as e:
        session.rollback()
        return f"An error occurred: {e}"
    finally:
        session.close()

# Streamlit App
st.title("User Input Form")

name = st.text_input("Enter your name")
age = st.number_input("Enter your age", min_value=1, max_value=120)
salary = st.number_input("Enter your salary", min_value=0)

if st.button("Submit"):
    if name and age and salary:
        result = insert_user(name, age, salary)
        st.success(result)
    else:
        st.error("Please fill out all fields!")
