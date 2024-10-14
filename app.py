import jenkins
import jinja2
import yaml
#--------- Initialize Pipeline ----------------
with open('values.yaml') as f:
    values = yaml.safe_load(f)
with open('main.jinja2') as f:
    template_content = f.read()
template = jinja2.Template(template_content)
output = template.render(values)
with open('Jenkinsfile', 'w') as f:
    f.write(output)
print("Jenkinsfile generated successfully!")


#----------------- Variable -------------------
job_name = "automate-pipeline-trigger"

with open('Jenkinsfile', 'r') as file:
    pipeline_script =file.read()

job_config = f'''<?xml version='1.0' encoding='UTF-8'?>
<flow-definition plugin="workflow-job@2.40">
  <actions/>
  <description>Automated Pipeline Job</description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@2.88">
    <script>{pipeline_script}</script>
    <sandbox>true</sandbox>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>
'''
#----------------- Code -----------------------
server = jenkins.Jenkins('http://192.168.42.3:8080', username='milad', password='11512de8485bb0e4b3c37b1c0d329c9cb9')

#jobs = server.get_all_jobs()
#print(jobs)

try:
    server.create_job(job_name, job_config)
    print(f"Job {job_name} Succefully Created.")
except jenkins.JenkinsException as e:
    print(f"Field: {e}")