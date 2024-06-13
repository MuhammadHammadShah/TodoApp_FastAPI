from fastapi import FastAPI
from todoapp_fastapi import settings
from sqlmodel import SQLModel , Field, Session , create_engine
from contextlib import asynccontextmanager

class Todo(SQLModel , table=True):
    id: int | None = Field(default=None , primary_key=True)
    title: str

connection_str:str = str(settings.DATABASE_URL).replace("postgresql" , "postgresql+psycopg")
engine = create_engine(connection_str)


def create_db_table():
    print("creaing db table")
    SQLModel.metadata.create_all(engine)
    print("Done creating.")

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Server StartUp")
    create_db_table()
    yield

app : FastAPI = FastAPI(lifespan=lifespan)

# STEP:1 DataBase Table schema




# Connection to the Databse
# Table data save , update , delete
@app.get("/")
def read_root():
    create_db_table()
    return {
        "Ho to the" : "World"
    }

#@app.get("/city") #get parameteer should be equal to function 
#def city():       #def name
#    return {
#        "City_name" : "Karachi"
#    }

@app.get("/db")
def db():
    return {
        "DB" : settings.DATABASE_URL ,
        "Connection" : connection_str
        
    }
@app.post("/todo")
def create_todo(todo_data:Todo):
    with Session(engine) as session:
        session.add(todo_data)
        session.commit()
        session.refresh(todo_data)
        return todo_data
