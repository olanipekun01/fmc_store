def validate(amnt):
    if amnt != "" and int(amnt) > 0:
        return True
    else:
        return False