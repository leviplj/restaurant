FROM ubuntu:latest as builder

RUN apt update && apt upgrade -y \
   && apt install python3-venv -y \
   && update-alternatives --install /usr/bin/python python /usr/bin/python3 1

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN mkdir /code
COPY requirements.txt /code/
WORKDIR /code

RUN pip install -r requirements.txt

FROM builder as runner

COPY . /code/

EXPOSE 8000

ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
