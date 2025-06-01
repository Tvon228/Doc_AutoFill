# Базовый образ
FROM python:3.12-alpine

# Рабочая папка
WORKDIR /backend

# Установка зависимостей
COPY pyproject.toml uv.lock .python-version ./
RUN pip install uv && uv sync --no-dev

# Копируем остальные файлы
COPY . .

# Запуск
RUN chmod +x run.sh
ENTRYPOINT ["./run.sh"]