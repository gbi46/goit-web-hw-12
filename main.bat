docker login
docker-compose up -d
docker run --name postgres_container3 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=567234 -e POSTGRES_DB=contacts_db -p 5432:5432 -d postgres
alembic init migrations
move env.py migrations
alembic revision --autogenerate -m 'Init'
alembic upgrade head
uvicorn main:app --reload