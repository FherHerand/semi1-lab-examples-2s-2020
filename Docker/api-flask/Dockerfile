FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT 5000
ENV IP "127.0.0.1"

CMD ["python", "app.py"]