from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='../crm/templates')

def split_string(value, delimiter=" "):
    return str(value).split(delimiter)


def replace_string(value, delimiter="-"):
    return str(value).replace(delimiter, ".")


templates.env.filters["split"] = split_string
templates.env.filters["replace"] = replace_string

