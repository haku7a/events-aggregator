set -e

alembic upgrade head

exec python app/main.py
