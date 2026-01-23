pipeline {
    agent { label "OneS" }
    environment {
        workDir = "D:\\addocs"
        rootDir = "D:\\ДЛЯ РЕЛИЗОВ\\work\\Данные конфигураций"
    }
    stages {
        stage('Подготовка .cf') {
            steps {
                script {
                    if (params.product == 'Fitness') {
                        env.base = "VAFitness"
                        env.dir = "${env.rootDir}\\Фитнес клуб КОРП 4.0\\cf"
                        env.rep = "${repositoryReleaseFitness}"
                        env.nameFile = "1С_Фитнес клуб КОРП. Сборка ${params.newversion}. Изменения и дополнения к документации.htm"
                    } else if (params.product == 'Salon') {
                        env.base = "VASPA"
                        env.dir = "${env.rootDir}\\SPA-Салон 3.0"
                        env.rep = "${repositoryReleaseSalon}"
                        env.nameFile = "1С_Салон красоты. Сборка ${params.newversion}. Изменения и дополнения к документации"
                    } else {
                        env.base = "VAStoma"
                        env.dir = "${env.rootDir}\\1С_Стоматология 2.1\\CF"
                        env.rep = "${repositoryReleaseStom}"
                        env.nameFile = "1С_Медицина. Стоматологическая клиника. Сборка ${params.newversion}. Изменения и дополнения к документации.htm"
                    }
                    // Очистка предыдущих данных
                    bat""" 
                    chcp 65001
                    if exist "${env.workDir}" rmdir /S /Q "${env.workDir}"
                    mkdir "${env.workDir}\\new" "${env.workDir}\\old" "${env.workDir}\\xml_new" "${env.workDir}\\xml_old"
                    """
                    echo "product=${params.product}, base=${env.base}, dir=${env.dir}"
                }
            }
        }
        stage('Обработка .cf') {
            parallel {
                stage('Выгрузка .cf из релизного') {
                    steps {
                        bat """
                            chcp 65001
                            @call vrunner loadrepo --storage-name ${env.rep} --storage-user ${env.VATest2} --ibconnection /Slocalhost/${env.base} --db-user Админ
                            @call vrunner updatedb --ibconnection /Slocalhost/${env.base} --db-user Админ
                            @call vrunner unload "${env.workDir}\\new\\${params.newversion}.cf" --ibconnection /Slocalhost/${env.base} --db-user Админ
                        """
                    }
                }
                stage('Перенос .cf') {
                    steps {
                        script {
                            def sourceFile = "${env.dir}\\${params.oldversion}.cf"
                            if (!fileExists(sourceFile)) {
                                error("Ошибка: Файл ${sourceFile} не найден.")
                            }
                            bat """
                                chcp 65001
                                copy "${sourceFile}" "${env.workDir}\\old"
                            """
                        }
                    }
                }
            }
        }
        stage('Подключение и обновление из хранилища') {
            parallel {
                stage('Сравнение конфигураций') {
                    steps {
                        bat """
                            chcp 65001
                            @call vrunner compare --secondFile "${env.workDir}\\old\\${params.oldversion}.cf" --reportFile "${env.workDir}\\Отчет.txt" --reportType Brief --firstFile "${env.workDir}\\new\\${params.newversion}.cf" --ibconnection /Slocalhost/${env.base} --db-user Админ
                        """
                    }
                }
                stage('Выгрузка новой версии') {
                    steps {
                        bat """
                            chcp 65001
                            @call vrunner decompile --out ${env.workDir}\\xml_new --in "${env.workDir}\\new\\${params.newversion}.cf" --ibconnection /Slocalhost/${env.base} --db-user Админ 
                        """
                    }
                }
                stage('Выгрузка старой версии') {
                    steps {
                        bat """
                            chcp 65001
                            @call vrunner decompile --out ${env.workDir}\\xml_old --in "${env.workDir}\\old\\${params.oldversion}.cf" --ibconnection /Slocalhost/${env.base} --db-user Админ 
                        """
                    }
                }
            }
        }
     }
}
def updateConfigFile() {
    def configJson = readFile(file: 'addocs/VAParams.json')
    def updatedConfigJson = configJson.replaceAll(/\$\{nameFile\}/, env.nameFile)
    writeFile(file: 'addocs/VAParams.json', text: updatedConfigJson)
}