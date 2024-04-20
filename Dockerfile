FROM python:3.12.3

SHELL ["/bin/bash", "-c"]


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN pip install --upgrade pip

RUN useradd -rms /bin/bash x_one_test_user

WORKDIR /x_one_test

RUN mkdir /x_one_test/static && chown -R x_one_test_user:x_one_test_user /x_one_test && chmod 755 /x_one_test

COPY . .

RUN pip install -r requirements.txt

CMD ["gunicorn","-b","0.0.0.0:8000","core.wsgi:application"]