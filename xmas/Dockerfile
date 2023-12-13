FROM python:3.6-slim
COPY requirements.txt /
RUN pip3 install -r /requirements.txt
COPY xmas.py /app
WORKDIR /app
CMD ["python", "xmas.py"]
