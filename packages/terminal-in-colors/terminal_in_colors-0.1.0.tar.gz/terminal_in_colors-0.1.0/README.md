# terminal-in-colors

Give color to your terminal, using 256 colors or RGB, use bold, italic, underline, among others, in a simple and uncomplicated way.


# Instalation

You can install simply using a command, thank *PyPi*.

```bash
$ pip install termina-in-colors
```

# Usage

```python
from terminal_in_color.ColorTerminal import ColorTerminal

string = "Hi"

c = ColorTerminal()

print(c.paint(string, color="red", blink="slow"))
```

# Methods Available

* `paint(string, color, bold, italic, underline, overline, doubleunderline, blink, background, opaque)` - Formats the string using the available options, returns a string.
* `find(color, exact)` - Searches by color name, integer, and returns list of matches, optionally, searches for exact matches or returns None.
* `clear()` - Clear the string formatting.
* `print_all()` - Print all 256 colors.`


# Documentation

-> **[https://kurotom.github.io/terminal_in_colors/](https://kurotom.github.io/terminal_in_colors/)**
