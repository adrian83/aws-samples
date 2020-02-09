FROM golang:1.13.7-buster


RUN git clone https://github.com/adrian83/aws-samples.git



WORKDIR aws-samples/echo-service

RUN ls -al

RUN go build

CMD ["echo"]



