import re

def password_verification(input_string):
    regex="^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{6,15}$"
    reg=re.compile(regex)
    out=re.search(reg,input_string)
    if(out):
        return(True)
    return(False)

def username_verification(input_string):
    regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$'
    reg=re.compile(regex)
    out=re.search(reg,input_string)
    if(out):
        return(True)
    return(False)

