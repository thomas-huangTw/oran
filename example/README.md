# Running xApp example in Docker
***
```
#Build an image from a Dockerfile
docker build -t ping:latest -f  Dockerfile-Ping . 
docker build -t pong:latest -f  Dockerfile-Pong .

#Run a command in a new container
docker run -i --net=host ping:latest
docker run -i --net=host pong:latest
```
