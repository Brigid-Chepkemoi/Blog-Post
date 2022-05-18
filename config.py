import os


class Config:
    SECRET_KEY='peeiicdjghsbnasgkkhjhjjhreirmd'
    QUOTE_API_BASE_URL='http://quotes.stormconsultancy.co.uk/random.json'
    SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://brie:brie1240@localhost:5433/blogpost'
    SQLALCHEMY_DATABASE_URI = 'postgres://umttmwmodaorna:58d3bbb2ae1e234218b5ead7e5b18ef4b0394cd6f6b93f0c8bae64f0429814a1@ec2-52-86-115-245.compute-1.amazonaws.com:5432/d7ohuleca980bt'
    UPLOADED_PHOTOS_DEST='app/static/photos'

    #  email configurations

    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT='587'
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD")
    SUBJECT_PREFIX='SASSY BLOG POST',
    SENDER_EMAIL='bchepkemoi2022@gmail.com'

    @staticmethod
    def init_app(app):
        pass


class ProdConfig(Config):
    """
    Production  configuration child class
    Args:
    Config: The parent configuration class with General configuration settings
    """
    uri = os.getenv('DATABASE_URL')
    if uri and uri.startswith('postgres://'):
        uri = uri.replace('postgres://', 'postgresql://', 1)

        SQLALCHEMY_DATABASE_URI=uri

    DEBUG = True



class TestConfig(Config):
    pass


class DevConfig(Config):
    """
    Development  configuration child class
    Args:
    Config: The parent configuration class with General configuration settings
    """


DEBUG=True

config_options={
    'development': DevConfig,
    'production': ProdConfig,
    'test': TestConfig
}
