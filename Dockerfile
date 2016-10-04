FROM cent/base:latest
MAINTAINER praveen.gunasekar@aol.com
RUN yum update -y && yum install httpd -y
EXPOSE 80
ENTRYPOINT ["/usr/sbin/httpd"] 
CMD ["-D", "FOREGROUND"]

