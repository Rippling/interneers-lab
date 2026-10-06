# domain : core logic

def greeting(name):
    if name == None:
        name = ""
    name = name.strip()
    if (name == ""):
        return "Hello, World!"
    else:
        return "Hello, "+name+"!"
