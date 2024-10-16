pipeline {
    agent any
    environment {
      REGISTERY ='192.168.1.104:5000'
      IMAGE = "${env.JOB_NAME}"
      PRODUCT_ID = '2'
      DOJO_URL = '192.168.1.104:8080'
      ENGAGEMENT_ID = '2'
      PRODUCT_NAME = 'Python'
    }

    
    stages {
        stage('checkout') {
            steps {
              git branch: 'main', credentialsId: '26e885c2-5e8a-44c9-8eff-95fb21ad957b', url: 'https://192.168.1.104:3000/hasan/python.git'
                }
            }
        stage('Get Short SHA'){
          steps {
            script {
              env.CI_COMMIT_SHORT_SHA=sh(
                script:'git rev-parse --short HEAD',
                returnStdout: true).trim()
            }
          }
        }
        
        stage('check security') {
          parallel {
            
            stage('git secret'){
              steps {
                sh ''' docker run --platform linux/amd64 --rm -i -v "$PWD:/repo" 192.168.1.104:5000/trufflehog git --json --since-commit HEAD --only-verified --fail file:///repo > trufflehog.json'''
              }
             
            }
            
            stage('git leaks'){
              steps {
                sh ''' docker run -v "$PWD:/repo" 192.168.1.104:5000/gitleaks detect --source="/repo" --report-format="json" --report-path="/repo/gitleaks.json" -v '''
              }
            }
             
          }
        
        }
        
        stage('Upload Scan Gitleaks') {
            steps {
                script {
                    sh '''#!/bin/bash
                        API_KEY="6241eeb3e9f7ff818a4a6e976dedaa261dfae5ab"
                        SCAN_TYPE="Gitleaks Scan"
                        FILE_PATH="gitleaks.json"
                       
                        IN=$(curl -X GET --header "Authorization: Token 6241eeb3e9f7ff818a4a6e976dedaa261dfae5ab" 192.168.42.12:8080/api/v2/tests/?engagement=2 | jq -r '[.results[].scan_type] | join(",")')
                        echo "$IN"
                        check_existing_test_by_type() {
                            while [ "$IN" != "$iter" ] ;do
                                iter=${IN%%,*}
                                IN="${IN#$iter,}"
                                echo "$iter"
                                if [ "$iter" = "$SCAN_TYPE" ]; then
                                    return 1
                                fi
                            done
                            return 0
                        }
                        check_existing_test_by_type
                        if [ $? -eq 1 ];then
                            echo "Starting Reimport"
                            curl -X POST --header "Content-Type: multipart/form-data" --header "Authorization: Token $API_KEY" -F "product_id=$PRODUCT_ID" -F "product_name=$PRODUCT_NAME"  -F "engagement=$ENGAGEMENT_ID" -F "active=true" -F "engagement_name=$IMAGE" -F "scan_type=$SCAN_TYPE" -F "file=@$FILE_PATH"  "http://192.168.42.12:8080/api/v2/reimport-scan/"
                        else
                            echo "Starting Import"
                            curl -X POST --header "Content-Type: multipart/form-data" --header "Authorization: Token $API_KEY" -F "product_id=$PRODUCT_ID" -F "engagement=$ENGAGEMENT_ID" -F "active=true" -F "product_name=$PRODUCT_NAME" -F "scan_type=$SCAN_TYPE" -F "file=@$FILE_PATH" "$DOJO_URL/api/v2/import-scan/"
                        fi
                    '''
                }
            }
        }
        stage('Upload Scan Trufflehog') {
            steps {
                script {
                    sh '''#!/bin/bash
                        API_KEY="6241eeb3e9f7ff818a4a6e976dedaa261dfae5ab"
                        SCAN_TYPE="Trufflehog Scan"
                        FILE_PATH="trufflehog.json"
                       
                        IN=$(curl -X GET --header "Authorization: Token 6241eeb3e9f7ff818a4a6e976dedaa261dfae5ab" 192.168.42.12:8080/api/v2/tests/?engagement=2 | jq -r '[.results[].scan_type] | join(",")')
                        echo "$IN"
                        check_existing_test_by_type() {
                            while [ "$IN" != "$iter" ] ;do
                                iter=${IN%%,*}
                                IN="${IN#$iter,}"
                                echo "$iter"
                                if [ "$iter" = "$SCAN_TYPE" ]; then
                                    return 1
                                fi
                            done
                            return 0
                        }
                        check_existing_test_by_type
                        if [ $? -eq 1 ];then
                            echo "Starting Reimport"
                            curl -X POST --header "Content-Type: multipart/form-data" --header "Authorization: Token $API_KEY" -F "product_id=$PRODUCT_ID" -F "product_name=$PRODUCT_NAME"  -F "engagement=$ENGAGEMENT_ID" -F "active=true" -F "engagement_name=$IMAGE" -F "scan_type=$SCAN_TYPE" -F "file=@$FILE_PATH"  "http://192.168.42.12:8080/api/v2/reimport-scan/"
                        else
                            echo "Starting Import"
                            curl -X POST --header "Content-Type: multipart/form-data" --header "Authorization: Token $API_KEY" -F "product_id=$PRODUCT_ID" -F "engagement=$ENGAGEMENT_ID" -F "active=true" -F "product_name=$PRODUCT_NAME" -F "scan_type=$SCAN_TYPE" -F "file=@$FILE_PATH" "$DOJO_URL/api/v2/import-scan/"
                        fi
                    '''
                }
            }
        }
        
        stage('Sonarqube'){ 
            steps{ 
                withSonarQubeEnv('Sonar-Server-8.9.2'){ 
                    sh ''' /var/lib/jenkins/sonar-cli/bin/sonar-scanner -Dsonar.projectKey=$IMAGE -Dsonar.sources=.  -Dsonar.exclusions=dependency-check-*''' 
                }
            }
        }
        
        stage('OWASP Dependency-Check Vulnerabilities-SCA') {
            steps{
                //scan Dependency Lib on Project (CI Security)
                dependencyCheck additionalArguments: ''' 
                            --enableExperimental
                           --noupdate
                           -o './'
                           -s './'
                           -f 'ALL' 
                          --prettyPrint''', odcInstallation: 'OWASP-Dependency-Check'
                
                dependencyCheckPublisher pattern: 'dependency-check-report.xml'
            }
        }
        stage('Upload Scan dependency-check-') {
            steps {
                script {
                    sh '''#!/bin/bash
                        API_KEY="6241eeb3e9f7ff818a4a6e976dedaa261dfae5ab"
                        SCAN_TYPE="Dependency Check Scan"
                        FILE_PATH="dependency-check-report.xml"
                       
                        IN=$(curl -X GET --header "Authorization: Token 6241eeb3e9f7ff818a4a6e976dedaa261dfae5ab" 192.168.42.12:8080/api/v2/tests/?engagement=2 | jq -r '[.results[].scan_type] | join(",")')
                        echo "$IN"
                        check_existing_test_by_type() {
                            while [ "$IN" != "$iter" ] ;do
                                iter=${IN%%,*}
                                IN="${IN#$iter,}"
                                echo "$iter"
                                if [ "$iter" = "$SCAN_TYPE" ]; then
                                    return 1
                                fi
                            done
                            return 0
                        }
                        check_existing_test_by_type
                        if [ $? -eq 1 ];then
                            echo "Starting Reimport"
                            curl -X POST --header "Content-Type: multipart/form-data" --header "Authorization: Token $API_KEY" -F "product_id=$PRODUCT_ID" -F "product_name=$PRODUCT_NAME"  -F "engagement=$ENGAGEMENT_ID" -F "active=true" -F "engagement_name=$IMAGE" -F "scan_type=$SCAN_TYPE" -F "file=@$FILE_PATH"  "http://192.168.42.12:8080/api/v2/reimport-scan/"
                        else
                            echo "Starting Import"
                            curl -X POST --header "Content-Type: multipart/form-data" --header "Authorization: Token $API_KEY" -F "product_id=$PRODUCT_ID" -F "engagement=$ENGAGEMENT_ID" -F "active=true" -F "product_name=$PRODUCT_NAME" -F "scan_type=$SCAN_TYPE" -F "file=@$FILE_PATH" "$DOJO_URL/api/v2/import-scan/"
                        fi
                    '''
                }
            }
        }
        stage('Build') {
            steps {
              sh ''' echo $CI_COMMIT_SHORT_SHA '''
              sh ''' DOCKER_BUILDKIT=1 docker build -t $REGISTERY/$IMAGE:v1 . '''
              sh ''' DOCKER_BUILDKIT=1 docker build -t $REGISTERY/$IMAGE:$CI_COMMIT_SHORT_SHA . '''
            }
        }
        stage('Trivy'){ 
            steps{
                sh ''' trivy image --db-repository $REGISTERY/aquasecurity/trivy-db:2 --java-db-repository $REGISTERY/aquasecurity/trivy-java-db:1 -f json -o trivy.json $REGISTERY/$IMAGE:$CI_COMMIT_SHORT_SHA '''
            }
        }
        stage('Upload Scan Trivy') {
            steps {
                script {
                    sh '''#!/bin/bash
                        API_KEY="6241eeb3e9f7ff818a4a6e976dedaa261dfae5ab"
                        SCAN_TYPE="Trivy Scan"
                        FILE_PATH="trivy.json"
                       
                        IN=$(curl -X GET --header "Authorization: Token 6241eeb3e9f7ff818a4a6e976dedaa261dfae5ab" 192.168.42.12:8080/api/v2/tests/?engagement=2 | jq -r '[.results[].scan_type] | join(",")')
                        echo "$IN"
                        check_existing_test_by_type() {
                            while [ "$IN" != "$iter" ] ;do
                                iter=${IN%%,*}
                                IN="${IN#$iter,}"
                                echo "$iter"
                                if [ "$iter" = "$SCAN_TYPE" ]; then
                                    return 1
                                fi
                            done
                            return 0
                        }
                        check_existing_test_by_type
                        if [ $? -eq 1 ];then
                            echo "Starting Reimport"
                            curl -X POST --header "Content-Type: multipart/form-data" --header "Authorization: Token $API_KEY" -F "product_id=$PRODUCT_ID" -F "product_name=$PRODUCT_NAME"  -F "engagement=$ENGAGEMENT_ID" -F "active=true" -F "engagement_name=$IMAGE" -F "scan_type=$SCAN_TYPE" -F "file=@$FILE_PATH"  "http://192.168.42.12:8080/api/v2/reimport-scan/"
                        else
                            echo "Starting Import"
                            curl -X POST --header "Content-Type: multipart/form-data" --header "Authorization: Token $API_KEY" -F "product_id=$PRODUCT_ID" -F "engagement=$ENGAGEMENT_ID" -F "active=true" -F "product_name=$PRODUCT_NAME" -F "scan_type=$SCAN_TYPE" -F "file=@$FILE_PATH" "$DOJO_URL/api/v2/import-scan/"
                        fi
                    '''
                }
            }
        }
        stage('Push To Docker Registries') {
            steps {
              sh ''' docker push $REGISTERY/$IMAGE:v1 '''
              sh ''' docker push $REGISTERY/$IMAGE:$CI_COMMIT_SHORT_SHA '''
            }
        }
        
        
        stage('Dast Zap Analaysis') {
          parallel {
              
            stage('Zap Import Context'){
              steps {
                sh ''' zap-cli --zap-url http://192.168.1.109 --port 8080 --api-key fkeaip9dqcg9229tpm9834vsod context import "Default Context" '''
              }
            }
            stage('Zap Open-url'){
              steps {
                sh ''' zap-cli --zap-url http://192.168.1.109 --port 8080 --api-key fkeaip9dqcg9229tpm9834vsod open-url http://192.168.42.232 '''
              }
            }
            
            
            stage('Zap Spider Scan Without Username'){
              steps {
                sh ''' zap-cli --zap-url http://192.168.1.109 --port 8080 --api-key fkeaip9dqcg9229tpm9834vsod spider -c "Default Context"  http://192.168.42.232 '''
              }
            }
            
            
            
            stage('Zap Active Scan Without Username'){
              steps {
                sh ''' zap-cli --zap-url http://192.168.1.109 --port 8080 --api-key fkeaip9dqcg9229tpm9834vsod active-scan --recursive -c "Default Context"  http://192.168.42.232 '''
              }
            }
            
            stage('Zap Publish Report'){
              steps {
                sh ''' zap-cli --zap-url http://192.168.1.109 --port 8080 --api-key fkeaip9dqcg9229tpm9834vsod  report -f xml -o python.xml '''
              }
            }
          }
        }
        stage('Upload Zap Report') {
            steps {
                script {
                    sh '''#!/bin/bash
                        API_KEY="6241eeb3e9f7ff818a4a6e976dedaa261dfae5ab"
                        SCAN_TYPE="ZAP Scan"
                        FILE_PATH="python.xml"
                       
                        IN=$(curl -X GET --header "Authorization: Token 6241eeb3e9f7ff818a4a6e976dedaa261dfae5ab" 192.168.42.12:8080/api/v2/tests/?engagement=2 | jq -r '[.results[].scan_type] | join(",")')
                        echo "$IN"
                        check_existing_test_by_type() {
                            while [ "$IN" != "$iter" ] ;do
                                iter=${IN%%,*}
                                IN="${IN#$iter,}"
                                echo "$iter"
                                if [ "$iter" = "$SCAN_TYPE" ]; then
                                    return 1
                                fi
                            done
                            return 0
                        }
                        check_existing_test_by_type
                        if [ $? -eq 1 ];then
                            echo "Starting Reimport"
                            curl -X POST --header "Content-Type: multipart/form-data" --header "Authorization: Token $API_KEY" -F "product_id=$PRODUCT_ID" -F "product_name=$PRODUCT_NAME"  -F "engagement=$ENGAGEMENT_ID" -F "active=true" -F "engagement_name=$IMAGE" -F "scan_type=$SCAN_TYPE" -F "file=@$FILE_PATH"  "http://192.168.42.12:8080/api/v2/reimport-scan/"
                        else
                            echo "Starting Import"
                            curl -X POST --header "Content-Type: multipart/form-data" --header "Authorization: Token $API_KEY" -F "product_id=$PRODUCT_ID" -F "engagement=$ENGAGEMENT_ID" -F "active=true" -F "product_name=$PRODUCT_NAME" -F "scan_type=$SCAN_TYPE" -F "file=@$FILE_PATH" "$DOJO_URL/api/v2/import-scan/"
                        fi
                    '''
                }
            }
        }                      
    }
}