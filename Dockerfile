FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . .

RUN chmod +x /app/entrypoint.sh

RUN poetry run python manage.py collectstatic --noinput

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]