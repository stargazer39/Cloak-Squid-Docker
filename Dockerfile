FROM alpine:latest
RUN apk add --no-cache  git make go squid python3
WORKDIR /home
RUN git clone https://github.com/cbeuw/Cloak.git
WORKDIR /home/Cloak
RUN go get ./...
RUN make && make install
WORKDIR /home
RUN rm -rf Cloak
RUN apk del make go git 
COPY ckserver_template.json /home
RUN mkdir /config
COPY start.py /home
ENTRYPOINT ["python3", "/home/start.py"]
RUN echo "Build success I guess?"