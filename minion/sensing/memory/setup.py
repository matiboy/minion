import minion.core.components


defines = {
    minion.core.components.Types.SENSOR: [
        {
            'name': 'Redis memory',
            'class': 'minion.sensing.memory.redis.Memcheck',
            'description': '''
<h3>Reads current values from Redis using ZRANGE family of commands</h3>
<h4>Output: whatever was put into memory</h4>
<p>Values can be added to the corresponding key with a score using ZADD. The score is expected to be a unix timestamp.</p>
<p>Redis Memcheck will grab values between 0 and current unix timestamp and trigger the corresponding command. It then deletes the items in redis</p>
            ''',
            'setup': [{
                'type': 'input',
                'name': 'key',
                'default': 'alzheimer',
                'message': 'Key used in the redis key-value store'
            },
            {
                'type': 'input',
                'name': 'redis_host',
                'default': 'localhost',
                'message': 'Redis host'
            },
            {
                'type': 'input',
                'name': 'redis_port',
                'default': '6379',
                'message': 'Redis port'
            },
            {
                'type': 'input',
                'name': 'redis_db',
                'default': '0',
                'message': 'Redis db'
            }],
            'requirements': (
                'redis',
                'arrow'
            ),
        }
    ]
}
