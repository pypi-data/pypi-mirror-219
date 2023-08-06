from .handlers import *
from .widgets import *


def link(href: str) -> None: ...


# ------------------------------------------------------------------------#

###########################################################################
############################## WINDOWS CLASS ##############################
###########################################################################

# ------------------------------------------------------------------------#


class Window:
    def __init__(self, title: str, icon: str, size: tuple, geometry: tuple, 
                 style: str, fixed_size: tuple, frame: bool,
                 movable: bool, top: bool, spacing: int, content_margin: tuple,
                 move: tuple) -> None:
        '''
        :param title:
        :param icon:
        :param size:
        :param geometry:
        :param style:
        :param fixed_size:
        :param frame:
        :param movable:
        :param top:
        :param spacing:
        :param content_margin:
        :param move:
        '''
        ...
        
    def run(self, css: str): ...
    def quit(self): ...
    def update(self, remove_id: any, widget): ...
    def normal(self): ...
    def minimize(self): ...
    def maximize(self): ...
    def details(self) -> dict: ...
    def title(self, value: any | str): ...

    def _move(self, position: tuple, top: bool): ...


# ------------------------------------------------------------------------#

###########################################################################
############################# LAYOUT PROCESSOR ############################
###########################################################################

# ------------------------------------------------------------------------#


def Box(widgets) -> list: ...

def Grid(widgets) -> list: ...
    
class ScrollArea:
    def __init__(self, widgets, id: any, contain: bool):
        '''
        ScrollArea

        :param widgets:
        :param id:
        :param contain:
        '''
        ...

class scrollarea(ScrollArea): ...


class Stack:
    def __init__(self, widgets: list | Box | Grid | TabWidget, id: any,
                current_changed: function, widget_removed: function):
        '''
        Stack Widget

        :param widgets:
        :param id:
        :param current_changed:
        :param widget_removed:
        '''
        ...

    def set(self, index: int): ...

    def show(self, widget): ...

class stack(Stack): ...


# ------------------------------------------------------------------------#

###########################################################################
############################## CORE ELEMENTS ##############################
###########################################################################

# ------------------------------------------------------------------------#


class Menubar:
    def __init__(self, menu_items: list):
        '''
        Menu Bar

        :param menu_items:
        '''
        ...


class menubar(Menubar): ...


class Titlebar:
    def __init__(self, icon: str, title: str, widgets: list, alignment: str, text_color: str,
                 background_color: str, height: any, button_style: str):
        '''
        Titlebar

        :param title:
        :param widgets:
        :param alignment:
        :param text_color:
        :param background_color:
        :param height:
        :param button_style: square or circle
        '''
        ...
        

class titlebar(Titlebar): ...

class Toolbar:
    def __init__(self, name: str, tool_items: list, movable: bool,
                 position: str, id: any, iconsize: tuple,
                 border: bool, orientation: str, newline: bool):
        '''
        Toolbar Element

        :param name:
        :param tool_items:
        :param movable:
        :param position:
        :param id:
        :param iconsize:
        :param border:
        :param orientation:
        :param newline:
        '''
        ...
        

class toolbar(Toolbar): ...

class Statusbar:
    def __init__(self): ...

    def message(self, text: str, time: int | float):
        '''
        Display temporary status message

        :param text:
        :param time: in seconds.
        '''
        ...

    def clear(self): ...

    def add(self, widget, type: str): ...

    def remove(self, id: any): ...


class statusbar(Statusbar): ...


class File:
    def __init__(self): ...

    def open(self, caption: str, filter: str, directory: str, type: str) -> list:
        '''
        Open File Dialog

        :param caption:
        :param filter:
        :param directory:
        :param type:
        '''
        ...

    def save(self, filter: str = '(All Files: *)'):
        '''
        Save File Dialog

        :param filter:
        '''
        ...

class file(File): ...

class Folder:
    def __init__(self, caption: str, directory: str) -> str:
        '''
        Folder Dialog

        :param caption:
        :param directory:
        '''
        ...

class folder(Folder): ...

class Popup:
    def __init__(self, title: any, widgets: list, size: tuple, id: any,
                 modal: bool, frame: bool, lock: bool) -> list:
        '''
        Popup Window

        :param title:
        :param widgets:
        :param size:
        :param id:
        :param modal:
        :param frame:
        :param lock:
        '''
        ...

    def result(self): ...
    # has a return value

class popup(Popup): ...


class TabWidget:
    def __init__(self, tabs: tab | list, id: any, movable: bool, closable: bool,
                 close_requested: function, clicked: function) -> list:
        '''
        Tab Widget

        :param tabs:
        :param id:
        :param movable:
        :param closable:
        :param close_requested:
        :param clicked:
        '''
        ...

class tabwidget(TabWidget): ...

class Highlight:
    def __init__(self, id: any, synthax: dict): ...


class GET:
    def __init__(self, id: any):

        '''
        GET ELEMENT

        :param id:

        :method value:
        :method update:
        :method delete:
        :method append:
        :method html:
        :method insert_html:
        :method plain_text:
        :method alignment:
        :method is_default:
        :method is_readonly:
        :method style:
        :method is_checked:
        :method hidden:
        :method hide:
        :method diabled:
        :method disable:
        :method enable:
        :method is_hidden:
        :method is_disabled:
        :method select_all:
        :method copy:
        :method cut:
        :method undo:
        :method redo:
        :method paste:
        :method clear:
        :method add:
        :method remove:
        :method current:
        :method count:
        :method selected_items:
        :method set:
        :method index:
        :method reset:
        :method minimum:
        :method maximum:
        :method is_text_visible:
        :method reject:
        :method accept:
        :method focus:
        :method cursor:
        :method setcursor:
        :method icon:
        :method show:
        :method scrollbar:
        '''

        ...
        
    def __repr__(self) -> str: ...

    def value(self, value: str): ...
    def update(self, widget): ...
    def delete(self): ...
    def append(self, value: str): ...
    def html(self, value: str): ...
    def insert_html(self, value: str): ...
    def plain_text(self, value: str | int) -> str: ...
    def alignment(self, value: str) -> str: ...
    def is_default(self) -> bool: ...
    def is_readonly(self) -> bool: ...
    def style(self, css: str, reset: bool): ...
    def is_checked(self) -> bool: ...
    def hidden(self, value: bool): ...
    def hide(self): ...
    def disabled(self, value: bool): ...
    def disable(self): ...
    def enable(self): ...
    def is_hidden(self) -> bool: ...
    def is_disabled(self) -> bool: ...
    def select_all(self): ...
    def copy(self): ...
    def cut(self): ...
    def undo(self): ...
    def redo(self): ...
    def paste(self): ...
    def clear(self): ...
    def add(self, items): ...
    def remove(self, items): ...
    def current(self) -> str | int: ...
    def count(self) -> int: ...
    def selected_items(self) -> list: ...
    def set(self, value): ...
    def index(self) -> int: ...
    def reset(self): ...
    def minimum(self) -> int: ...
    def maximum(self) -> int: ...
    def is_text_visible(self) -> bool: ...
    def reject(self, result: int): ...
    def accept(self, result: int): ...
    def focus(self, value: bool): ...
    def has_focus(self, value: bool) -> bool: ...
    def cursor(self) -> tuple: ...
    def setcursor(self, cursor: tuple): ...
    def icon(self, path: str): ...
    def show(self, widget): ...
    def scrollbar(self, scrollbar, bar_type: str, id: any): ...

class get(GET): ...

# ------------------------------------------------------------------------#

###########################################################################
############################## EASE OF ACCESS #############################
###########################################################################

# ------------------------------------------------------------------------#


class Exit(Button):
    def __init__(self, label: str, icon: str, id: any, disabled: bool, default: bool,
                 grid: tuple, sizePolicy: tuple, checkable: bool, checked: bool, hidden: bool, 
                 focus: bool, icon_size: int, statustip: any | str, tooltip: any | str, shortcut: str):
        ...

class exit(Exit): ...

class Copy(Button):
    def __init__(self, Target_ID: any, button_text: str, icon: str, id: any, 
                 disabled: bool, default: bool, grid: tuple, sizePolicy: tuple, 
                 checked: bool, hidden: bool, focus: bool, icon_size: int, 
                 statustip: any | str, tooltip: any | str, shortcut: str):
        ...

class copy(Copy): ...

class Cut(Button):
    def __init__(self, Target_ID: any, button_text: str, icon: str, id: any, 
                 disabled: bool, default: bool, grid: tuple, sizePolicy: tuple, 
                 checked: bool, hidden: bool, focus: bool, icon_size: int, 
                 statustip: any | str, tooltip: any | str, shortcut: str):
        ...

class cut(Cut): ...

class Paste(Button):
    def __init__(self, Target_ID: any, button_text: str, icon: str, id: any, 
                 disabled: bool, default: bool, grid: tuple, sizePolicy: tuple, 
                 checked: bool, hidden: bool, focus: bool, icon_size: int, 
                 statustip: any | str, tooltip: any | str, shortcut: str):
        ...

class paste(Paste): ...

class Undo(Button):
    def __init__(self, Target_ID: any, button_text: str, icon: str, id: any, 
                 disabled: bool, default: bool, grid: tuple, sizePolicy: tuple, 
                 checked: bool, hidden: bool, focus: bool, icon_size: int, 
                 statustip: any | str, tooltip: any | str, shortcut: str):
        ...

class undo(Undo): ...

class Redo(Button):
    def __init__(self, Target_ID: any, button_text: str, icon: str, id: any, 
                 disabled: bool, default: bool, grid: tuple, sizePolicy: tuple, 
                 checked: bool, hidden: bool, focus: bool, icon_size: int, 
                 statustip: any | str, tooltip: any | str, shortcut: str):
        ...

class redo(Redo): ...

# ------------------------------------------------------------------------#

###########################################################################
############################## CONTROL BUTTONS ############################
###########################################################################

# ------------------------------------------------------------------------#


def minimize() -> GET: ...
def maximize() -> GET: ...
def close() -> GET: ...
def title() -> GET: ...
