FROM ubuntu:latest
# Install OpenSSH server
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    openssh-server python3 python3-flask python3-flask-login vim nginx dnsmasq \
    make docker docker.io \
    && rm -rf /var/lib/apt/lists/

# Configure SSH server
RUN mkdir /var/run/sshd
#RUN useradd -ms /bin/bash newuser
#RUN echo "newuser:0xC0ff33" | chpasswd
#change yes to no to allow root login
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
#host the ssh server on port 15010
RUN echo "port 15010" >> /etc/ssh/sshd_config
RUN echo "root:0xC0ff33" | chpasswd
 
    

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
#copy nginx stuff
COPY nginx-default.txt /etc/nginx/sites-available/default 
RUN echo "address=/cat.blog.com/127.0.0.1\
address=/evil.blog.com/127.0.0.1\
address=/interm.blog.com/127.0.0.1" > /etc/dnsmasq.conf

RUN echo "127.0.0.1	evil.blog.com \
        127.0.0.1	cat.blog.com \
        127.0.0.1	interm.blog.com \
        127.0.0.1	localhost" > /etc/hosts 

# Expose the port the app runs on
EXPOSE 8000
EXPOSE 8001
EXPOSE 8002

# Start the app
CMD ["sh", "fullBuild.sh"]
