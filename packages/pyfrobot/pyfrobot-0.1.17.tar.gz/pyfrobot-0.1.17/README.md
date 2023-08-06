# Py Framework Robot

## Fichero de configuración


```yaml
mqtt:
  enabled: true
  # Parametros de conexión a mqtt
  connection:
    broker_host: "localhost"
    broker_port: 1883
    client_id: "test"
    username: "robot" # Change to None if not required
    password: "robot" # Change to None if not required

  # Alias de los topics y subscripciones
  topics:
    aliases:
        - "topic:alias"
    subscribe:
        - alias1
``` 