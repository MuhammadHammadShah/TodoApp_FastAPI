install pipx

pip install pipx


install poetry 

pipx install poetry


create poetry project

poetry new todoapp_fastapi


install fastapi

poetry add fastapi


install uvicorn

poetry add uvicorn


If an error comes of used port use this command

`poetry run uvicorn todoapp_fastapi.main:app --host 127.0.0.1 --port 8002 --reload`

instead of

`poetry run uvicorn todoapp_fastapi.main:app --reload`