import configparser

def create_config(config_path, default_values):
    # 创建ConfigParser对象
    config = configparser.ConfigParser()

    # 添加默认配置项
    for section, options in default_values.items():
        config.add_section(section)
        for option, value in options.items():
            config.set(section, option, str(value))

    # 将配置写入文件
    with open(config_path, 'w') as configfile:
        config.write(configfile)

# 示例默认配置值
default_config = {
    'Server': {
        'host': 'localhost',
        'port': '8080',
    },
    'Database': {
        'username': 'admin',
        'password': 'secret',
        'database_name': 'mydb',
    }
}

# 调用函数创建配置文件
create_config('config.ini', default_config)