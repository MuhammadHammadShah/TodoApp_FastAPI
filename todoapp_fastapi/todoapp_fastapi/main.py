from fastapi import FastAPI
from todoapp_fastapi import settings
from sqlmodel import SQLModel , Field, Session , create_engine, select
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
        "Connection" : connection_str,
    }
@app.post("/todo")
def create_todo(try_content:Todo):
    with Session(engine) as session:
        #session = Session(engine)
        session.add(try_content)
        session.commit()
        session.refresh(try_content)
        #session.close()
        return try_content

#dependency injection

#get all Todos Data
@app.get("/todos")
def get_all_todos():
    with Session(engine) as session:
    #session = Session(engine)
    # Todos Select
      query = select(Todo)
      all_todos = session.exec(query).all()
      return all_todos