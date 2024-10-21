# pipeline-automate-jenkins
## To Automate Create jenkinsfile And Create Job Use Library python-jenkins
## Table of Contents
- [Requirements](#requirements)
- [Usage](#usage)
- [Features](#features)
- [Contact](#contact)
## Requirements
1. install library:
    ```bash
    pip install python-jenkins
    ```
## Usage
1. Import Your Jenkins-server On app.py
    ```bash
    server = jenkins.Jenkins('<YOUR-URL>', username='<YOUR-USERNAME>', password='<YOUR-PASSWORD>')
    ```
2. Import Your Values in values.yaml

## Features
-  You Have DevSecops Pipeline That Automate DAST Anaylsis Like Zap, Nessus
-  We Use SonarQube And Trivy, Grype To Scan Our Image And Code
-  Send Our Report To Defectdojo 
