import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED  = True
PASSWORD_SALT = os.environ.get('PASSWORD_SALT', 'xxxxxx')
SECRET_KEY    = os.environ.get('SECRET_KEY', 'you-will-never-guess')

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'app.db'))

