FROM zauberzeug/nicegui:1.3.13

RUN pip install --no-cache-dir quotes

COPY . /app