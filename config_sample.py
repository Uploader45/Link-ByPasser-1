class Config(object):

    AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "1300445326").split())
    BANNED_USERS = set(int(x) for x in os.environ.get("BANNED_USERS", "").split())
    LOG_CHAN = int(os.environ.get("LOG_CHAN", "-1001145342921"))
    UPDATE_CHANNEL = "DevilBotz"
    USERNAME = os.environ.get("USERNAME", "Stay007") 
    ADL_BOT_RQ = {}