from flask import Flask, request, render_template
import ply.lex as lex

app = Flask(__name__)

reserved = {
    "for": "FOR",
    "do": "DO",
    "while": "WHILE",
    "if": "IF",
    "else": "ELSE",
    "int": "INT",
    "float": "FLOAT",
    "string": "STRING",
    "programa": "PROGRAMA",
}

polla = {
    "suma": "SUMA",
    "menos": "MENOS",
    "a": "A",
    "b": "B",
    "c": "C",
    "printf": "Printf",
    "read": "READ",
    "end": "END",
}

tokens = [
    'NUMBER', 'LPAREN', 'RPAREN', 'COMMA', 'SEMICOLON', 'COLON', 'PLUS', 'MINUS', 'EQUALS',
    'LBRACE', 'RBRACE', 'DOT', 'ID', 'STRING', 'ERROR'
] + list(reserved.values()) + list(polla.values())

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'
t_COLON = r':'
t_PLUS = r'\+'
t_MINUS = r'-'
t_EQUALS = r'='
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_DOT = r'\.'
t_STRING = r'\"([^\\\n]|(\\.))*?\"'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    elif t.value in polla:
        t.type = polla[t.value]
    else:
        t.type = 'ERROR'
    return t

t_ignore = ' \t\n'

def t_error(t):
    t.type = 'ERROR'
    t.value = t.value[0]
    t.lexer.skip(1)
    return t

lexer = lex.lex()

@app.route('/', methods=['GET', 'POST'])
def index():
    tokens_list = []
    if request.method == 'POST':
        input_text = request.form['inputText']
        lexer.input(input_text)

        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens_list.append(tok)

    return render_template('index.html', tokens=tokens_list, reserved=reserved, polla=polla)

if __name__ == '__main__':
    app.run(debug=True)
