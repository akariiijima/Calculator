def readNumber(line, index):
    number = 0
    flag = 0
    keta = 1
    while index < len(line) and (line[index].isdigit() or line[index] == '.'):
        if line[index] == '.':
            flag = 1
        else:
            number = number * 10 + int(line[index])
            if flag == 1:
                keta *= 0.1
        index += 1
    token = {'type': 'NUMBER', 'number': number * keta, 'priority': 0}
    return token, index


def readPlus(line, index):
    token = {'type': 'PLUS', 'priority': 0}
    return token, index + 1


def readMinus(line, index):
    token = {'type': 'MINUS', 'priority': 0}
    return token, index + 1

def readTimes(line, index):
    token = {'type': 'TIMES', 'priority': 0}
    return token, index + 1

def readDivided(line, index):
    token = {'type': 'DIVIDED', 'priority': 0}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readTimes(line, index)
        elif line[index] == '/':
            (token, index) = readDivided(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens



def check_priority(tokens):
    #*と/の連なった群に優先度をつける
    for index in range(len(tokens)):
        if(tokens[index]['type'] == 'TIMES' or tokens[index]['type'] == 'DIVIDED'):
            tokens[index-1]['priority'] = 1
            tokens[index]['priority'] = 1
            tokens[index+1]['priority'] = 1
    return tokens



def make_list_in_list(tokens):
    token1 = []
    new_tokens = []
    for index in range(len(tokens)):
        if(tokens[index]['priority'] == 1):
            token1.append(tokens[index])
        if(tokens[index]['priority'] == 0):
            if(len(token1) == 0):
                new_tokens.append(tokens[index])
            else:
                new_tokens.append(token1)
                new_tokens.append(tokens[index])
                token1 = []
    if(len(token1) != 0):
                new_tokens.append(token1)          
    return new_tokens



def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if isinstance(tokens[index], list):#もしリストがあった場合、再帰
            tokens[index] = {'type' : 'NUMBER','number' : evaluate(tokens[index])}
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            elif tokens[index - 1]['type'] == 'TIMES':
                answer *= tokens[index]['number']
            elif tokens[index - 1]['type'] == 'DIVIDED':
                answer /= tokens[index]['number']
            else:
                print('Invalid syntax')
        index += 1
    return answer


def test(line, expectedAnswer):
    tokens = tokenize(line)
    checked_tokens = check_priority(tokens)
    enclose_tokens = make_list_in_list(checked_tokens)
    actualAnswer = evaluate(enclose_tokens)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expectedAnswer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
    print("==== Test started! ====")
    test("1+2", 3)
    test("1.0+2.1-3", 0.1)
    test("1.0*2.1-3", -0.9)
    test("1.0+2.1*3", 7.3)
    test("2.1/1.0-3", -0.9)
    test("1.0+2.1/3", 1.7)
    test("123.4+123*123/123", 246.4)
    test("1/2*4+1*5-5/1", 2)
    test("1/2*4*2*1/4+1*5/2-5/1", -1.5)
    print("==== Test finished! ====\n")

runTest()

while True:
    line = input('> ')
    tokens = tokenize(line)#字句を分割する
    checked_tokens = check_priority(tokens)#字句に優先度をつける
    enclose_tokens = make_list_in_list(checked_tokens)#優先度をつけたものをリストで括る
    answer = evaluate(enclose_tokens)
    print("answer = %f\n" % answer)


