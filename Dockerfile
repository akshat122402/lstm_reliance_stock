FROM python:3.9

WORKDIR /lstm

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["python", "run_app.py"]
