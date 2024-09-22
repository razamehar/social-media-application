FROM python:3.9.7

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Add pip install directory to PATH
ENV PATH="/usr/local/bin:$PATH"

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
