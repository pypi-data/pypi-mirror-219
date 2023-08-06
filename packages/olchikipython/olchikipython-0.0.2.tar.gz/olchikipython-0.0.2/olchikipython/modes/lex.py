# ------------------------------------------------------------
# ply_test.py
#
# tokenizer to test olchikiPython grammer
# ------------------------------------------------------------


def run(args, code):

    import yaml
    language_dict = yaml.load(open(args["dictionary"]), Loader=yaml.SafeLoader)

    if args["reverse"]:
        reserved = {value:key for key, value in language_dict.get("reserved").items()}
        # ------------- Debugging ---------------
        # print ("Reversed:", reserved)
        # ------------- Debugging ---------------

    else:
        reserved = language_dict.get("reserved")
        # ------------- Debugging ---------------
        # print ("normal:", reserved)
        # ------------- Debugging ---------------

        

    # ------------- Debugging ---------------
    # print ("'a' in ASCII number is:", ord('a'))
    # print ("'ا' in ASCII number is:", ord('ا'))
    # print ("'۰' in ASCII number is:", ord('۰'))
    # print ("'۲' in ASCII number is:", ord('۲'))
    # print ("'۹' in ASCII number is:", ord('۹'))
    # ------------- Debugging ---------------


    from unidecode import unidecode



    import ply.lex as lex
    import re


    # By default, the lexer validates all rules against only
    # English characters. We can't have that, can we?
    lex._is_identifier = re.compile(r'.')

    # Regular expression rules for simple tokens
    t_PLUS          = r'\+'
    t_MINUS         = r'-'
    t_TIMES         = r'\*'
    t_DIVIDE        = r'/'
    t_LPAREN        = r'\('
    t_RPAREN        = r'\)'
    t_EQUALS        = r'=='
    t_ASSIGNMENT    = r'='


    # A regular expression rule with some action code
    def t_NUMBER(t):
        # ------------- Debugging ---------------
        # print ("The number was:", t.value)
        # ------------- Debugging ---------------
        

        if args["reverse"]:
            value_str = list(t.value)
            for i in range(0, len(value_str)):
                value_str[i] = reserved.get(value_str[i], value_str[i])
            t.value = ''.join(value_str)
        else:
            import olchikipython.filters.unidecoder as num_filter
            t.value = num_filter.filter(t.value)
        
        # ------------- Debugging ---------------
        # print ("The number is now:", t.value)
        # ------------- Debugging ---------------

        return t


    if args["reverse"]:
        t_NUMBER.__doc__ = r'[0-9][0-9]*[.]{0,1}[0-9]*'
    else:    
        t_NUMBER.__doc__ = r'['+language_dict["numbers"]["start"]+'-'+language_dict["numbers"]["end"]+']['+language_dict["numbers"]["start"]+'-'+language_dict["numbers"]["end"]+']*[.]{0,1}['+language_dict["numbers"]["start"]+'-'+language_dict["numbers"]["end"]+']*'

    # r'['+language_dict["letters"]["start"]+'-'+language_dict["letters"]["end"]+'_]['+language_dict["numbers"]["start"]+'-'+language_dict["numbers"]["end"]+'_'+language_dict["letters"]["start"]+'-'+language_dict["letters"]["end"]+']*'


    


    # List of token names.   This is always required
    tokens =  [
        "PLUS", 
        "MINUS",
        "TIMES",
        "DIVIDE",
        "LPAREN",
        "RPAREN",
        "EQUALS",
        "ASSIGNMENT",
        "NUMBER",
        "STRING",
        'ID',

        'newline',
        'COMMENT',
        # 'tab',

    ] + list(reserved.values())

    # Define a rule so we can track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        return t


    def t_ID(t):
        
        

        t.type = reserved.get(t.value,'ID')    # Check for reserved words    
        


        if args['translate']:
            if t.type == 'ID':
                t.value = unidecode(t.value)




        return t

    if args["reverse"]:
        t_ID.__doc__ = r'[a-zA-Z_][a-zA-Z_0-9]*'
    else:    
        t_ID.__doc__ = r'['+language_dict["letters"]["start"]+'-'+language_dict["letters"]["end"]+'_]['+language_dict["numbers"]["start"]+'-'+language_dict["numbers"]["end"]+'_'+language_dict["letters"]["start"]+'-'+language_dict["letters"]["end"]+']*'


    # A string containing ignored characters (spaces and tabs)
    # t_ignore  = ' \t'

    # Error handling rule
    def t_error(t):
        # ------------- Debugging ---------------
        # print("Illegal character '%s'" % t.value[0])
        # ------------- Debugging ---------------

        if args["reverse"] is False:
            t.value = unidecode(t.value[0])
        else:
            t.value = t.value[0]

        t.lexer.skip(1)


        # ------------- Debugging ---------------
        # print("Now becomes '%s'" % t.value[0])
        # print("still keeping it tho")
        # ------------- Debugging ---------------

        return t

    # Strings rule
    def t_STRING(t):
        # r'[\"][.][\"]'
        
        r'("(\\"|[^"])*")|(\'(\\\'|[^\'])*\')'

        # ------------- Debugging ---------------
        # print ("Found a string!", t.value)
        # ------------- Debugging ---------------

        return t

    # Comments rule
    def t_COMMENT(t):
        r'\#.*\n'

        # ------------- Debugging ---------------
        # print ("Found a comment!", t.value)
        # ------------- Debugging ---------------

        return t

    # Build the lexer
    lexer = lex.lex()

 

    dots_and_stuff = {
        "."  :    ".",
        ","  :    ",",
    }

    # ------------- Debugging ---------------
    # print ("normal:", dots_and_stuff)
    # ------------- Debugging ---------------

    if args["reverse"]:
        dots_and_stuff = {value:key for key, value in dots_and_stuff.items()}
        # ------------- Debugging ---------------
        # print ("Reversed:", dots_and_stuff)
        # ------------- Debugging ---------------

    for key, value in dots_and_stuff.items():
        code = code.replace(key, value)

    # ------------- Debugging ---------------
    # print ("Code is,\n", code)
    # ------------- Debugging ---------------

    lexer.input(code)

    if args["keep"] or args["keep_only"]:
        eng_pyfile = open("compiled.en.py", "wt")


    compiled_code = ""

    if args["keep_only"]:
        print ("Compiling", args["file"][0], "...")

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input

        # ------------- Debugging ---------------
        #print(tok)
        #print ("Tok's value is:", tok.value)
        #print ("Tok's type is:", tok.type)
        # ------------- Debugging ---------------



        if tok.value in reserved.keys():

            # ------------- Debugging ---------------
            # if tok.type == '۔':
            #     print ("Found an olchiki dot!")
            # ------------- Debugging ---------------
    
            # if args["reverse"] and tok.type == 'NUMBER':
            #     compiled_code += tok.value
            # else:
            compiled_code += tok.type
        else:
            compiled_code += tok.value


    if args["keep"] or args["keep_only"]:
        eng_pyfile.write(compiled_code)
        eng_pyfile.close()


    if args["return"] is True:
        return compiled_code

    elif args["keep_only"] is False:
        exec(compiled_code)