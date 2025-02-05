FROM zauberzeug/nicegui:1.3.13

WORKDIR /app

COPY app /app

RUN pip install --no-cache-dir -r app/requirements.txt

CMD ["python", "/app/main.py"]