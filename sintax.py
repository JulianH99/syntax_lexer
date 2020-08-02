from lexer import TOKENS
from queue import Queue, LifoQueue


class SQLSyntaxError(Exception):
    def __init__(self, message, line, col):
        self.message = message
        self.line = line
        self.col = col

    def __str__(self):
        return "{} at line {} col {}".format(self.message, self.line, self.col)


class SyntaxAnalyzer:

    token_list = []
    qtoken = Queue()

    def __init__(self, sql_file, tokens):
        """

        :param sql_file: SQLFileReader object
        :param tokens: LexerStream object
        """
        self.sql_file = sql_file

        self.token_list = [(tok.name, tok.value) for tok in tokens]
        [self.qtoken.put(token) for token in self.token_list]

    def start_analysis(self):

        index = 0
        paren_stack = LifoQueue()
        prev_token_val = ''
        param_name_stack = LifoQueue()

        begin_found = False
        end_found = False

        in_select = False

        while not self.qtoken.empty():
            token = self.qtoken.get()
            token_name = token[0]
            token_value = token[1]
            print(token_name, token_value)

            if index == 0 and token_name != 'CREATE':
                raise SQLSyntaxError('No create keyword found', 0, 0)

            if index == 1 and token_name != 'PROCEDURE':
                raise SQLSyntaxError('No procedure keyword found', 0, 0)

            if index == 2 and token_name != 'OBJECT_NAME':
                raise SQLSyntaxError('No procedure name found after PROCEDURE keyworkd',
                                     self.sql_file.locate(TOKENS['PROCEDURE']),
                                     len(TOKENS['PROCEDURE']))

            if token_name == 'L_PAREN':
                paren_stack.put_nowait((token_value, self.token_list[index - 1][1]))

            elif token_name == 'PARAM_TYPE':
                param_name_stack.put_nowait(token_name)

            elif token_name == 'OBJECT_NAME':
                param_name_stack.put_nowait(token_name)

            elif token_name == 'PARAM_DTYPE':
                if param_name_stack.qsize() > 0:
                    tok = param_name_stack.get()
                    if tok == 'OBJECT_NAME':
                        index += 1
                        continue
                    while not param_name_stack.empty():
                        param_name_stack.get()
                raise SQLSyntaxError('Missing param name',
                                     self.sql_file.locate(token_value),
                                     0)
            elif token_name == 'R_PAREN':
                prev_token_val = self.token_list[index - 1][1]
                line = self.sql_file.locate(prev_token_val)

                if paren_stack.qsize() == 0 or paren_stack.get()[0] != '(':
                    raise SQLSyntaxError('Missing opening parent in line', line, 0)

            elif token_name == 'BEGIN':
                begin_found = True

            elif token_name == 'SELECT':
                if not begin_found:
                    raise SQLSyntaxError('begin keyword must come before any statement',
                                         self.sql_file.locate('select'),
                                         0)

                else:
                    in_select = True

            elif token_name == 'ALL':
                if in_select:
                    prev_token_name = self.token_list[index -1][0]
                    print("prev token name", prev_token_name, index -1)
                    if prev_token_name not in ['SELECT', 'COMMA']:
                        raise SQLSyntaxError('Invalid token found near %s' % TOKENS['ALL'],
                                             self.sql_file.locate('*'),
                                             0)

            elif token_name == 'COMMA':
                prev_token_name = self.token_list[index-1][0]
                prev_token_val = self.token_list[index-1][1]
                if prev_token_name not in ['OBJECT_NAME', 'PARAM_DTYPE', 'SINGLE_QUOTE', 'NUMBER', 'ALL']:
                    raise SQLSyntaxError('Invalid token near %s' % token_value,
                                         self.sql_file.locate(prev_token_val),
                                         len(prev_token_name))

            elif token_name == 'FROM':
                prev_token_name = self.token_list[index-1][0]
                prev_token_val = self.token_list[index-1][1]

                if prev_token_name not in ['OBJECT_NAME', 'ALL']:
                    raise SQLSyntaxError('Invalid token near %s' % token_value,
                                         self.sql_file.locate(prev_token_val),
                                         0)

            elif token_name == 'WHERE':
                prev_token_name = self.token_list[index-1][0]
                next_token_name = self.token_list[index+1][0]

                if prev_token_name not in ['OBJECT_NAME']:
                    raise SQLSyntaxError('Missing table name near %s' % token_value,
                                         self.sql_file.locate(token_value),
                                         0)

                if next_token_name not in ['OBJECT_NAME']:
                    print(next_token_name)
                    raise SQLSyntaxError('Missing column name near %s' % token_value,
                                         self.sql_file.locate(token_value),
                                         0)
            elif token_name == 'OPERATOR':
                prev_token_name = self.token_list[index - 1][0]
                next_token_name = self.token_list[index + 1][0]

                if prev_token_name not in ['OBJECT_NAME']:
                    raise SQLSyntaxError('Missing column name near %s' % token_value,
                                         self.sql_file.locate(token_value),
                                         0)

                if next_token_name not in ['SINGLE_QUOTE', 'NUMBER', 'OBJECT_NAME', 'L_PAREN']:
                    raise SQLSyntaxError('Wrong right side of operator %s' % token_value,
                                         self.sql_file.locate(token_value),
                                         0)

            elif token_name == 'END':
                end_found = True

            index += 1

        if paren_stack.qsize() > 0:
            raise SQLSyntaxError('Missing closing parent',
                                 paren_stack.get()[0],
                                 0)

        if not begin_found:
            raise SQLSyntaxError('Missing begin keyword',
                                 0,
                                 0)

        if not end_found:
            raise SQLSyntaxError('Missing end keyword',
                                 len(self.sql_file.lines),
                                 0)

        return True






