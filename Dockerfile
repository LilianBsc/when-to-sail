FROM debian:bullseye
LABEL maintainer="https://github.com/LilianBsc"

WORKDIR /app
VOLUME . /app

RUN apt update
RUN apt-get install -y python3.12

RUN pip install --upgrade pip
RUN pip install -r requirement.txt

EXPOSE 4000

CMD ["streamlit", "run", "app.py"]
