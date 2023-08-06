from .handlers import *

def Column(widgets) -> list: ...

def column(widgets) -> Column: ...

def item(label: any, func: function, icon: str, tooltip: any | str, 
         statustip: any | str, shortcut: str) -> list: ...

def tab(layout, name: str, icon: str) -> list: ...
def option(value: any, icon: str) -> list: ...
def ListItem(label: any, icon: str) -> list: ...
def separator() -> list: ...
def empty() -> list: ...
def fieldset(label: any | str, widgets: list, id: str, orientation: str) -> list: ...
def Group(widgets: list, orientation: str) -> list: ...
def group(widgets: list, orientation: str) -> list: ...

class Button:
    def __init__(self, value: any, func: function, icon: str, id: any, disabled: bool, 
                 default: bool, grid: tuple, sizepolicy: tuple, checkable: bool,
                 checked: bool, hidden: bool, focus: bool, icon_size: int, 
                 statustip: any | str, tooltip: any | str, shortcut: str):
        '''
        Button Widget

        :param value:
        :param func:
        :param icon:
        :param id:
        :param disabled:
        :param default:
        :param grid:
        :param sizepolicy:
        :param checkable:
        :param checked:
        :param hidden:
        :param focus:
        :param icon_size:
        :param statustip:
        :param tooltip:
        :param shortcut:
        '''
        ...

class button(Button): ...

class Input:
    def __init__(self, placeholder: any, id: any, value: any,
                 type: str, disabled: bool, readonly: bool,
                 maxlength: int, hidden: bool, font: str,
                 fontsize: int, text_changed: function, return_pressed: function,
                 editing_finished: function, text_edited: function,
                 selection_changed: function, sizepolicy: tuple, grid: tuple):
        '''
        Input Widget

        :param placeholder:
        :param id:
        :param value:
        :param type:
        :param diabled:
        :param readonly:
        :param maxlength:
        :param hidden:
        :param font:
        :param fontsize:
        :param text_changed:
        :param return_pressed:
        :param editing_finished:
        :param text_edited:
        :param selection_changed:
        :param sizepolicy:
        :param grid:
        '''
        ...

class input(Input): ...

class Text:
    def __init__(self, value: any, id: any, link: str,
                 hovered: function, clicked: function, buddy: str, alignment: str,
                 wordwrap: bool, grid: tuple,
                 sizepolicy: tuple, hidden: bool):
        '''
        Text Widget

        :param value:
        :param id:
        :param link:
        :param hovered:
        :param clicked:
        :param buddy:
        :param alignment:
        :param wordwrap:
        :param grid:
        :param sizepolicy:
        :param hidden:
        '''

        ...
        
class text(Text): ...

class Image:
    def __init__(self, source: str, id: any, size: int, alignment: str, grid: tuple,
                 sizepolicy: tuple, hidden: bool):
        '''
        Image Widget

        :param source:
        :param id:
        :param size:
        :param alignment:
        :param grid:
        :param sizePolicy:
        :param hidden:
        '''

        ...

class image(Image): ...

class CheckBox:
    def __init__(self, label: any, checked: bool, id: any,
                 state_changed: function, toggled: function, grid: tuple,
                 sizepolicy: tuple):
        '''
        Checkbox Widget

        :param label:
        :param checked:
        :param id:
        :param state_changed:
        :param toggled:
        :param grid:
        :param sizepolicy:
        '''
        ...

class checkbox(CheckBox): ...

class RadioButton:
    def __init__(self, label: any, checked: bool, id: any,
                 toggled: function, grid: tuple,
                 sizepolicy: tuple):
        '''
        RadioButton Widget

        :param label:
        :param checked:
        :param id:
        :param stateChanged:
        :param toggled:
        :param grid:
        :param sizepolicy:
        '''
        ...

class radiobutton(RadioButton): ...

class Textarea:
    def __init__(self, id: any, placeholder: any,
                 hidden: bool, alignment: str, value: any,
                 disabled: bool, readonly: bool, text_changed: function,
                 selection_changed: function, undo_available: function,
                 redo_available: function, maxlength: int, font: str,
                 fontsize: int, sizepolicy: tuple,
                 grid: tuple, tabwidth: int,
                 wordwrap: bool):
        '''
        Textarea Widget

        :param id:
        :param placeholder
        :param hidden:
        :param alignment:
        :param value;
        :param disabled:
        :param readonly:
        :param text_changed:
        :param selection_changed:
        :param undo_available:
        :param redo_available:
        :param maxlegth:
        :param font:
        :param fontsize:
        :param sizepolicy:
        :param grid:
        :param tabwidth:
        :param wordwrap:
        '''
        ...
class textarea(Textarea): ...

class ListWidget:
    def __init__(self, list_items: any, id: any, mode: str, grid: tuple,
                 sizepolicy: tuple, func: function):
        '''
        List Widget

        :param list_items:
        :param id:
        :param mode:
        :param grid:
        :param sizepolicy:
        :param func:
        '''
        ...

class listwidget(ListWidget): ...

class Select:
    def __init__(self, options: list, id: any, placeholder: any, grid: tuple,
                 sizepolicy: tuple, current_text_changed: function, activated: function):
        '''
        Select Widget

        :param options:
        :param id:
        :param placeholder:
        :param grid:
        :param sizepolicy:
        :param current_text_changed:
        :param activated:
        '''

        ...

class select(Select): ...

class ProgressBar:
    def __init__(self, id: any,  min: int, max: int, value: int, orientation: str, 
                 grid: tuple, sizepolicy: tuple, text_visible: bool, inverted: bool,
                 value_changed: function):
        '''
        ProgressBar Widget

        :param id:
        :param min:
        :param max:
        :param value:
        :param orientation:
        :param grid:
        :param sizepolicy:
        :param text_visible:
        :param inverted:
        :param value_changed:
        '''
        ...

class progressbar(ProgressBar): ...

class Slider:
    def __init__(self, id: any, min: int, max: int, value: int,
                 step: int, orientation: str, grid: tuple,
                 sizepolicy: tuple, value_changed: function):
        '''
        Slider Widget

        :param id:
        :param min:
        :param max:
        :param value:
        :param step:
        :param orientation:
        :param grid:
        :param sizepolicy:
        :param value_changed:
        '''
        ...

class slider(Slider): ...

class Dial:
    def __init__(self, id: any, min: int, max: int, value: int,
                 tick_target: str, tick: bool, wrapping: bool, grid: tuple,
                 sizepolicy: tuple, value_changed: function):
        '''
        Dial Widget

        :param id:
        :param min:
        :param max:
        :param value:
        :param tick_target:
        :param tick:
        :param wrapping:
        :param grid:
        :param sizepolicy:
        :param value_changed:
        '''
        ...

class dial(Dial): ...