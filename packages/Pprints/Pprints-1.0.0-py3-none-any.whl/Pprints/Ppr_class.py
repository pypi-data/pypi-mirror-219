import os, colorama
from typing import overload
from ColorTER import *
import arabic_reshaper
from bidi.algorithm import get_display

__version__ = ['1.0.0']

pprint = ''

# Colors Print
RED            = colorama.Fore.RED
GREEN            = colorama.Fore.GREEN
RESET            = colorama.Fore.RESET
BLUE            = colorama.Fore.BLUE
YELLOW            = colorama.Fore.YELLOW
CYAN            = colorama.Fore.CYAN
MAGENTA            = colorama.Fore.MAGENTA
BLACK            = colorama.Fore.BLACK
WHITE            = colorama.Fore.WHITE

try:

    class _Fnc:
        def __init__(self, color) -> None:
            self.color = color
            global pprint
            if 'print_access_request_library_PPrint' not in os.environ:
                os.environ['print_access_request_library_PPrint'] = pprint
            if os.environ['print_access_request_library_Pprint'] == '0':
                Print.printY(f'You are using Pprint library :')
                Print.printM(f'\t version: {__version__[0]} (:')
                Print.printB(f'You are sending a request to this IP: \"{self.url}\"')
            
        @overload
        def print(self, text: str) -> None: ...

        def print(self, text: str) -> None:
            reshaped_text = arabic_reshaper.reshape(u'{0}'.format(text))
            bidi_text = get_display(reshaped_text)
            print(self.color + bidi_text + RESET)

    class Pprint(_Fnc):
        def __init__(self, color: any = WHITE):
            self.color = color
            super().__init__(color)

        def print(self, text: str) -> None:
            translation_table = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
            super().print(text.translate(translation_table))
            
except Exception as e:
    
    Print.printY("Libray Pprint Error !")