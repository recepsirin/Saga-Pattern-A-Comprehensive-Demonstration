# Flight Service

## Installation

Up both DB and AMQP services by executing below commands respectively.

```bash
docker-compose up -d
```

```bash
docker exec -it flight_db /bin/bash
```

```bash
mongo
```

```bash
use flights
```

```bash
db.createCollection("flights") 
```

```bash
db.flights.insertMany([
                      {"date":"31-12-2021","available": true},
                      {"date":"30-11-2021","available": false}])
```

### flight db

* 27018/flights