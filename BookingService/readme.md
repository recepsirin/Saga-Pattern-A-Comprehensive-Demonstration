# Booking Service


## Installation


Up api, db and nginx containers with the command below
```bash
docker-compose up -d
```

Then, up saga execution coordinator and logging service with the command below
```bash
docker-compose -f docker-compose-sec.yml up -d
```

### Reaching out to the saga transactions logs
* localhost:7755/saga.log

### booking endpoint
* 4000/booking [POST]

### booking db
* 27017/booking