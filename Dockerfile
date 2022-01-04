FROM openjdk:17
COPY . /mc
WORKDIR /mc/data
VOLUME /mc/data
EXPOSE 25565
ENTRYPOINT [ "sh","../system/bin/start.sh" ]

