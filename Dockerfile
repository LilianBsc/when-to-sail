FROM python:3.11-slim
LABEL maintainer="https://github.com/LilianBsc"

WORKDIR /app
VOLUME . /app

RUN apt update

RUN pip3 install -r requirement.txt

EXPOSE 4000

CMD ["streamlit", "run", "0-⛵_Home.py"]
