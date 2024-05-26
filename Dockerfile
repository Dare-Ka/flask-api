FROM python:3.11-alpine
RUN apk add --no-cache gcc musl-dev linux-headers

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 5000

CMD python models.py \
    && gunicorn app:app -b 0.0.0.0:5000 --capture-output