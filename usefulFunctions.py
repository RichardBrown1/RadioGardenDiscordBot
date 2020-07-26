def dubApos(string):
    if isinstance(string, str):
        return string.replace("'", "''")
    else:
        return "NULL"
