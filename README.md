# pipeline-automate-jenkins
## To Automate Create jenkinsfile And Create Job Use Library python-jenkins
Prepare DevSecops Pipeline That Analyze Your Code By SonarQube, Check Your Dependency That Your Library Use it; Before Push To Registry Check vulnerabilities Image By Trivy And Grype; Also Send Our Reports To Defectdojo, At the End We Automate DAST To Test 
![Screenshot 2024-10-21 132944](https://github.com/user-attachments/assets/db3f879c-eb2d-494c-9a46-5b57440ffb45)

## Table of Contents
- [Prerequisites](#Prerequisites)
- [Usage](#usage)
- [Features](#features)
- [Contact](#contact)
## Prerequisites
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
-  You Have DevSecops Pipeline That Automate DAST; analysis Tools Like Zap, Nessus
-  We Use SonarQube And Trivy, Grype To Scan Our Image And Code
-  Send Our Report To Defectdojo
-  If You Do Not Need To Have Any Of Theme  On The Values File Change That Part To False
