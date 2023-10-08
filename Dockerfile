FROM ubuntu:latest
LABEL authors="Ruslan"

ENTRYPOINT ["top", "-b"]