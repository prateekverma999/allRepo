FROM python:latest
WORKDIR /app
COPY . .
RUN python hello.py
CMD [ "python","hello.py" ]