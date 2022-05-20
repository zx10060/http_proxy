FROM python:slim

COPY . /http_proxy
WORKDIR /http_proxy
RUN pip install -r requirements.txt
RUN pip install --upgrade pip
EXPOSE 8000
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]

