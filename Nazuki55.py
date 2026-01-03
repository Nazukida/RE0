def check_password(string_arg):
    if len(string_arg) > 8:
        return False
    if len(string_arg) < 4:
        return False
    thislist = [0, 0, 0, 0]#lower,upper,digit,special
    for char in string_arg:
        if 'a' <= char <= 'z':
            thislist[0] = 1
        elif 'A' <= char <= 'Z':
            thislist[1] = 1
        elif 0<= char <= 9:
            thislist[2] = 1
        else:
            thislist[3] = 1
    if sum(thislist) == 4:
        return True
    else:
        return False