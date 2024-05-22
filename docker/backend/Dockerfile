FROM python:3.10-alpine

RUN pip install --upgrade pip

WORKDIR /app
COPY ./ ./

COPY ./requirements.txt /.
RUN pip install -r requirements.txt

RUN ["chmod", "+x", "./backend/entrypoint.sh"]
ENTRYPOINT ["./docker/admin/entrypoint.sh"]