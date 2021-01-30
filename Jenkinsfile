pipeline {
	agent any
	stages {
		stage("Pull code") {
		    steps {
			sh "rm -f -R search-engine"
			sh "git clone git@github.com:saraivaufc/search-engine.git"
		    }
		}
		stage("Scan code") {
			steps {
				dir("search-engine") {
					sh "/opt/sonar-scanner/bin/sonar-scanner -Dsonar.projectKey=search-engine -Dsonar.sources=. -Dsonar.host.url=http://sonarqube:9000 -Dsonar.login=63deffbc0a66d8ba8886b7d80acb0dadeaf156af"
				}
			}
		}
	}
}
