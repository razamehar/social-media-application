FROM python:3.9.7

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8051

ENTRYPOINT ["streamlit","run"]

CMD ["streamlit_app.py"]
