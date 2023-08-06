# Py Framework Robot

## Fichero de configuración


```yaml
mqtt:
    connection:
    broker_host: "localhost"
    broker_port: 1883
    client_id: "test"
    username: "robot" # Change to None if not required
    password: "robot" # Change to None if not required

    topics:
    aliases:
        - "topic:alias"
    subscribe:
        - alias1
``` 