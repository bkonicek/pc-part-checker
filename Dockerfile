FROM python:3.7-alpine

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "readsheet.py"]