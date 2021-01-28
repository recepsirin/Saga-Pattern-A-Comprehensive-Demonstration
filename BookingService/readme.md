# Booking Service


## Installation

##### Installation consists of two steps.


First One
```bash
docker-compose up -d
```

Wait 50 seconds for downloading container's images, then

Second Step
```bash
docker-compose -f docker-compose-sec.yml up -d
```

### to reach out the saga transactions logs
7755/saga.log

### booking endpoint
4000/booking [POST]

### booking db
27017/booking