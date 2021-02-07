FROM python:3.8-buster
ARG PROJECT_ID=projectid
ENV PROJECT_ID ${PROJECT_ID}
WORKDIR /root
COPY requirements.txt requirements.txt
RUN pip install -U pip && pip install -r requirements.txt
COPY main.py main.py
COPY tests tests
ENTRYPOINT [ "python", "main.py" ]
