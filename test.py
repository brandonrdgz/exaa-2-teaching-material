# from bs4 import BeautifulSoup

# with open("Output/Preguntas/Calculo/Pregunta 01.html") as fp:
#     fileContent = BeautifulSoup(fp, 'html.parser')
#     questionId = fileContent.head.questionid.text
#     moduleName = fileContent.head.modulename.text
#     topicName = fileContent.head.topicname.text
#     content = ''
#     for tag in fileContent.body.find(id="content").children:
#         content = content + str(tag)
#     answers = []
#     for tag in fileContent.body.find(id="answers").find_all('li'):
#         answer = str(tag.p)
#         answer = answer.replace('&lt;-- correcta', '')
#         answer = answer.replace('&lt;— correcta', '')
#         answers.append((answer, tag.p.text.find('correcta') != -1))
#         #print(str(tag.p) + '\n\n')
    
#     print(f'"""INSERT INTO Question VALUES ({questionId}, \'{moduleName}\', \'{topicName}\', \'{content}\')""",\n')

#     for answer in answers:
#         print(f'"""INSERT INTO Answer VALUES ({questionId}, \'{answer[0]}\', \'' + str(answer[1]).upper() + '\')""",\n\n')

from pathlib import Path

result = Path('Original/Preguntas').rglob('*.html')
i = 0

for path in result:
    i += 1
    print(str(i) + '. ' + str(path.absolute()))