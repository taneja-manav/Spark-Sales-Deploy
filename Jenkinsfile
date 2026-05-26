/*
 * Jenkinsfile — Declarative Pipeline
 * ====================================
 * CI/CD pipeline for the PySpark Sales Analysis project.
 *
 * Stages:
 *   1. Environment Setup  — Install Python dependencies
 *   2. Linting            — Static analysis with flake8
 *   3. Run Spark Job       — Execute the PySpark sales analysis
 */

pipeline {
    agent any

    environment {
        PYTHON      = 'python3'
        PIP         = 'pip3'
        SPARK_APP   = 'src/sales_analysis.py'
        VENV_DIR    = '.venv'
    }

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        // -------------------------------------------------------
        // Stage 1: Environment Setup
        // -------------------------------------------------------
        stage('Environment Setup') {
            steps {
                echo '=== Setting up Python virtual environment ==='
                sh """
                    ${PYTHON} -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    ${PIP} install --upgrade pip
                    ${PIP} install pyspark flake8 openpyxl pandas
                """
            }
        }

        // -------------------------------------------------------
        // Stage 2: Linting
        // -------------------------------------------------------
        stage('Linting') {
            steps {
                echo '=== Running flake8 linting on source code ==='
                sh """
                    . ${VENV_DIR}/bin/activate
                    flake8 src/ \
                        --max-line-length=120 \
                        --statistics \
                        --count \
                        --show-source
                """
            }
        }

        // -------------------------------------------------------
        // Stage 3: Run Spark Job
        // -------------------------------------------------------
        stage('Run Spark Job') {
            steps {
                echo '=== Executing PySpark Sales Analysis ==='
                sh """
                    . ${VENV_DIR}/bin/activate
                    spark-submit \
                        --master local[*] \
                        --driver-memory 2g \
                        ${SPARK_APP}
                """
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check the logs above for details.'
        }
        always {
            echo '🧹 Cleaning up workspace artifacts...'
            cleanWs(deleteDirs: true, patterns: [[pattern: "${VENV_DIR}/**", type: 'INCLUDE']])
        }
    }
}
