uv run python src/manage.py collectstatic --noinput
cd src && uv run daphne config.asgi:application -b 127.0.0.1 -p 4123
