docker build -t jeremy_proyecto_grafos/proyecto_grafos:0.0.1.RELEASE .

docker container run -d -p 4000:4000 --name proyecto_grafos jeremy_proyecto_grafos/proyecto_grafos:0.0.1.RELEASE
