FROM python:3.8.0-buster

WORKDIR /app

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \ 
    apt-get update && \  
    ACCEPT_EULA=Y apt-get install msodbcsql17 -y && \
    apt-get install -y unixodbc-dev

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY main.py /app

CMD ["python", "main.py"]
