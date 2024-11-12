
---

# 42 ".c" Code Formatter

This tool automatically formats your C code to comply with the 42 norm.

## Installation

To install the package, you can use either of the following methods:

### With `pip`:

```
pip install 42formatter
```

### Or with `pipx` (recommended for isolated environments):

```
pipx install 42formatter
```

### Why `pipx`?
`pipx` is recommended if you want to install the tool in an isolated environment, avoiding conflicts with other Python packages.

## How to Use

Run the following command to format your C file(s):

```
x42format <input_file(s)>
```

## Features

- Skip 42 header or Alert you if it's missing/invalid
- Replace "    " (4 spaces) by "    " TAB
- Fix variable declaration format
- Put space after flow control keywork       ->   "while(" becomes "while (" | "break;" becomes "break ;"
- Fix missing ";" at end of lines that needs one
- Fix strange spaces before and after pointer         ->   "type  *  var" -> "type\t*var"
- Fix merged spaces and tabs                          ->   "  \t "        ->  "\t"
- Fix spaces around operators                         ->   "1+1"          ->   "1 + 1"
- Remove useless empty lines
- Fix function declaration format
- Fix newline after closing brace : "}"
- Fix strange spaces around type casting

## License

This project is under a **Proprietary License**.  
All rights are reserved. The project remains the property of Antoine Josse.  
Any modifications or contributions to the project require prior permission from the author (contact at [ajosse@student.42.fr](mailto:ajosse@student.42.fr)).  
Redistribution under a different name is not allowed.  
The project must always be attributed to the original author.

## Contributing

If you have any suggestions for improvements, feel free to contact me at [ajosse@student.42.fr](mailto:ajosse@student.42.fr).

---

This tool is here to save you time while battling with Norminette.

Antoine :)

---
