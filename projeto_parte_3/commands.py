class Commands:
    HELP_CMD = "/help"
    LOGIN_CMD = "hi, meu nome eh "
    LOGOUT_CMD = "/bye"
    SHOW_LIST_CMD = "/list"
    SHOW_FRIEND_LIST_CMD = "/mylist"
    ADD_FRIEND_CMD = "/addtomylist "
    REMOVE_FRIEND_CMD = "/rmvfrommylist "
    BAN_CMD = "/ban "
    USER_ENTERED = " entrou na sala!"
    USER_ALREADY_EXISTS = "ja existe um usuario com este nome"
    USER_BANNED = "você foi banido!"
    ALL_CMDS = [SHOW_LIST_CMD, SHOW_FRIEND_LIST_CMD, ADD_FRIEND_CMD, REMOVE_FRIEND_CMD, BAN_CMD, LOGOUT_CMD]

class Ban:
    def __init__(self, banned_user, votes_needed, caller, votes_count=1) -> None:
        self.user = banned_user
        self.votes_count = votes_count
        self.votes_needed = votes_needed
        self.voters = [caller]