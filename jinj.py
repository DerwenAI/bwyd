
import json
import pathlib

from icecream import ic
import jinja2

env = jinja2.Environment(loader = jinja2.FileSystemLoader("."))
template = env.get_template("jinj.jinja")

model_path: pathlib.Path = pathlib.Path("model.json")
data: dict = json.load(open(model_path, "r", encoding = "utf-8"))

output = template.render(module = data)

print(output)
