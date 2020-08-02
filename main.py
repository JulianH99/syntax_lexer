from lexer import lg
from file_reader import SqlFileReader
from sintax import SyntaxAnalyzer

sql_file = SqlFileReader('sql.sql')


lex = lg.build()
identified_tokens = lex.lex(sql_file.one_line)


synax = SyntaxAnalyzer(sql_file, identified_tokens)

ok = synax.start_analysis()

if ok:
    print("*******\nSyntax analysis ran ok\n*******")


