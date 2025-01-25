import streamlit as st
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker

# Database connection details
DB_SERVER = 'SHREYASONKUSARE\\SQLEXPRESS'
DB_DATABASE = 'test'
DB_USER = 'sa'
DB_PASSWORD = 'admin123'

# Cached database engine
@st.cache_resource
def get_engine():
    connection_string = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"
    return create_engine(connection_string)

engine = get_engine()

# Table metadata
metadata = MetaData()
users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(50), nullable=False),
    Column('age', Integer, nullable=False),
    Column('salary', Integer, nullable=False),
)

# Create table if not exists
if not engine.dialect.has_table(engine, "users"):
    metadata.create_all(engine)

# Insert user into database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def insert_user(name, age, salary):
    session = SessionLocal()
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

# Streamlit app
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
