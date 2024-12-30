# backend_fast_api

pip install -r requirements.txt
pip freeze > requirements.txt

python src/main.py

alembic revision --autogenerate -m "init"
alembic downgrade -1
