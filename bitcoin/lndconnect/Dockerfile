FROM golang:latest

RUN apt update && apt install -y --no-install-recommends \
    git \
    vim \
    && apt clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# RUN go install github.com/LN-Zap/lndconnect@latest
# RUN $GOPATH/src/github.com/LN-Zap/lndconnect/make
WORKDIR /root

RUN git clone https://github.com/LN-Zap/lndconnect lndconnect 

COPY .bash_shell_helpers /root/.bashrc

COPY lndconnect/build /root/build
RUN /root/build

ENTRYPOINT ["lndconnect"]