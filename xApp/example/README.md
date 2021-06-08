# Example introduce
Two xApp frameworks are provided in the examples directory. Among them general xApp acts according to its own criteria, which may include receipt of RMR messages.
In addition, reactive xApp acts on messages that are delivered (pushed) via RMR. The xApp only takes action upon receipt of an RMR message. The xApp never takes action at another time.

To run a counter example, build the Docker images for both examples using the supplied Dockerfiles. Then start the Pong container (the listener) followed by the Ping container (the sender). 

# Running xApp example in Docker
***
```
#Build an image from a Dockerfile
docker build -t ping:latest -f  Dockerfile-pingxApp . 
docker build -t pong:latest -f  Dockerfile-pongxApp .

#Run a command in a new container
docker run -i --net=host ping:latest
docker run -i --net=host pong:latest
```
### Reference
* https://github.com/o-ran-sc/ric-plt-xapp-frame-py
