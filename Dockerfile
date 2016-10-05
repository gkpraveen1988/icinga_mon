<<<<<<< HEAD
FROM ubuntu:latest
MAINTAINER praveen.gunasekar@aol.com
RUN apt-get update
RUN apt-get install -y apache2
EXPOSE 80
ENTRYPOINT ["apache2ctl"]
CMD ["-D","FOREGROUND"]
=======
FROM cent/base:latest
MAINTAINER praveen.gunasekar@aol.com
RUN yum update -y && yum install httpd -y
EXPOSE 80
ENTRYPOINT ["/usr/sbin/httpd"] 
CMD ["-D", "FOREGROUND"]
>>>>>>> c526364079b086be0ad2d96453609cde5ecae4ea

