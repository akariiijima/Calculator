def readNumber(line, index, num):
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
    token = {'type': 'NUMBER', 'number': number * keta, 'priority': 0, 'bracket': num}
    return token, index


def readPlus(line, index, num):
    token = {'type': 'PLUS', 'priority': 0, 'bracket': num, 'number': 'null'}
    return token, index + 1


def readMinus(line, index, num):
    token = {'type': 'MINUS', 'priority': 0, 'bracket': num, 'number': 'null'}
    return token, index + 1

def readTimes(line, index, num):
    token = {'type': 'TIMES', 'priority': 0, 'bracket': num, 'number': 'null'}
    return token, index + 1

def readDivided(line, index, num):
    token = {'type': 'DIVIDED', 'priority': 0, 'bracket': num, 'number': 'null'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    count = 0
    #不必要な()がないか※例:(1+3)
    if(line[0] == '(' and line[len(line)-1] == ')'):
        num = -1
    else:
        num = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index, num)
        elif line[index] == '+':
            (token, index) = readPlus(line, index, num)
        elif line[index] == '-':
            (token, index) = readMinus(line, index, num)
        elif line[index] == '*':
            (token, index) = readTimes(line, index, num)
        elif line[index] == '/':
            (token, index) = readDivided(line, index, num)
        elif line[index] == '(':
            num += 1
            index += 1
            count += 1
            continue
        elif line[index] == ')':
            num -= 1
            index += 1
            continue
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

#優先度をつけたものをリストで括る「(」「)」→'bracket'の順位
def make_list_Bracket(tokens, count):#初期値count=0,count=0,1,2,....n(「()」の回数分)
    token = []
    new_tokens = []
    num = count
    for index in range(len(tokens)):
        if(tokens[index]['bracket'] >= num+1):
            token.append(tokens[index])
        if(tokens[index]['bracket'] == num):
            if(len(token) == 0):
                new_tokens.append(tokens[index])
            else:
                new_tokens.append(token)
                new_tokens.append(tokens[index])
                token = []
    if(len(token) != 0):
        new_tokens.append(token)

    count += 1
    #()の中に()がないかcheck
    for index in range(len(new_tokens)):
        if isinstance(new_tokens[index], list):#もしリストがあった場合
            new_tokens[index] = make_list_Bracket(new_tokens[index], count)#再帰
    return new_tokens


#字句に優先度をつける
def check_priority(tokens):
    for index in range(len(tokens) - 1):
        if isinstance(tokens[index], list):#もしリストがあった場合(index番目)
            tokens[index] = {'number': check_priority(tokens[index]),'priority': 0,'type': 'NUMBER'}#再帰
        if isinstance(tokens[index + 1], list):#もしリストがあった場合(index+1番目)...★何故か？
            tokens[index + 1] = {'number': check_priority(tokens[index + 1]),'priority': 0,'type': 'NUMBER'}#再帰
        
        if(tokens[index]['type'] == 'TIMES' or tokens[index]['type'] == 'DIVIDED'):
            tokens[index - 1]['priority'] = 1
            tokens[index]['priority'] = 1
            tokens[index + 1]['priority'] = 1#★ここで次のトークンを調べたいから
            
    return tokens



#優先度をつけたものをリストで括る「*」「/」→'priority'の順位
def make_list_TimesDivided(tokens):
    token = []
    new_tokens = []
    for index in range(len(tokens)):
        if isinstance(tokens[index]['number'], list):#もしリストがあった場合
            tokens[index]['number'] = make_list_TimesDivided(tokens[index]['number'])#再帰
        if(tokens[index]['priority'] == 1):
            token.append(tokens[index])
        if(tokens[index]['priority'] == 0):
            if(len(token) == 0):
                new_tokens.append(tokens[index])
            else:
                new_tokens.append(token)
                new_tokens.append(tokens[index])
                token = []
    if(len(token) != 0):
        new_tokens.append(token)
        
    return new_tokens



#'number':リスト→リストに変換
def numberlist_to_list(tokens):

    for index in range(len(tokens)):
        if isinstance(tokens[index], list):#もしリストがあった場合
            tokens[index] = numberlist_to_list(tokens[index])#再帰
        elif isinstance(tokens[index]['number'], list):#もし'number':リストであった場合
            tokens[index] = tokens[index]['number']
            tokens[index] = numberlist_to_list(tokens[index])#再帰
        
    return tokens

    



def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if isinstance(tokens[index], list):#もしリストがあった場合
            tokens[index] = {'type' : 'NUMBER','number' : evaluate(tokens[index])}#再帰
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
    enclose_tokens1 = make_list_Bracket(tokens,0)
    checked_tokens = check_priority(enclose_tokens1)
    enclose_tokens2 = make_list_TimesDivided(checked_tokens)
    enclose_tokens3 = numberlist_to_list(enclose_tokens2)
    actualAnswer = evaluate(enclose_tokens3)
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
    test("(3.0+4*(2.9-1))/5", 2.12)
    test("3.0+4*(2.9-1)/5", 4.52)
    test("(3.0+4)*(2.9-1)/5", 2.66)
    test("(3.0+4)*((2.9-1)/5-1)", -4.34)
    test("(1+3*2-3)*3+1-3*6", -5)
    test("1-5+3*(2+1)", 5)
    test("(2*(4+5*3)-2)*4+1", 145)
    test("(3+9-4/3*(2*(4+5*3)-2))*4+1", -143)
    test("(3+9-4/3*(2*(4+5*3)-2))*4.89+8.4653", -167.5747)
    test("(3.2+(1+3/(((1.0*2+1)*9+1)*2+4.0)))*4+1", 18)
    test("(3+4)", 7)
    print("==== Test finished! ====\n")

runTest()

while True:
    line = input('> ')
    tokens = tokenize(line)#字句を分割する
    enclose_tokens1 = make_list_Bracket(tokens,0)#優先度をつけたものをリストで括る「(」「)」→'bracket'の順位
    checked_tokens = check_priority(enclose_tokens1)#字句に優先度をつける
    enclose_tokens2 = make_list_TimesDivided(checked_tokens)#優先度をつけたものをリストで括る「*」「/」→'priority'の順位
    enclose_tokens3 = numberlist_to_list(enclose_tokens2)#'number':リスト→リストに変換
    answer = evaluate(enclose_tokens3)
    print("answer = %f\n" % answer)


