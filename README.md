# backend_fast_api

https://github.com/Kinzina/backend_fast_api/commit/42fb279e129318ecfc99d99363c797c46df4ee1a = task_04
https://github.com/Kinzina/backend_fast_api/commit/... = task_04

pip install -r requirements.txt
pip freeze > requirements.txt

python src/main.py

alembic revision --autogenerate -m "init"
alembic downgrade -1
