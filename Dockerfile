FROM python:3.12-alpine
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install
COPY . .
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]