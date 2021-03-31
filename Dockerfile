FROM python:3.9.2-slim-buster
RUN apt update
RUN apt-get install -y git
#&& apt install openssh-server sudo -y
ARG CP_HOME=/var/www/catprez
ARG CP_THEME_HOME=/var/www/catprez-profcat
ARG DATA_DIR=/var/www/catprez-profcat/data

# CatPrez setup
WORKDIR /var/www
RUN mkdir /root/.ssh/
COPY bbpl-nopass.pem /root/.ssh/id_rsa
RUN chmod 700 /root/.ssh/id_rsa
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts
RUN git clone git@bitbucket.org:surroundbitbucket/catprez.git

WORKDIR /var/www/catprez
RUN pip install -r requirements.txt
RUN pip install gunicorn

# ProfCat setup
WORKDIR /var/www/catprez-profcat

RUN rm -r /var/www/catprez/catprez/data
COPY ./data /var/www/catprez/catprez/data
COPY ./model ./model
COPY ./plugins ./plugins
COPY ./style ./style
COPY ./templates ./templates
COPY ./apply.sh ./apply.sh
RUN ls /var/www/catprez/catprez/data
RUN chmod 700 apply.sh
RUN ./apply.sh

# Run
WORKDIR /var/www/catprez
CMD ["gunicorn", "-w", "5", "-b", "0.0.0.0:5000", "wsgi:application"]
EXPOSE 5000