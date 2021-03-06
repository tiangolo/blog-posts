FROM python:3.8

RUN pip install streamlit

COPY ./app /app/

CMD [ "streamlit", "run", "app/lit.py", "--server.port", "80" ]
