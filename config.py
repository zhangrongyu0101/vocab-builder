class Config:
    # 通用配置
    SECRET_KEY = 'your_secret_key'
    DEBUG = False
    MONGO_URI = "mongodb://localhost:27017/vocab_builder"

class DevelopmentConfig(Config):
    # 开发环境特有配置
    DEBUG = True
    PROXIES = {
        "http": "http://127.0.0.1:4780",
        "https": "https://127.0.0.1:4780",
    }

class ProductionConfig(Config):
    # 生产环境特有配置
    DEBUG = False
    PROXIES = {
        # 生产环境可能不需要代理或使用不同的代理
    }

# 可以根据需要将config设置为对应环境的配置类
config = DevelopmentConfig
# 或者在生产环境中使用
# config = ProductionConfig
