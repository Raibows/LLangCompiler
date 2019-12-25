from Struct import *
from prettytable import PrettyTable





class Lexer():
    def __init__(self):
        self.LLang_path = r'./test.LLang'
        self.target_token_path = ''
        self.target_word_table_path = ''
        self.target_formatter_file_path = './rductLang.reduct'
        self.origin_file = []
        self.coder = Code()
        self.tokens = []
        self.symbols = []
        self.unrecognized = []

    def get_symbols(self)->[Symbol]:
        return self.symbols

    def get_tokens(self):
        return self.tokens

    def __add_symbol(self, symbol:Symbol)->bool:
        for one in self.symbols:
            if one.name == symbol.name:
                one.token_labels.append(symbol.token_labels[0])
                return False
        self.symbols.append(symbol)
        return True

    def __correct_real_int(self, wrong:str)->str:
        dot = False
        right = ''
        for l in wrong:
            if l.isdigit():
                right += l
            if l == '.':
                if not dot:
                    right += l
                    dot = True
                else:
                    break
            if l.isalpha():
                break
        if right != wrong:
            print(f'Warning real or int has been corrected from {wrong} to {right}')
        return right


    def __formatter(self):
        with open(self.LLang_path, 'r', encoding='UTF-8') as temp:
            self.origin_file = temp.readlines()
            for i in range(len(self.origin_file)):
                if i == 0:
                    self.origin_file[i] = self.origin_file[i].strip('\ufeff')
                self.origin_file[i] = self.origin_file[i].strip('\n')
                self.origin_file[i] = self.origin_file[i].strip('\r')
                self.origin_file[i] = self.origin_file[i].strip('\t')
                self.origin_file[i] = self.origin_file[i].strip()
                if self.origin_file[i][-1] == ' ':
                    raise RuntimeError('Error line end exits whitespace!', self.origin_file[i])
                # self.origin_file[i] = self.origin_file[i].replace(' ', '')

    def scanner(self):
        self.__formatter()
        if not self.origin_file:
            raise RuntimeError('origin_file is NULL')
        label = 0
        number = 0
        un_index = 0
        for line in self.origin_file:
            i = 0
            while i < len(line):
                # print(line, i)
                if line[i].isalpha(): #tag or key
                    j = i
                    while j < len(line) and (line[j].isalpha() or line[j].isdigit()):
                        j += 1
                    word = line[i:j]
                    i = j

                    judge = self.coder.is_key(word)
                    if judge[0]: # key
                        temp = Token(label, word, judge[1], -1, judge[2])
                        self.tokens.append(temp)
                        label += 1
                        continue

                    judge = self.coder.is_TAG(word)
                    if judge[0]: # tag
                        temp = Token(label, word, judge[1], -1, judge[2])
                        self.tokens.append(temp)
                        temp = Symbol(number, word, judge[1], judge[2], label)
                        if self.__add_symbol(temp):
                            number += 1
                        label += 1
                        continue
                    raise RuntimeError('Either tag nor key !', line, word)

                elif line[i].isdigit() or line[i] == '.':
                    j = i
                    while j < len(line) and (line[j].isdigit() or line[j] == '.' or line[j].isalpha()):
                        j += 1
                    word = line[i:j]
                    i = j
                    word = self.__correct_real_int(word)

                    judge = self.coder.is_INT(word)
                    if judge[0]: # int
                        temp = Token(label, word, judge[1], -1,judge[2])
                        self.tokens.append(temp)
                        temp = Symbol(number, word, judge[1], judge[2], label)
                        if self.__add_symbol(temp):
                            number += 1
                        label += 1
                        continue

                    judge = self.coder.is_REAL(word)
                    if judge[0]: # real
                        temp = Token(label, word, judge[1], -1, judge[2])
                        self.tokens.append(temp)
                        temp = Symbol(number, word, judge[1], judge[2], label)
                        if self.__add_symbol(temp):
                            number += 1
                        label += 1
                        continue
                    raise RuntimeError('Either int nor real !', line, word)

                judge = self.coder.is_bounder(line[i])
                if judge[0]: # bounder
                    if (i+1) < len(line) and self.coder.is_bounder(line[i+1])[0]:
                        raise RuntimeError('Duplicate bounder', line, line[i], line[i+1])
                    temp = Token(label, line[i], judge[1], -1, judge[2])
                    self.tokens.append(temp)
                    label += 1
                    i += 1
                    continue

                judge = self.coder.is_operator(line[i])
                if judge[0]: # operator
                    # 超前搜索一个即可
                    if self.coder.is_operator(line[i+1])[0]: # 2个字符组成的运算符
                        word = line[i] + line[i+1]
                        judge2 = self.coder.is_operator(word)
                        if judge2[0]:
                            temp = Token(label, word, judge2[1], -1, judge2[2])
                            self.tokens.append(temp)
                            label += 1
                            i += 2
                            continue
                        raise RuntimeError('Error defined double chars operator', line, word)
                    else: # single operator
                        temp = Token(label, line[i], judge[1], -1, judge[2])
                        self.tokens.append(temp)
                        label += 1
                        i += 1
                        continue
                if line[i] != ' ':
                    print('Warning, unrecognized letter or word', line, line[i])
                    self.unrecognized.append(Unrecognized(un_index, line, line[i], i))
                    un_index += 1
                i += 1

    def output_formatted_file(self):
        file = []
        i = 0
        while i < len(self.tokens):
            line = []
            if self.tokens[i].label < 2:
                i += 1
                continue
            else:
                while i < len(self.tokens):
                    line.append(self.tokens[i].name)
                    line.append(' ')
                    if self.tokens[i].name == ';':
                        i += 1
                        break
                    i += 1
            file.append(line)
        with open(self.target_formatter_file_path, 'w', encoding='utf-8') as writer:
            for line in file:
                writer.writelines(line)
                writer.writelines('\n')



    def show_tokens(self):
        table = PrettyTable(['label', 'name', 'code', 'type'])
        print(f'共检测到 关键字、标识符、定界符 共 {len(self.tokens)} 个')
        for token in self.tokens:
            table.add_row([token.label, token.name, token.code, token.type])
        print(table)

    def show_symbols(self):
        print(f'共检测到 用户自定义标识符和常数 共 {len(self.symbols)} 个')
        table = PrettyTable(['number', 'name', 'code', 'type', 'Token-labels'])
        for symbol in self.symbols:
            table.add_row([symbol.number, symbol.name, symbol.code, symbol.type, symbol.token_labels])
        print(table)

    def show_unrecognized(self):
        print(f'共检测到 未知符号 共 {len(self.unrecognized)} 个')
        table = PrettyTable(['un_index', 'name', 'pos', 'line'])
        for un in self.unrecognized:
            table.add_row([un.un_index, un.name, un.pos, un.line])
        print(table)

    def show_all(self):
        self.show_tokens()
        print()
        self.show_symbols()
        print()
        self.show_unrecognized()
        print()























    def get_word_token(self, word:str):
        pass


