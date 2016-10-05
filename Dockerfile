FROM docker.io/ubuntu:14.04
MAINTAINER praveen.gunasekar@aol.com
RUN apt-get update
RUN apt-get install -y apache2
RUN mkdir -p /var/www/html/test.com
COPY test.conf /etc/apache2/sites-available/
COPY index.html /var/www/html/test.com/
EXPOSE 80
ENTRYPOINT ["apache2ctl"]
CMD ["-D","FOREGROUND"]

