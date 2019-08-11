file = open("test.txt","r", encoding='utf-8')
explane_cache = ''
file.readline()


def handler_explane(explanes):
    line = explanes.split('\n')
    result = line[0]
    for x in range(1, len(line) - 1):
        if line[x].strip() == '' or line[x][0].islower():
            result = result + ' ' + line[x]
        else:
            result = result + '\n' + line[x]
    return result

while(True):
    temp = file.readline()
    if temp[0:3] == 'Ref':
        explane = handler_explane(explane_cache)
        print(explane)
        break
    else:
        explane_cache+=temp