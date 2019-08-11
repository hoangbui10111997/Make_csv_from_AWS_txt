a = '''hoang huy and
Huy hoang
Bui Hoang'''
line = a.split('\n')
if line[0][(len(line[0])-4):len(line[0])] == ' and':
    print(1)
