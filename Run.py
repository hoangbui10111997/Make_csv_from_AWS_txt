import csv
import os
file_cache = open("Cache.txt", "w", encoding='utf-8')


def fix_condition(a, b):
    if b.strip() == '':
        return True
    if b[0].islower():
        return True
    if (len(b)+5) < len(a):
        return True
    if 'AWS' in a[(len(a)-4):]:
        return True
    if 'Data' in a[(len(a)-4):]:
        return True
    if 'and' in a[(len(a)-4):]:
        return True
    if 'or' in a[(len(a)-3):]:
        return True
    if 'of' in a[(len(a)-3):]:
        return True
    if ',' in a[(len(a)-2):]:
        return True
    if '.' in a[(len(a)-2):]:
        return True
    return False


def handler_explane(explanes):
    line = explanes.split('\n')
    result = line[0].capitalize()
    for x in range(1, len(line) - 1):
        if fix_condition(line[x-1],line[x]):
            result = result + ' ' + line[x]
        else:
            result = result + '\n' + line[x]
    return result


def handler_answer(answer, choice):
    answers = answer.split(',')
    result = ''
    for x in answers:
        result = result + choice[int(x)-1].strip() + ', '
    return result.strip()[0:(len(result)-2)]


def question_check(question_content):
    try:
        if int(question_content[0:1]) in range(1, 7) and question_content[1:3]=='. ':
            file_cache.write('\n')
            return True
        else:
            return False
    except ValueError:
        return False


def make_cache_file():
    file = open("AWS.txt", "r", encoding='utf-8')
    read_flag = True
    while True:
        pass_question = file.readline()
        if pass_question[0:3] == 'SET':
            break
    while True:
        if read_flag:
            content = file.readline()
        if content.strip() == 'MARK TO STOP':
            file_cache.write('MARK TO STOP')
            break
        if content[0:3] == 'SET':
            while True:
                pass_question = file.readline()
                if pass_question[0:3] == 'SET':
                    break
        read_flag = True
        if content[0:8] == 'Question' and int(content[9:11]) in range(0, 1000):
            answer_flag = False
            choice_flag = False
            explane_flag = False
            while True:
                question_content = file.readline()
                if question_check(question_content):
                    answer_flag = True
                    file_cache.write(question_content.strip())
                elif question_content[0:6] == 'Answer':
                    file_cache.write('\n')
                    file_cache.write(question_content.strip())
                    choice_flag=True
                elif question_content[0:3] == 'Exp':
                    explane_cache = ''
                    while True:
                        temp = file.readline()
                        if temp[0:3] == 'Ref':
                            explane = handler_explane(explane_cache)
                            file_cache.write('\n')
                            file_cache.write(explane.strip())
                            explane_flag = True
                            break
                        else:
                            explane_cache+=temp
                else:
                    if answer_flag == True and question_content.strip() != '' and choice_flag == True and explane_flag == True:
                        read_flag = False
                        file_cache.write('\nEnd\n')
                        content = question_content
                        break
                    file_cache.write(question_content.strip())
                    file_cache.write(' ')
    file.close()


def create_csv():
    filecsv = open('AWS.csv', mode='w', newline='')
    fields = ['Question', 'Choice1', 'Choice2', 'Choice3', 'Choice4', 'Choice5', 'Answer', 'Explane']
    writer = csv.DictWriter(filecsv, fieldnames=fields)
    writer.writeheader()
    file = open("Cache.txt", "r", encoding='utf-8')
    while True:
        Question = file.readline().strip()
        if Question.strip() == 'MARK TO STOP':
            break
        Choice = ['','','','','']
        count = 0
        Explane = ''
        while True:
            choice_cache = file.readline()
            if choice_cache[0] != 'A':
                Choice[count] = choice_cache.strip()
                count += 1
            else:
                Answer = handler_answer(choice_cache[8:], Choice)
                break
        while True:
            temp = file.readline()
            if temp.strip() == 'End':
                break
            else:
                Explane += temp
        print(Question)
        print(Choice[0])
        print(Choice[1])
        print(Choice[2])
        print(Choice[3])
        print(Choice[4])
        print(Answer)
        print(Explane.strip())
        writer.writerow({'Question':Question, 'Choice1':Choice[0], 'Choice2':Choice[1], 'Choice3':Choice[2], 'Choice4':Choice[3], 'Choice5':Choice[4], 'Answer':Answer, 'Explane':Explane.strip()})


def main():
    make_cache_file()
    print("Make cache complete!")
    file_cache.close()
    create_csv()
    print("Create file CSV complete!")
    os.remove("Cache.txt")
    print("Deleted Cache file")


if __name__ == '__main__':
    main()
