import jinja2
import yaml

with open('values.yaml') as f:
    values = yaml.safe_load(f)
with open('main.jinja2') as f:
    template_content = f.read()


template = jinja2.Template(template_content)
output = template.render(values)


with open('Jenkinsfile', 'w') as f:
    f.write(output)

print("Jenkinsfile generated successfully!")
