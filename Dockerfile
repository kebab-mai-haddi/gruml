FROM ubuntu:latest

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

# RUN rm /usr/lib/python3.6/pyclbr.py
# RUN copy pyclbr.py us

RUN mkdir -p /home/ubuntu/generate_uml
COPY ./* /home/ubuntu/generate_uml/

# Install GRUML requirements
RUN apt-get update && apt-get install -y python3-pip git
RUN ls /home/ubuntu/generate_uml
WORKDIR /home/ubuntu/generate_uml
RUN ls
RUN pip3 install -r requirements.txt

# Change pyclbr
RUN rm /usr/lib/python3.8/pyclbr.py
COPY ./pyclbr /usr/lib/python3.8/pyclbr.py
# Keep running the container
CMD tail -f /dev/null