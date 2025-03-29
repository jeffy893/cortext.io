FROM ubuntu:18.04
WORKDIR /home/ec2-user
COPY . .
# Upgrade installed packages
RUN apt-get update && apt-get upgrade -y && apt-get clean

# (...)

# Python package management and basic dependencies
RUN apt-get install -y vim curl python3.8 python3.8-dev python3.8-distutils

# Register the version in alternatives
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

# Set python 3 as the default python
RUN update-alternatives --set python3 /usr/bin/python3.8

# Upgrade pip to latest version
RUN curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py --force-reinstall && \
    rm get-pip.py

RUN python3 -m pip install -r requirements.txt
RUN apt-get install -y openjdk-11-jdk
