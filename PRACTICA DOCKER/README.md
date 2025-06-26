docker build -t jeremy/practica:0.0.1.RELEASE .
docker container run -d -p 4000:4000 --name practica jeremy/practica:0.0.1.RELEASE