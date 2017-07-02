try:
    import config_private
    DEFAULT_USER_PASSWORD = config_private.DEFAULT_USER_PASSWORD
except Exception as e:
    print('private config not found. use default values')

    # Create you own config_private file, or modify parameters below :

    # ################################################ DEFAULT_USER_PASSWORD ###
    # Used to initialize users password.
    # Value is encrypted. To initialize this field, you can copy one from db.
    DEFAULT_USER_PASSWORD = 'pbkdf2_sha256$24000$...='

# Project status are used in the project's workflow.
PROJECT_STATUS = ['active', 'archive']
