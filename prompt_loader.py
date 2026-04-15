import yaml
from jinja2 import Template

def load_prompt(template_name: str, **variables) -> dict:
    with open(f"prompts/{template_name}.yaml") as file:
        raw_yaml = yaml.safe_load(file)

    return {
        "system": Template(raw_yaml['system']).render(**variables),
        "user": Template(raw_yaml['user']).render(**variables),
    }