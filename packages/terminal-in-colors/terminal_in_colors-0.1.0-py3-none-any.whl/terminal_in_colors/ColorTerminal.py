from terminal_in_colors.info_colors import ansi_colors

from typing import Union


class ColorTerminal(object):
    """Class that provides methods to create formatted, colored sentences.

    Allows the use of ANSI and RGB colors in terminal, using numbers,
    color name, or list of integers to use RGB.

    Once the class is initialized, it allows to use the methods:

    - `paint(string, color, bold, italic, underline, strikethrough,\
     doubleunderline, blink, background, opaque)` - Formats the string using\
      the available options, returns a string.
    - `find(color, exact)` - Searches by color name, integer, and returns list\
     of matches, optionally, searches for exact matches or returns None.
    - `clear()` - Clear the string formatting.
    - `print_all()` - Print all 256 colors.
    """

    def __init__(self):
        """Constructor"""
        self.__neutro = '\033[0;0m'
        self.__bold = '\033[1;1m'
        self.__opaque = '\033[2;2m'
        self.__italic = '\033[3;3m'
        self.__underline = '\033[4;4m'
        self.__intermitent_slow = '\033[5;5m'
        self.__intermitent_rapid = '\033[6;6m'
        self.__strikethrough = '\033[9;9m'
        self.__doubleunderline = '\033[21;21m'
        self.__base_ansi = '\x1b[38;5;_m'
        self.__base_rbg_fg = '\x1b[38;2;R;G;Bm'
        self.__base_rbg_bg = '\x1b[48;2;R;G;Bm'

    def paint(
            self,
            string: str,
            color: Union[list, str, int] = None,
            bold: bool = False,
            italic: bool = False,
            underline: bool = False,
            strikethrough: bool = False,
            doubleunderline: bool = False,
            blink: str = False,
            background: Union[list, str, int] = None,
            opaque: bool = False,
            ) -> str:
        """Styles the phrase as indicated and returns it.

        Args:
            string  (str)   :   string to add format.
            color   (list|str|int)  :   represent a color could be a list\
             [R, G, B] of int, string, or integer.
            bold    (bool)  :   enable bold.
            italic  (bool)  :   enable italic.
            underline   (bool)    :  enable underline.
            strikethrough    (bool)  :   enable strikethrough.
            doubleunderline     (bool)  :    enable double underline.
            blink   (str)   :   set blink slow (recomended) or rapid\
             (could not work).
            background  (list|str|int)  :   set background color, could be a\
             list [R, G, B] of int, string, or integer.
            opaque  (bool)  :   the color of text is less intense.

        Returns:
            str :   string formatted by options enter.
        """
        frase = ''
        if color is None:
            frase += self.__neutro
        else:
            type_color = type(color)
            if type_color is list:
                if len(color) == 3:
                    # frase += self.__set_rgb(color)
                    range_rgb = [0 <= i < 256 for i in color]
                    if all(range_rgb):
                        frase += self.__set_rgb(color, background=False)
                    else:
                        string_warn = "Integers must be between 0 to 255."
                        msg = self.__error_msg(string_warn)
                        raise ValueError(msg)
                else:
                    msg = self.__error_msg("Must be a list of 3 integers.")
                    raise ValueError(msg)
            else:
                frase += self.__set_color(color)

        if background is not None:
            frase += self.__set_bg(background)

        if bold:
            frase += self.__bold
        if italic:
            frase += self.__italic
        if underline:
            frase += self.__underline
        if strikethrough:
            frase += self.__strikethrough
        if doubleunderline:
            frase += self.__doubleunderline
        if blink is not None:
            if str(blink) == "slow":
                frase += self.__intermitent_slow
            elif str(blink) == "rapid":
                frase += self.__intermitent_rapid
        if opaque:
            frase += self.__opaque

        return frase + string + self.__neutro

    def clear(self) -> str:
        """Clear all formats.

        Returns
            str :   string without color to apply on message to clean color\
            format.
        """
        return self.__neutro

    def print_all(self) -> str:
        """Print all 256 colors combinations."""
        msg = f'\n\tTerminal_in_Colors - {len(ansi_colors)} colors\n'
        print(self.paint(string=msg, bold=True, underline=True))
        format_msg = ""
        for i in range(0, 256):
            format_msg += f'\x1b[38;5;{i}m' + 'Hi' + self.__neutro + " "
            if i % 20 == 0:
                format_msg += "\n"
        print(format_msg)

    def __set_color(self, color: str | int) -> str:
        """Sets the color, must be a string, integer, or list of integers for\
        RGB.

        Args:
            color (str|int) : sets the color using the string (name) or\
            integer of the color.

        Returns:
            str : returns the color string to apply in the message.
        """
        base = self.__base_ansi
        type_color = type(color)
        if type_color is str:
            color = self.__exact_scan(color)
            if color is None:
                return ""
            else:
                return base.replace("_", str(color[0][0]))

        elif type_color is int:
            return base.replace("_", str(color))

    def __set_rgb(self, list_code: list[int], background: bool = False) -> str:
        """Set color using RGB.

        Args:
            list_code   (list[int])   :   set RGB color using list of 3\
             integers.
            background  (bool)  :   False (default), set this color is to\
             background.

        Returns:
            str :   return string formatted to color RGB.
        """
        if background:
            rgb = self.__base_rbg_bg
        else:
            rgb = self.__base_rbg_fg
        keys = ["R", "G", "B"]
        dict_rbg = dict(zip(keys, list_code))
        for k, v in dict_rbg.items():
            rgb = rgb.replace(k, str(v))
        return rgb

    def __set_bg(self, color: str | int | list[int] = None) -> str:
        """Set background color.

        Args:
            color   (str|int|list[int]) :   set background color using string\
             (search for exact color if no exists return background without\
              color), integer or list of integer RGB.

        Returns:
            str :   return string background formatted.
        """
        if color is not None:
            tipo = type(color)
            if tipo is list:
                if len(color) == 3:
                    range_rgb = [0 <= i < 256 for i in color]
                    if all(range_rgb):
                        return self.__set_rgb(color, background=True)
                    else:
                        string_warn = "Integers must be between 0 to 255."
                        msg = self.__error_msg(string_warn)
                        raise ValueError(msg)
                else:
                    msg = self.__error_msg("Must be a list of 3 integers.")
                    raise ValueError(msg)
            elif tipo is int:
                return f'\x1b[48;5;{color}m'
            elif tipo is str:
                clr = self.__exact_scan(color)
                if clr is None:
                    clr = self.__neutro
                else:
                    clr = clr[0][0]
                return f'\x1b[48;5;{clr}m'

    def find(self, color: str, exact: bool = False) -> list | None:
        """Search for color using a string or integer, and return a list of\
         tuples of all matches.
        Optional, exact search by string.

        Args:
            color   (str|int)  :    color for search, must be sting or integer.
            exact   (bool)  :   boolean, set search exactly for color enter,\
             if not matches color return None.

        Returns:
            list | None :   return list of tuples with color matches (integer\
             and name of color) or None.
        """
        r = None
        if type(color) is str:
            if exact:
                r = self.__exact_scan(color)
                if r is None:
                    return None
                else:
                    return r
            else:
                r = [
                        (k, v) for (k, v) in ansi_colors.items()
                        if color.lower() in v.lower()
                    ]
        elif type(color) is int:
            r = [
                    (k, v) for (k, v) in ansi_colors.items()
                    if k == color
                ]
        return r

    def __exact_scan(self, color: str) -> str | None:
        """Find the exact color using a string.

        Args:
            color   (str)   :   search using string passed.

        Returns:
            list | None :   return list with a tuple with integer and name of\
             color matches exactly or return None.
        """
        result = [
                (k, v) for (k, v) in ansi_colors.items()
                if color.lower() == v.lower()
            ]
        if len(result) == 0:
            return None
        else:
            return result

    def __error_msg(self, message: str) -> str:
        """Formatted error message.

        Args:
            message (str) : string of the message to be formed.

        Returns:
            str : return string formatted with the message entered.
        """
        return self.paint(
                    string=message,
                    color="red",
                    bold=True,
                    underline=True,
                    doubleunderline=True
                )
