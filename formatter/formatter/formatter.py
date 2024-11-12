


# code by Twatwane ;) - ajosse@student.42.fr                      - November, 12th, 2024
#                     - https://github.com/Twatwane/42formatter

# list of collaborators : ChatGPT ^^

# use like this : "x42format <input_file(s)>"

"""
This code aims to format your input file to the standard of 42.

What will be done :
- Skip 42 header or Alert you if it's missing/invalid
- Replace "    " (4 spaces) by "    " TAB
- Fix variable declaration format
- Put space after flow control keywork                ->   "while(" becomes "while (" | "break;" becomes "break ;"
- Fix missing ";" at end of lines that needs one
- Fix strange spaces before and after pointer         ->   "type  *  var" -> "type\t*var"
- Fix merged spaces and tabs                          ->   "  \t "        ->  "\t"
- Fix spaces around operators                         ->   "1+1"          ->   "1 + 1"
- Remove useless empty lines
- Fix function declaration format
- Fix newline after closing brace : "}"

"""

import sys
import os
import re

# kw means keywords
# -- GLOBAL VARIABLES --   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
input_file_path = ""
content = ""
header = ""

types = [
    "int",           # Type entier standard
    "size_t",        # Type pour les tailles d'objets
    "long int",      # Entier long
    "short int",     # Entier court
    "char",          # Caractère
    "unsigned int",  # Entier non signé
    "unsigned long", # Entier long non signé
    "unsigned short",# Entier court non signé
    "unsigned char", # Caractère non signé
    "long long",     # Entier long long
    "unsigned long long", # Entier long long non signé
    "float",         # Nombre flottant
    "double",        # Double précision
    "long double",   # Double précision longue
    "void",          # Type vide (pour les fonctions sans retour)
    "struct",        # Structure (souvent utilisée dans les définitions)
    "union",         # Union (structure avec partage de mémoire)
    "enum",          # Énumération
    "bool",          # Booléen (C99+)
    "wchar_t",       # Type de caractère large (pour Unicode en C)
    "int8_t",        # Entier signé de 8 bits (depuis stdint.h)
    "int16_t",       # Entier signé de 16 bits
    "int32_t",       # Entier signé de 32 bits
    "int64_t",       # Entier signé de 64 bits
    "uint8_t",       # Entier non signé de 8 bits
    "uint16_t",      # Entier non signé de 16 bits
    "uint32_t",      # Entier non signé de 32 bits
    "uint64_t",      # Entier non signé de 64 bits
    "intptr_t",      # Entier signé capable de contenir un pointeur
    "uintptr_t",     # Entier non signé capable de contenir un pointeur
    "ptrdiff_t",     # Différence entre deux pointeurs
    "size_t",        # Taille d'un objet (en octets)
    "ssize_t",       # Taille signée (utilisé pour les tailles et retours d'erreur)
    "float_t",       # Flottant selon la précision de la plateforme
    "double_t",      # Double selon la précision de la plateforme
]
kw_types = []
kw_pointers = []

for type in types:
    kw_types.append(type)
    kw_pointers.append(f"{type} *")

kw_flow_control = [
    "if",          # Conditionnel
    "else",        # Sinon (alternative pour if)
    "switch",      # Structure de sélection multiple
    "case",        # Cas pour switch
    "default",     # Valeur par défaut dans switch
    "while",       # Boucle while
    "do",          # Boucle do-while
    "for",         # Boucle for
    "break",       # Quitter la boucle/switch
    "continue",    # Passer à l'itération suivante
    "return",      # Retourner une valeur d'une fonction
    "goto"         # Saut vers une étiquette (utilisé rarement)
]
kw_operators = [
    "sizeof",      # Taille d'un type/objet en octets
    "typedef",     # Alias de type
    "static",      # Déclaration de durée de vie étendue et portée interne
    "extern",      # Lien externe (utilisé pour déclarer des variables/fonctions externes)
    "inline",      # Indication de fonction en ligne
    "const",       # Constante (valeur immuable)
    "volatile",    # Indication pour optimisation minimale par le compilateur
    "restrict",    # Indique que le pointeur est non superposable (optimisation)
    "register",    # Indication pour stocker en registre (rarement utilisé)
]
operators = [
    "+",      # Addition
    "-",      # Soustraction
    "*",      # Multiplication
    "/",      # Division
    "%",      # Modulo
    "=",      # Assignation
    "+=",     # Addition avec assignation
    "-=",     # Soustraction avec assignation
    "*=",     # Multiplication avec assignation
    "/=",     # Division avec assignation
    "%=",     # Modulo avec assignation
    "==",     # Égalité
    "!=" ,    # Différence
    "<",      # Inférieur
    ">",      # Supérieur
    "<=",     # Inférieur ou égal
    ">=",     # Supérieur ou égal
    "&&",     # ET logique
    "||",     # OU logique
]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# memo
# content = re.sub(r' *\t+ *', '\t', content)
# * means 0 or many
# + means 1 or many

def skip_header():

    global input_file_path
    global content
    global header

    # Read file
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    # If 42 header
    if ( lines[0].startswith("/*") and (lines[10][-3:-1] == "*/") ):

        header_lines = lines[0:12]       # Keep header by side
        header = ''.join(header_lines)

        content_lines = lines[12:]         # Skip header
        content = ''.join(content_lines)
    
    else:
        print(f"Missing or Invalid 42 Header in : {input_file_path}, cannot process")
        sys.exit()


def replace_spaces_by_tab():

    global input_file_path
    global content
    global header

    # replace "    " (4 spaces) by "    " TAB
    content = content.replace('    ', '\t')


def make_result_file():

    global input_file_path
    global content
    global header

    file_name, file_extension = os.path.splitext(input_file_path)
    output_file_path = f"{file_name}_fixed{file_extension}"

    # create empty c file and put result in
    with open(f'{output_file_path}', 'w') as file:
        file.write(header)
        file.write(content)

    print(f"fixed   '{input_file_path}'  ->  '{output_file_path}'")


def fix_spaces_with_var_types():
    
    global input_file_path
    global content
    global header
    global kw_types

    for type in kw_types:
        content = re.sub(rf"\b{type} +", f"{type}\t", content)      # "int  var"     ->  "int\tvar"
        content = re.sub(rf"\b{type}\*", f"{type}\t*", content)     # "int*  var"    ->  "int\t*  var"
        content = re.sub(r"\*\s+", "*", content)                    # "int\t*  var"  ->  "int\tvar"
        content = re.sub(rf"{type}\(", f"{type} (", content)        # "int(thing *)" ->  "int (thing *)"
        

def space_after_kw_flow_control():

    global input_file_path
    global content
    global header
    global kw_flow_control

    for keyword in kw_flow_control:
        content = re.sub(rf"\b{keyword}\(", f"{keyword} (", content)
        content = re.sub(rf"\b{keyword};", f"{keyword} ;", content)


def fix_missing_semicolons():

    global content

    # Split content into lines
    lines = content.splitlines()
    fixed_lines = []
    
    # Expressions régulières pour les lignes qui devraient se terminer par un ";"
    semicolon_needed_pattern = re.compile(r"[^;\{\}]\s*$")  # Ligne ne se terminant pas par ; ou {
    exclude_pattern = re.compile(r"\b(if|for|while|switch|else)\b")  # Mots-clés de contrôle de flux
    function_declaration_pattern = re.compile(r"\)\s*$")  # Déclaration de fonction se terminant par )

    for line in lines:
        # Nettoyage des espaces en fin de ligne pour un traitement plus propre
        stripped_line = line.rstrip()
        
        # Vérifier si la ligne correspond au motif nécessitant un ;
        if (semicolon_needed_pattern.search(stripped_line) and not exclude_pattern.search(stripped_line) and not function_declaration_pattern.search(stripped_line)):
            # Ajouter un point-virgule si nécessaire
            fixed_lines.append(stripped_line + ";")
        else:
            # Garder la ligne intacte si elle n'a pas besoin de point-virgule
            fixed_lines.append(stripped_line)

    # join fixed content
    content = "\n".join(fixed_lines)


def merge_tab_spaces():

    global content

    content = re.sub(r' +\t+ +', '\t', content)
    content = re.sub(r'\t+ +', '\t', content)
    content = re.sub(r' +\t+', '\t', content)


def fix_function_declaration_spaces():

    global content
    global kw_types

    lines = content.splitlines()
    fixed_lines = []

    for index, line in enumerate(lines):

        match = 0
        for type in kw_types:
            if type in line and lines[index + 1] == "{":
                match = 1
                break

        newline = ""
        inside_parenthesis = 0

        if match:                               # if line matches pattern
            for x in range(len(line)):          # void	*memchr(const void	*ptr, int	value, size_t	num)
                
                c = line[x]
                if c == "(":
                    while not (c == ")" and x == len(line)):

                        #print(c, x == len(line))
                        c = line[x]
                        if c == '\t' or c == ' ':
                            newline = newline + ' '
                            while c == '\t' or c == ' ':
                                x += 1
                                c = line[x]

                        else:
                            newline = newline + c
                            x += 1
                    break

                else:
                    newline = newline + c

                #print("out")

            fixed_lines.append(newline)
                
        else:
            fixed_lines.append(line)
        
    # join fixed content
    content = "\n".join(fixed_lines)


def fix_function_declaration_format():

    global content
    global kw_types

    # Itérer sur chaque type et enlever les espaces entre le nom de fonction et la parenthèse ouvrante
    for type in kw_types:
        # Cherche "type funcname   (" et remplace par "type\tfuncname("
        pattern = rf"({type})\s+(\w+)\s+\("
        replacement = rf"\1\t\2("
        content = re.sub(pattern, replacement, content)

    content = re.sub(r'(\w+)\s+\(', r'\1(', content)
    fix_function_declaration_spaces()


def fix_spaces_around_operators():

    global content
    global kw_types
    global operators

    for operator in operators:

        pattern = rf"(\w+){re.escape(operator)}(\w+)"
        replacement = rf"\1 {operator} \2"
        content = re.sub(pattern, replacement, content)


def line_is_var_declaration(line):

    global kw_types

    for type in kw_types:
        if type in line and ";" in line and (not "=" in line):
            return True
        
    return False

def fix_var_declarations():

    global content
    global kw_types

    # Split content into lines
    lines = content.splitlines()
    fixed_lines = []
    temp_type = ""

    # ------ remove all empty lines ---- ↓ ------------------------------------------

    for index, line in enumerate(lines):
        for type in kw_types:
            if type in line:
                fixed_lines.append(line)
                temp_type = type
                break
        if line == "":

            if lines[index - 1] == "}":
                fixed_lines.append(line)

        elif not (temp_type in line):
            fixed_lines.append(line)

    # ------------ put empty line after last declaration -- ↓ ------------------------
    #"""
    lines = fixed_lines
    fixed_lines = []
    n = len(lines)
    i = 0

    for index, line in enumerate(lines):
        fixed_lines.append(line)

        if line_is_var_declaration(line):
            i = index + 1
            if line_is_var_declaration(lines[i]):
                pass
            else:
                fixed_lines.append("")

    #"""
    # ----------- fix variable alignment -- ↓ -------------------------------------------------------
    #"""
    lines = fixed_lines
    fixed_lines = []
    max_type_length = 0
    n = len(lines)
    i = 0
    to_skip = 0

    for index, line in enumerate(lines):

        if to_skip > 0:
            to_skip -= 1
            continue

        if line_is_var_declaration(line) and not line_is_var_declaration(lines[index - 1]):
            i = index

            # ---------------- find max length -- ↓ --------------------------
            while (i < n) and line_is_var_declaration(lines[i]):
                line_length = 0

                for letter in lines[i][1:]:
                    
                    if letter == "\t":
                        line_length += 4
                        break
                    else:
                        line_length += 1


                if line_length > max_type_length:
                    max_type_length = line_length

                i += 1
                to_skip += 1
            #print(max_type_length)

            #---------------- transform lines -- ↓ --------------------------
            i = index
            while (i < n) and line_is_var_declaration(lines[i]):
                line_length = 0

                for letter in lines[i][1:]:
                    
                    if letter == "\t":
                        line_length += 4
                        break
                    else:
                        line_length += 1

                while line_length < max_type_length:

                    words = lines[i].strip().split()  # cut line into words
                    first_word = words[0] if words else ""
                    rest = lines[i][len(first_word) + 1:]

                    #print(first_word)
                    #print(rest)

                    lines[i] = "\t" + first_word + "\t" + rest
                    line_length += 4

                i += 1
                
            i = index
            u = 0
            while (u < to_skip):
                fixed_lines.append(lines[i])
                i += 1
                u += 1
            fixed_lines.append("")
        

        else:
            fixed_lines.append(line)
    #"""
    # ----------- cleaned ;)) -----------------------------------------------------------------------

    # join fixed content
    content = "\n".join(fixed_lines)


def put_newline_after_brace():

    global content

    lines = content.splitlines()
    fixed_lines = []

    if lines[-1] != "":
        lines.append("")

    for index, line in enumerate(lines):

        if line == "}" and lines[index + 1] != "":
            fixed_lines.append(line)
            fixed_lines.append("")
        
        else:
            fixed_lines.append(line)

    # join fixed content
    content = "\n".join(fixed_lines)


def fix_cast_spaces():

    global content

    content = re.sub(r"\t\*\)", " *)", content)
        

def adjustments():

    global content
    global kw_types

    content = re.sub(r"unsigned\s+","unsigned ", content)

    for type in kw_types:
        content = re.sub(rf"{type}\(", f"{type} (", content)        # "int(thing *)" ->  "int (thing *)"



def normiser():

    global content

    #print(input_file_path)
    #"""
    try:

        skip_header()                           # skip or alert user if missing/invalid

        replace_spaces_by_tab()                 # "    "     -> "\t"
    
        fix_spaces_with_var_types()             # "int  var" -> "int\tvar"    and    "type  *  var" -> "type\t*var"
        
        fix_function_declaration_format()       # "funcname (void)"   ->   "funcname(void)" 

        space_after_kw_flow_control()           # "while("   -> "while ("

        fix_missing_semicolons()                # "a = 2"    -> "a = 2;"

        merge_tab_spaces()                      # "  \t "    -> "\t"

        fix_spaces_around_operators()           # "1+1"      ->   "1 + 1"

        fix_var_declarations()                  # too many things

        fix_cast_spaces()                       # assert "type = (char *)" and not "type = (char\t*)"

        put_newline_after_brace()               # }  \n

        adjustments()                           # "unsigned" or type casting problems fixing

        make_result_file()                      # "srcs/file.c"   ->  new "srcs/file_fixed.c"


    # Exceptions - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    except FileNotFoundError:
        print(f"Error : file '{input_file_path}' not found :/.")
    except Exception as e:
        print(f"Error : {e}")
    #"""



def main():
    global input_file_path
    # Check if an argument is provided
    if len(sys.argv) < 2:
        print("Usage: x42format <input_file(s)>")
    else:
        # Process
        for arg in sys.argv[1:]:
            input_file_path = arg
            normiser()

if __name__ == "__main__":
    main()
