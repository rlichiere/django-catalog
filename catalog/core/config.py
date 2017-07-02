try:
    import config_private
    ALLOWED_HOSTS = config_private.ALLOWED_HOSTS
    SECRET_KEY = config_private.SECRET_KEY
    DEFAULT_USER_PASSWORD = config_private.DEFAULT_USER_PASSWORD
except Exception as e:
    print('private config not found. use default values')

    # Create you own config_private file, or modify parameters below :

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


# Project status are used in the project's workflow.
PROJECT_STATUS = ['active', 'archive']

# Activates DEBUG in settings
DEBUG = True
