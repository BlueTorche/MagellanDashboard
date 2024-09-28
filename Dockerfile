FROM debian:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libpq-dev

RUN mkdir /srv/magellan-logs

WORKDIR /srv/magellan-logs

COPY models models
COPY static static
COPY templates templates
COPY requirements.txt requirements.txt
COPY app.py app.py

RUN pip3 install -r requirements.txt --break-system-packages

EXPOSE 80 443

#create lowpriv user to run the app with low privileges
RUN useradd -ms /bin/bash lowpriv
RUN chown -R lowpriv:lowpriv /srv/magellan-logs
#RUN chown -R lowpriv:lowpriv /etc/ssl/magellan-logs

USER lowpriv

CMD ["gunicorn","-b","0.0.0.0:80","-w","3","app:create_app()"]