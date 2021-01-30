# Payment Service


## Installation

Up both DB and AMQP services by doing copy and paste respectively.

```bash
docker-compose up -d
```

```bash
docker exec -it payment_db /bin/bash
```

```bash
mongo
```

```bash
use payment
```

```bash
db.createCollection("payment") 
```

```bash
db.flights.insertMany([
                      {"customer_id":"PmCdvNtBSzU2WEgY","wallet":"OK"},
                      {"customer_id":"82yxmrNR2tcRwz78","wallet":"OK"}])
```


## payment db
27019/payment