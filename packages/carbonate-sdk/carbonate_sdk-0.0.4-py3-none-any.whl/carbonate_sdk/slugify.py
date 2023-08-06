import re

def slugify(value):
    file = re.sub(r"([^\w\s\d\-_~,;\[\]\(\).])", '', value)
    file = re.sub(r"([\.]{2,})", '', file)

    return file