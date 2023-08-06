FROM continuumio/miniconda3
# FROM --platform=linux/amd64 continuumio/miniconda3

MAINTAINER Brando Miranda "brandojazz@gmail.com"

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    ssh \
    git \
    m4 \
    libgmp-dev \
    opam \
    wget \
    ca-certificates \
    rsync \
    strace \
    gcc \
    rlwrap \
    sudo

RUN useradd -m bot
# format for chpasswd user_name:password
RUN echo "bot:bot" | chpasswd
RUN adduser bot sudo

WORKDIR /home/bot
USER bot

# makes sure depedencies for pycoq are installed once already in the docker image
ENV WANDB_API_KEY="SECRET"
RUN pip install wandb --upgrade

RUN pip install ultimate-utils

# then make sure editable mode is done to be able to use changing pycoq from system
RUN echo "pip install -e /home/bot/ultimate-utils" >> ~/.bashrc
RUN echo "pip install wandb --upgrade" >> ~/.bashrc
RUN echo "eval $(opam env)" >> ~/.bashrc
# - set env variable for bash terminal prompt p1 to be nicely colored
ENV force_color_prompt=yes

RUN mkdir -p /home/bot/data/

##RUN pytest --pyargs pycoq
##CMD /bin/bash