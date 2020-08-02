from rply import LexerGenerator


TOKENS = {
    'LOGICAL': r'(and|or|not)+',
    'CREATE': r'create',
    'PROCEDURE': r'procedure',
    'BEGIN': r'begin',
    'END': r'end',
    'INSERT': r'(insert)+',
    'INTO': r'(into)+',
    'PARAM_DTYPE': r'(int|varchar|double|bit|boolean)+',
    'PARAM_TYPE': r'(out|inout|in)+',
    'PARAM_NAME': r'((in|out|inout)) (\D\w+) ((int|varchar|double|bit|boolean))',
    'L_PAREN': r'\(+',
    'R_PAREN': r'\)+',
    'COMMA': ',+',
    'SELECT': r'(select)+',
    'FROM': r'(from)+',
    'ALL': r'(\*)+',
    'UPDATE': r'(update)+',
    'VALUES': r'(values)+',
    'SEMI': r';+',
    'WHERE': r'(where)+',
    'SET': r'(set)+',
    'OPERATOR': r'(\=|\<\=|\>\=|\>|\<|\<\>|\!\=)+',
    'ARITHMETICAL': r'(\+|\-|\/)+',

    'SINGLE_QUOTE': '\'+',
    'LT': '<+',
    'NUMBER': r'\d+',
    'OBJECT_NAME': r'[a-z_]+',
}

lg = LexerGenerator()
lg.ignore(r'\s')

for tok_name, tok_val in TOKENS.items():
    lg.add(tok_name, tok_val)



