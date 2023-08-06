import os 

def get_env(key, default=""): 
    val = os.getenv(key)
    return val if val else default

class Config:
    def __init__(self):
        self.config = {}

    def __call__(self, key):
        return self.get_env(key)
    
    def load_yaml(self, file):
        import yaml
        with open(file, 'r') as conf_file:
            self.config = yaml.safe_load(conf_file)

    def load_json(self, file):
        import json
        with open(file, 'r') as conf_file:
            self.config = json.load(conf_file)

    def set(self, key, value):
        '''set config'''
        keys = key.split(".")
        config_value = self.config
        for k in keys:
            config_value = config_value[k]
        config_value = value

    def merge(self, config):
        '''merge config'''
        self.config.update(config)
        return self.config

    def get(self, key):
        '''
        Args：
            key - 配置key，支持级联：app.name
        Return:
            config['app']['name'] else None
        '''
        print(key)
        keys = key.split(".")
        config_value = self.config
        for k in keys:
            config_value = config_value.get(k)
        return config_value

    def get_env(self, key):
        """ 
        Args：
            key - 配置key，支持级联：app.name
        Return:
            app.name 先取 APP_NAME 环境变量，再取config['app']['name'] 
        """
        keys = key.split(".")
        env_key = "_".join([i.upper() for i in keys])
        config_value = get_env(env_key)
        if not config_value:
            return self.get(key)
        return config_value

