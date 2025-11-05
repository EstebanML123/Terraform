pipeline {
    agent any
    
    environment {
        DOCKER_HOST = "unix:///var/run/docker.sock"
    }
    
    stages {
        stage('Verify Environment') {
            steps {
                sh '''
                    echo "=== Herramientas disponibles ==="
                    docker --version
                    docker-compose --version
                    echo "=== Estructura del proyecto ==="
                    pwd
                    ls -la
                '''
            }
        }
        
        stage('Build') {
            steps {
                sh 'docker-compose build --no-cache'
            }
        }
        
        stage('Start Test Infrastructure') {
            steps {
                sh '''
                    echo "=== Iniciando solo MySQL y Redis para tests ==="
                    docker-compose -f docker-compose.test.yml up -d test-mysql test-redis
                    echo "=== Esperando 45 segundos para inicialización de MySQL ==="
                    sleep 45
                    echo "=== Verificando estado de los servicios ==="
                    docker-compose -f docker-compose.test.yml ps
                    docker-compose -f docker-compose.test.yml logs test-mysql | tail -20
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    echo "=== Ejecutando tests con aplicación ==="
                    docker-compose -f docker-compose.test.yml up --abort-on-container-exit --exit-code-from test-web
                '''
            }
            post {
                always {
                    sh '''
                        echo "=== Guardando logs de test ==="
                        docker-compose -f docker-compose.test.yml logs --no-color > test_logs.txt 2>&1 || true
                        echo "=== Logs guardados correctamente ==="
                        tail -n 50 test_logs.txt || true

                        echo "=== Deteniendo entorno de test ==="
                        docker-compose -f docker-compose.test.yml down || true
                    '''
                    archiveArtifacts artifacts: 'test_logs.txt', allowEmptyArchive: true
                }
            }
        }
        
        stage('Deploy to Development') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                sh '''
                    echo "=== Desplegando entorno de desarrollo ==="
                    docker-compose down || true
                    docker-compose up -d
                    echo "=== Esperando que Flask se inicie ==="
                    sleep 30
                '''
            }
        }
        
        stage('Integration Test') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                sh '''
                    echo "=== Realizando pruebas de integración ==="
                    timeout time: 90, unit: 'SECONDS', activity: true {
                        while true; do
                            if curl -s -f http://localhost:5000/login > /dev/null; then
                                echo "✅ Aplicación Flask respondiendo"

                                # Acepta "Register" o "Registro" (por si el idioma varía)
                                if curl -s http://localhost:5000/register | grep -iq "register\\|registro"; then
                                    echo "✅ Formulario de registro accesible"
                                    echo "🎉 Todas las pruebas pasaron correctamente"
                                    break
                                else
                                    echo "⏳ Esperando servicios..."
                                    sleep 10
                                fi
                            else
                                echo "⏳ Esperando que la aplicación esté lista..."
                                sleep 10
                            fi
                        done
                    }
                '''
            }
        }
    }
    
    post {
        success {
            echo "🎉 Pipeline COMPLETADO EXITOSAMENTE"
        }
        failure {
            echo "❌ Pipeline FALLÓ - Revisar logs de test"
            sh '''
                echo "=== Últimos logs de MySQL ==="
                docker-compose -f docker-compose.test.yml logs test-mysql | tail -30 || true
                echo "=== Últimos logs de Test Web ==="
                docker-compose -f docker-compose.test.yml logs test-web | tail -30 || true
            '''
        }
        always {
            sh '''
                echo "=== Limpiando entorno de desarrollo ==="
                docker-compose down || true
                echo "=== Liberando espacio Docker ==="
                docker system prune -f || true
            '''
            // 🔹 Se limpia el workspace al final, no antes de leer los logs
            cleanWs()
        }
    }
}
