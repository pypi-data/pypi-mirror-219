import os.path as path

from clera import *
from configparser import ConfigParser

def editor():
    DEFAULT_CONFIG = ConfigParser()

    DEFAULT_CONFIG['MAIN'] = {
        'font_family' : "monospace",
        'size' : '16',
    }


    DIR_NAME = f'{path.dirname(__file__)}'

    def init_config_file():
        if path.isfile(f'{DIR_NAME}/config.ini') == False:
            with open(f'{DIR_NAME}/config.ini', 'w') as config_file:
                DEFAULT_CONFIG.write(config_file)

    init_config_file()

    class Settings:
        def __init__(self, filename):
            self.config = ConfigParser()
            self.filename = filename
            self.config_dict = dict()

        def scan(self):
            self.config.read(self.filename)

            for section in self.config.sections():
                self.config_dict[section] = dict(self.config.items(section))


        def get(self, name):
            self.scan()
            section = self.config_dict[name]

            self.make_python(section)        
            
            return section
        
        def add(self):
            return self.config

        
        def update(self):
            for KEY in self.config_dict:
                VALUE = self.config_dict[KEY]
                self.make_config(VALUE)

                self.config[KEY] = VALUE

                with open(self.filename, 'w') as file:
                    self.config.write(file)

        def make_python(self, section):
            for KEY in section:
                VALUE = section[KEY]
                if VALUE == 'True':
                    section[KEY] = True
                elif VALUE == 'False':
                    section[KEY] = False
                elif VALUE == 'None':
                    section[KEY] = None
        
        def make_config(self, section):
            for KEY in section:
                VALUE = section[KEY]
                if VALUE == None:
                    section[KEY] = 'None'

    SETTINGS = Settings(f"{DIR_NAME}/config.ini")
    MAIN = SETTINGS.get("MAIN")



    # Automatic indention
    lines = [0]
    def make_line_width():
        line_width = '40px'

        if int(MAIN['size']) > 16:
            line_width = '55px'
        elif int(MAIN['size']) > 14:
            line_width = '45px'

        return line_width

    def set_line_number(line_widget, text_widget):
        # area = GET('line')
        line_widget.value(''.join([
            f'{line + 1}\n' 
            for line in range(
                len(str(text_widget).split('\n'))
                )
            ]).removesuffix('\n'))
        line_widget.select_all()
        line_widget.alignment('right')
        line_widget.setcursor(line_widget.cursor())

        if len(str(text_widget).split('\n')) >= 10000:
            line_widget.style('max-width: 65px')
        elif len(str(text_widget).split('\n')) >= 1000:
            line_widget.style('max-width: 55px')
        else:
            line_widget.style(f'max-width: {make_line_width()}')

            

    def auto_indent():
        txt = GET('txt')
        txt_value = str(txt).split('\n')

        line = lines[0]
        curr_line = len(txt_value)
        def tab(n: None = None):
            c, p = txt.cursor()

            first = str(txt)[:p]
            last = str(txt)[p:]

            txt_value = first.split('\n')
            
            if n == 'add':
                txt_value[-1] += '}'
            else:
                txt_value[-1] = '\t'
                p += len('\t')


            last = last.split('\n')

            if last[0] == '':
                last.pop(0)

            if n == 'close':
                txt_value.append('}')
            
            txt_value += last
            
            # if txt_value[-1] == '':
            #     txt_value.pop(-1)
            
            txt_value = '\n'.join(txt_value)
            value = txt_value
            
            cursor = c, p

            txt.value(value)

            txt.setcursor(cursor)

        
        ln = txt_value[-1]
        c, p = txt.cursor()

        if str(txt)[:p].split('\n')[-1] == '':
            if line < curr_line:
                end = str(txt)[:p].strip()

                try:
                    end = end[-1].split()[0]
                except:
                    ...

                if  end == ';':
                    tab()
                elif end == '{':
                    try:
                        after = str(txt)[p:].strip()[0]
                    except:
                        after = None

                        if after != '}':
                            tab('close')
                
                lines[0] = curr_line
            else:
                lines[0] = 0

        elif ln == '\t}':
            txt_value[-1] = txt_value[-1].replace('\t', '')
            txt_value = '\n'.join(txt_value)
            cursor, postion = txt.cursor()
            postion -= len('\t')
            cursor = cursor, postion
            txt.value(txt_value)

            txt.setcursor(cursor)
        else:
            ...

        line_w = GET('line')
        txt_w = GET('txt')
        

        if len(str(line_w).split('\n')) < len(str(txt_w).split('\n')) or len(str(line_w).split('\n')) > len(str(txt_w).split('\n')):
            set_line_number(line_w, txt)

    #interface
    window = Window(content_margin=0, frame=False, movable=True, fixed_size=(420, 270), spacing=0)
    line_width = make_line_width()

    settings_styling = f'''
        font-size: {MAIN['size']}px;
        font-family: {MAIN['font_family']};
    '''
    win_color = 'rgb(19, 19, 19)'
    txt_color = 'rgb(23, 23, 23)'
    css = f'''
    window [
        background: {win_color};
    ]

    button [
        color: white;
        border: 0px solid;
        padding: 3px 2px;
    ]

    select [
        height: 25px;
    ]

    button:hover [
        background: rgba(131, 130, 130, 0.5);
        border-radius: 5px;
    ]

    scrollbar:vertical [
        background: rgba(0, 0, 0, 0);
        width: 15px;
        margin: 0;
        max-width: 5px;
    ]

    scrollbar::handle:vertical [
        background: gray;   
    ]

    scrollbar::add-line:vertical [
        height: 0px;
    ]

    scrollbar::sub-line:vertical [
        height: 0px;
    ]

    popup [
        color: white;
        background: {win_color};
    ]

    line [
        max-width: {line_width};
        border: 0px solid;
        background: rgb(19, 19, 19);
        color: rgb(131, 130, 130);
        {settings_styling}
    ]

    txt [
        color: white;
        {settings_styling}
        background: {txt_color};
        border: 0px;
    ]

    scrollbar:horizontal [
        background: rgba(0, 0, 0, 0);
        margin: 0;
        max-height: 5px;
    ]

    scrollbar::handle:horizontal [
        background: gray;   
    ]

    scrollbar::add-line:horizontal [
        height: 0px;
    ]

    scrollbar::sub-line:horizontal [
        height: 0px;
    ]
    '''
    # line {
    #     max-width: 65px;
    #     border: 0px solid;
    #     background: rgb(19, 19, 19);
    #     color: rgb(131, 130, 130);
    # }


    POPUP_STYLING = '''
    button { 
        padding: 5px 20px 8px 20px; 
        background: rgba(131, 130, 130, 0.5); 
        border-radius: 5px;
    } 

    button:hover {
        background: rgba(131, 130, 130, 1); 
        border-radius: 5px;
    }'''



    allow = '(Clera Style: *.cx)'


    editor_state = [False]
    file_path = [None]




    def handle(action):
        textarea = GET('txt')

        def save_as():
            file, format = File.save(filter=allow)
            file_path[0] = file
            if file.strip().endswith('cx'):
                ...
            else:
                file = f'{file.strip()}.cx'

            if len(file.removesuffix('.cx')) != 0:
                with open(file, 'w') as file:
                    file.write(str(textarea))
                    editor_state[0] = False
                    GET('line').style('border-right: 0px;')
                    return True
            else:
                return False


        def handle_open():
            file, format = File.open(filter=allow)
            file_path[0] = file

            
            with open(file, 'r') as file:
                file = file.read()
                textarea.value(file)
                editor_state[0] = False
                GET('line').style('border-right: 0px;')

        
        
        def make_new():
            file_path[0] = None
            textarea.clear()
            editor_state[0] = False
            GET('line').style('border-right: 0px;')


        def unsaved(action):
            def cancel():
                GET('warning-popup').delete()

            def dont_save():
                cancel()

                if action == 'open':
                    handle_open()
                elif action == 'new':
                    make_new()
                elif action == 'exit':
                    window.quit()

            def save():
                cancel()
                query = handle_save()
                
                if query == True:
                    if action == 'open':
                        handle_open()
                    elif action == 'new':
                        make_new()
                    elif action == 'exit':
                        window.quit()
                else:
                    if action == 'open':
                        handle_open()
                    elif action == 'exit':
                        window.quit()

            warning = [
                [Text('Do you want to Save Document?', id='save-msg')],
                [Button('Save', save, id='popup-save'), Button("Don't Save", dont_save, id='popup-d-save'), Button('Cancel', cancel,id='popup-cancel', shortcut='Esc')]
            ]

            Popup('Notification', warning, modal=True, id='warning-popup', lock=True)
            GET('popup-save').style(POPUP_STYLING)
            GET('popup-d-save').style(POPUP_STYLING)
            GET('popup-cancel').style(POPUP_STYLING)
            GET('save-msg').style('color: white;')


        
        def handle_save():
            if file_path[0] != None and len(file_path[0])  != 0:
                with open(file_path[0], 'w') as file:
                    file.write(str(textarea))
                    editor_state[0] = False
                    GET('line').style('border-right: 0px;')
            else:
                save_as()
            

        if action == 'open':
            if editor_state[0] == True:
                unsaved('open')
            else:
                handle_open()
        elif action == 'save':
            handle_save()
        elif action  == 'save_as':
            save_as()
        elif action == 'new':
            if editor_state[0] == True:
                unsaved('new')
            else:
                make_new()

            
            GET('txt').focus()
        elif action == 'exit':
            if editor_state[0] == True:
                unsaved('exit')
            else:
                window.quit()
        else:
            ...

        GET('txt').focus()
        
        


    def changed():
        auto_indent()

        if editor_state[0] == False:
            editor_state[0] = True
            GET('line').style('border-right: 1px solid gray;')
        else:
            ...

    # end

    state = ['on']

    def switch():
        current_state = state[0]
        _switch = GET('switch')
        _textarea = GET('txt')

        if current_state == 'on':
            _switch.icon(f'{DIR_NAME}/../icons/off.png')
            state[0] = 'off'
            _textarea.disable()
        elif current_state == 'off':
            _switch.icon(f'{DIR_NAME}/../icons/on.png')
            state[0] = 'on'
            _textarea.enable()

    def settings():
        def pop_action(action):
            popup = GET('settings')

            if action == 'cancel':
                popup.delete()
                GET('txt').focus()

            elif action == 'apply':
                size_value = GET('-size-').current()
                font = GET('font').current()

                MAIN['size'] = size_value
                MAIN['font_family'] = font
                SETTINGS.update()

                settings_styling = f'''
                    font-size: {MAIN['size']}px;
                    font-family: {MAIN['font_family']};
                '''

                GET('line').style(f'{settings_styling};max-width: {make_line_width()}')
                GET('txt').style(settings_styling)

        size = [
            option(12),
            option(13),
            option(14),
            option(15),
            option(16),
            option(17),
            option(18),
        ]
        
        font_options = [
            option('monospace'),
            option('courier'),
            option('arial'),
            option('comic sans ms'),
            option('helvatica'),
        ]


    # Input('font family', sizepolicy=fixed, value=MAIN['font_family'], id='font')
        settings = [
            [Select(font_options, id='font'), Select(size, placeholder=MAIN['size'], id='-size-')],
            [Button('Apply', call(pop_action, 'apply'), id='apply'), Button('Cancel', call(pop_action, 'cancel') , id='cancel')]
        ]

        # settings = [
        #     [Text('UNAVAILABLE!', alignment=center)],
        #     [Button('Cancel', call(pop_action, 'cancel') , id='cancel')]
        # ]
        
        popup(id='settings', widgets=settings,frame=False, lock=True, size=(230, 100), modal=True)
        GET('apply').style(POPUP_STYLING)
        GET('cancel').style(POPUP_STYLING)
        GET('-size-').style('max-width: 40px;')

        sizes = [12, 13, 14, 15, 16, 17, 18]
        GET('-size-').set(sizes.index(int(MAIN['size'])))

        fonts = ['monospace', 'courier', 'arial', 'comic sans ms', 'helvatica']
        GET('font').set(fonts.index(MAIN['font_family']))

    tool_items = [
        Button(func=call(handle, 'new'), icon=f'{DIR_NAME}/../icons/add-file.png', icon_size=25, tooltip='new', shortcut='Ctrl+N'),
        Button(func=call(handle, 'open'), icon=f'{DIR_NAME}/../icons/documents.png', icon_size=25, tooltip='open', shortcut='Ctrl+O'),
        Button(func=call(handle, 'save'), icon=f'{DIR_NAME}/../icons/save.png', icon_size=25, tooltip='save', shortcut='Ctrl+S'),
        Button(func=call(handle, 'save_as'), icon=f'{DIR_NAME}/../icons/save-as.png', icon_size=25, tooltip='save as', shortcut='Ctrl+Shift+S'),
        Button(id='switch', func=switch, icon=f'{DIR_NAME}/../icons/on.png', icon_size=25, tooltip='switch', shortcut='F5'),
        Button(id='gear', func=settings, icon=f'{DIR_NAME}/../icons/gear.png', icon_size=25, tooltip='settings'),
        Text(id='space', sizepolicy=('expand', 'expand')),
        Button(func=call(handle, 'exit'), icon=f'{DIR_NAME}/../icons/close.png', icon_size=25, tooltip='exit', shortcut='Esc'),
    ]

    toolbar('main', tool_items, position='right', orientation='v', id='tools', border=False)
    # Textarea('line', disabled=True, value='1'), 

    Box([[Textarea('line', disabled=True, value='1'), Textarea('txt', text_changed=changed, wordwrap=False)]])

    GET('txt').scrollbar(GET('line').scrollbar(id='scroll'))
    GET('line').alignment('right')


    keywords = [
        'button', 
        'text', 
        'input', 
        'checkbox', 
        'radiobutton',
        'toolbar', 
        'fieldset', 
        'item', 
        'textarea', 
        'window',
        'listwidget', 
        'select', 
        'progressbar', 
        'slider', 
        'dial',
        'tabwidget', 
        'popup', 
        'group',
        'stack',
        'scrollbar'
    ]


    synthax = {
        r'(.*).*\{': {
            'color': 'rgb(14, 106, 182)'
        },
        
        r(keywords): {
            'color': 'red',
        }, 
        
        r'(.*).*:': {
            'color': 'rgb(131, 130, 130)'
        },

        '\'(.*?)\'|\"(.*?)\"': {
            'color': 'yellow',
        },

        ':(.*);|:(.*)': {
            'color': 'red'
        },

        r'(-)[0-9]': {
            'color': 'rgb(14, 106, 182)'
        },

        r'[0-9](.*)[0-9]': {
            'color': 'rgb(14, 106, 182)'
        },

        r'px': {
            'color': 'rgb(131, 130, 130)'
        },

        r(['rgb',"rgba"]): {
            'color': 'rgb(155, 102, 197)'
        },

        
        r'\:|\;|\,': {
            'color': 'white'
        },

        r'[0-9]': {
            'color': 'rgb(14, 106, 182)'
        },

        

        r'\A#(.*)': {
            'color': 'rgb(94, 134, 0)'
        },
        
        r'\{|\}': {
            'color': 'rgb(235, 211, 3)'
        },
        
        r'\(|\)': {
            'color': 'rgb(112, 66, 150)'
        },
        
        
    }


    Highlight('txt', synthax)
    GET('txt').focus()
    window.run(css)
