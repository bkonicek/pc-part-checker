FROM python:3.7-alpine

ENV PYTHONUNBUFFERED=1

RUN addgroup -S worker && \
    adduser -S worker -G worker

WORKDIR /code

RUN chown -R worker:worker /code

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER worker

CMD ["python", "readsheet.py"]