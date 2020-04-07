# configuration source: https://hub.docker.com/r/theeluwin/ubuntu-konlpy/dockerfile
# basing on ubuntu OS
FROM ubuntu:latest
LABEL maintainer="Ahn Young Jin <snoop2head@gmail.com>"

# apt init
ENV LANG=C.UTF-8
ENV TZ=Asia/Seoul
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata g++ git curl

# installing java jdk and java jre
RUN apt-get install -y default-jdk default-jre

# packages for language translation
RUN apt-get install -y gettext

# installing python3 and pip3
RUN apt-get install -y python3-pip python3-dev
RUN apt-get install -y python-psycopg2

RUN cd /usr/local/bin && \
    ln -s /usr/bin/python3 python && \
    ln -s /usr/bin/pip3 pip && \
    pip3 install --upgrade pip

# apt cleanse
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# timezone
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# workspace
RUN mkdir -p /workspace
WORKDIR /workspace

# install konlpy dependencies: jpype, konlpy, konlpy mecab
RUN pip install jpype1-py3 konlpy
RUN cd /workspace && \
    curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh | bash -s

# getting environment variable on console
# different environment variables according to projects are on AWS Console
ENV PYTHONNUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV WSGIPath config/wsgi.py
ENV DJANGO_SETTINGS_MODULE config.settings
ENV DEBUG False

# copying local file into container's /code/ directory
COPY ./requirements.txt /code/requirements.txt
RUN apt-get install -y python3-pip
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

# apt cleanse
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# copying the rest of the files into container's /code/ directory
# container's working directory is /code/
COPY . /code/
WORKDIR /code/

#Exposing port to 5000, which is port for aws nginx
EXPOSE 5000

# CMD multiple commands using start.sh file
ADD start.sh /
RUN chmod +x /start.sh

CMD ["/start.sh"]