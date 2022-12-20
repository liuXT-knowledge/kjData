'''
1. 将题目格式化成excel表格
2. 再用excel将表格数据另存为csv文件
3. 把csv导入anki，使用会计模板，制作好anki的会计题库
'''
import pandas as pd
import re

csvFileds = ["id","question","options","answer","notes","Tags","questionPre"]
cards = []
bookCode = None
questionCode = '（　）|（ ）|（）'
tagCode = '　|：'

dataFrom = 'wx'
dataCode = '22'

bookName = 'jjf'
bookZj = [10,11]


if(bookName == 'sw'):
    bookCode = f'{dataCode}01'
if(bookName == 'jjf'):
    bookCode = f'{dataCode}02'

if(bookCode is None):
    print("从新输入正确代码")
    exit(0)

for zj in bookZj:
    txtFile = rf'E:\Projects\vscode\python\kj\{dataFrom}\{bookName}\txt\{zj}.txt'
    with open(txtFile,'r',encoding='utf-8') as file:
        cout = 0
        card = {"id":"","question":"","options":"","answer":"","notes":"","Tags":"","questionPre":""}
        options = ""
        optionJudge = False
        noteJudge = False
        preJudge = False
        note = ""
        questionPre = ''
        while 1:
            line = file.readline()
            if not line:
                break
            is_seprator = '------------' in line
            question = re.search(questionCode,line)
            is_question = question is not None
            is_answer = '正确答案' in line 
            is_note_begin = '答案解析' in line
            is_tag = '考查知识点' in line 
            is_option = re.search('[ABCDYN]',line)
            is_pre_begin = '提示：该题目' in line
            if(is_seprator):
                cout += 1
                id = bookCode + "%02d"%zj + "%03d"%cout
                card["id"] = id 
                card["options"] = options[2:]
                card["notes"] = note
                card["questionPre"] = questionPre
                cards.append(card)
                preJudge = False
                card = {}
                options = ""
                note = ""
                questionPre = ""
                continue
            if(is_question): 
                line = line.replace('\n','').replace(question.group(),'{{c1::}}')
                card["question"] = line
                optionJudge = True
                continue
            if(is_answer): 
                optionJudge = False
                findStr = re.findall('[ABCDYN]',line)
                result = ''.join(findStr)
                result = result.replace('A','1').replace('B','2').replace('C','3').replace('D','4').replace('Y','1').replace('N','2')
                final = ''
                if(len(result)>1):
                    for item in result:
                        final += item + "||"
                    final = final[0:-2]
                else:
                    final = result
                card["answer"] = final
                continue
            if(is_note_begin and len(line)==5): 
                noteJudge = True
                continue
            if(is_tag): 
                tag = re.search(tagCode,line).group()
                
                card["Tags"] = line.split(tag)[1].replace('\n','')
                noteJudge = False
                continue
            if(noteJudge):
                note += line.replace('\n','<br>')
                continue  
            if(optionJudge and len(line)==2 and is_option is not None):
                options += "||"
                continue
            if(optionJudge):
                options += line.replace('\n','<br>')
                continue
            if(is_pre_begin):
                preJudge = True
                continue
            if(preJudge and line[0:3] !='【资料'):
                questionPre += line.replace('\n','<br>')
    csvPath = rf'E:\Projects\vscode\python\kj\{dataFrom}\{bookName}\csv\{zj}.csv'
    data = pd.DataFrame(cards)
    data.to_csv(csvPath,index=False)