FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
         wget \
         bash

RUN mkdir opt/custom-conda
RUN cd opt/custom-conda

RUN wget --no-check-certificate https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /opt/custom-conda/miniconda.sh && \
    chmod +x /opt/custom-conda/miniconda.sh && \
    /opt/custom-conda/miniconda.sh -b -p /opt/custom-conda/miniconda && \
    rm /opt/custom-conda/miniconda.sh

ENV PATH=$PATH:/opt/custom-conda/miniconda/bin

COPY requirements.txt /opt
RUN conda create --name state-of-indices-env
RUN conda init bash && \
    . /root/.bashrc && \
    conda activate state-of-indices-env && \
    pip install -r /opt/requirements.txt

COPY . /opt/program/
ENTRYPOINT ["/usr/bin/bash", "/opt/program/run.sh"]
