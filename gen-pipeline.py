import jinja2
import yaml

# Load the values from the YAML file
with open('values.yaml') as f:
    values = yaml.safe_load(f)

# Load the Jinja2 template from the file
with open('main.jinja2') as f:
    template_content = f.read()

# Create a Jinja2 template object
template = jinja2.Template(template_content)

# Render the template with the values
output = template.render(values)

# Write the final output to a Jenkinsfile
with open('Jenkinsfile', 'w') as f:
    f.write(output)

print("Jenkinsfile generated successfully!")

