# backend_fast_api

print(query.compile(engine, compile_kwargs={"literal_binds": True}))

https://github.com/Kinzina/backend_fast_api/commit/42fb279e129318ecfc99d99363c797c46df4ee1a = task_04
https://github.com/Kinzina/backend_fast_api/commit/b29eb9b4997022800bb3bcca6377042e6a4f681e = task_05
https://github.com/Kinzina/backend_fast_api/commit/2dd67748bbb094b73af9f0d96e5449f03dc1ece4 = task_06
https://github.com/Kinzina/backend_fast_api/commit/70212f5378f9f3494ff29c6faeb0301073294655 = task_07

pip install -r requirements.txt
pip freeze > requirements.txt

python src/main.py

alembic revision --autogenerate -m "init"
alembic downgrade -1
