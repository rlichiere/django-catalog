try:
    import config_private

    # Password used to initialize users.
    # Value is encrypted. To initialize this field, you musthave to copy it from dbFor example
    DEFAULT_USER_PASSWORD = config_private.DEFAULT_USER_PASSWORD

except Exception as e:
    print('private config not found. use default values')

    DEFAULT_USER_PASSWORD = 'pbkdf2_sha256$24000$...='

# Project status are used in the project's workflow.
PROJECT_STATUS = ['active', 'archive']
