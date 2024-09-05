import html
import os
import sys
import shutil
from pathlib import Path
from bs4 import BeautifulSoup

FALSE_SQLITE_INT_VALUE = 0
TRUE_SQLITE_INT_VALUE = 1

def getBooleanSqliteIntValue(boolean: bool) -> int:
   if boolean:
      return TRUE_SQLITE_INT_VALUE
   else:
      return FALSE_SQLITE_INT_VALUE

def getSqlInstructionsFromQuestionHtml(questionId: int, filePath: str) -> str:
   with open(filePath) as fp:
      fileContent = BeautifulSoup(fp, 'html.parser')
      moduleName = fileContent.head.modulename.text
      topicName = fileContent.head.topicname.text
      content = ''
      sqlInstructions = ''

      #empiezo a probar lo de las imagenes
      for imgTag in fileContent.body.find_all('img'):
         imgTag['src'] = str(imgTag['src']).replace('\r\n', '')
         imgTag['src'] = str(imgTag['src']).replace('\n', '')
         imgTag['src'] = str(imgTag['src']).replace(' ', '')

      #termino

      for tag in fileContent.body.find(id="content").children:
         content = content + str(tag)
      
      content = html.escape(content, quote=True)

      if ord(content[:1]) == 10:
         content = content.replace(chr(10), "", 1)

      answers = []

      for tag in fileContent.body.find(id="answers").find_all('li'):
         answer = str(tag.p)
         answer = answer.replace('&lt;-- correcta', '')
         answer = answer.replace('&lt;— correcta', '')
         answer = answer.replace('''&lt;—
                    correcta''', '')
         answer = answer.replace('&lt;—correcta', '')
         answer = answer.replace('''&lt;--
                    correcta''', '')
         
         answer = html.escape(answer, quote=True)

         answers.append((answer, tag.p.text.find('correcta') != -1))
      
      sqlInstructions = f'"""INSERT INTO Question VALUES ({questionId}, \'{moduleName}\', \'{topicName}\', \'{content}\');""",\n\n'

      for answer in answers:
         sqlInstructions = sqlInstructions + f'"""INSERT INTO Answer VALUES ({questionId}, \'{answer[0]}\', ' + str(getBooleanSqliteIntValue(answer[1])) + ');""",\n\n'

   return sqlInstructions



outputQuestionsPath = 'Output/Preguntas'

if not os.path.isdir('Original/Preguntas'):
   sys.exit('Questions folder doesn\'t exist')

if os.path.isdir(outputQuestionsPath):
   shutil.rmtree(outputQuestionsPath)

shutil.copytree('Original/Preguntas', outputQuestionsPath)
questionHtmlFilesPath = Path(outputQuestionsPath).rglob('*.html')
questionId = 0
sqlFile = open(outputQuestionsPath + '/questionsSql.txt', 'a')

for filePath in questionHtmlFilesPath:
   questionId += 1
   sqlInstructions = getSqlInstructionsFromQuestionHtml(questionId, str(filePath.absolute())) + '\n\n\n'
   sqlFile.write(sqlInstructions)

sqlFile.close()