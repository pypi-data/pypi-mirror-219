import yaml


class MqttConfig:
    def __init__(self, file_path):
        self.load_config(file_path)
        self.validate_topic_subscriptions()

    def load_config(self, file_path):
        try:
            with open(file_path, 'r') as file:
                config_data = yaml.safe_load(file)

            mqtt_config = config_data.get('mqtt', {})

            self.enabled = mqtt_config.get('enabled', False)

            connection = mqtt_config.get('connection', {})
            self.broker_host = connection.get('broker_host', 'localhost')
            self.broker_port = connection.get('broker_port', 1883)
            self.client_id = connection.get('client_id', 'test')
            self.username = connection.get('username', 'robot')
            self.password = connection.get('password', 'robot')

            topics = mqtt_config.get('topics', {})
            self.topic_aliases = topics.get('aliases', [])
            self.topic_subscriptions = topics.get('subscribe', [])
        except Exception as e:
            raise ValueError(f'Error al cargar la configuración: {str(e)}')

    def get_topic_from_alias(self, alias):
        for entry in self.topic_aliases:
            if entry.startswith(f'{alias}:'):
                return entry.split(':', 1)[1]

        return None

    def validate_topic_subscriptions(self):
        for alias in self.topic_subscriptions:
            if alias not in [entry.split(':', 1)[0] for entry in self.topic_aliases]:
                raise ValueError(
                    f'Alias "{alias}" no encontrado en las colas (topics.aliases).')

    def printConfig(self):
        print('Enabled:', self.enabled)
        print('Broker Host:', self.broker_host)
        print('Broker Port:', self.broker_port)
        print('Client ID:', self.client_id)
        print('Username:', self.username)
        print('Password:', self.password)
        print('Topic Aliases:', self.topic_aliases)
        print('Topic Subscriptions:', self.topic_subscriptions)
