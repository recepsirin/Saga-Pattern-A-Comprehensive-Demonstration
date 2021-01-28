## RabbitMQ Cluster Installation


## General info
This cluster consists of 3 rabbitmq-nodes and haproxy node. This cluster will be used by payment, booking, sec and flight services.
	
## Technologies
Project is created with:
* Rabbitmq
* Rabbitmq-management
* Haproxy

## Setup
To run this project:

run all docker containers with the command below
```
docker-compose up -d
```

then enable management plugins for node 1
```
docker exec rabbitmq-node1 rabbitmq-plugins enable rabbitmq_management
```

also, for node 2
```
docker exec rabbitmq-node2 rabbitmq-plugins enable rabbitmq_management
```

lastly, for node 3
```
docker exec rabbitmq-node3 rabbitmq-plugins enable rabbitmq_management
```


## Haproxy 
* ID: admin
* PWD: admin



## RabbitMq Management Ui 
* ID: guest
* PWD: guest

##### References

* [I had just taken this cluster from here](https://github.com/pardahlman/docker-rabbitmq-cluster)