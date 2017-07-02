import yaml

# Create you own private.yml file, or modify parameters below :

# ######################################################## ALLOWED_HOSTS ###
# Used to allow connections on this IP (settings.py requirement)
ALLOWED_HOSTS = ['localhost']

# ########################################################### SECRET_KEY ###
# Secret key of django application (settings.py requirement)
SECRET_KEY = '21*7!=3^44afq...'

# ################################################ DEFAULT_USER_PASSWORD ###
# Used to initialize users password (applicative requirement)
# Value is encrypted. To initialize this field, you can copy one from db.
DEFAULT_USER_PASSWORD = 'pbkdf2_sha256$24000$...='

try:
    with open('private.yml') as private_config_file:
        private_config = yaml.load(private_config_file)
        if 'ALLOWED_HOSTS' in private_config:
            ALLOWED_HOSTS = private_config['ALLOWED_HOSTS']
        if 'SECRET_KEY' in private_config:
            SECRET_KEY = private_config['SECRET_KEY']
        if 'DEFAULT_USER_PASSWORD' in private_config:
            DEFAULT_USER_PASSWORD = private_config['DEFAULT_USER_PASSWORD']
except Exception as e:
    print('unable to load private config (%s). default values used.' % e)



# Project status are used in the project's workflow.
PROJECT_STATUS = ['active', 'archive']

# Activates DEBUG in settings
DEBUG = True
