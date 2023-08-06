import os.path as path
import base64

from .data import *

__path__ = __path__[0]

icon_data = {
    'add-file.png': ADD_FILE_ICON,
    'close.png': CLOSE_ICON,
    'document.png': DOCUMENT_ICON,
    'documents.png': DOCUMENTS_ICON,
    'gear.png': GEAR_ICON,
    'hand-drawn-icon.png': HAND_DRAWN_ICON,
    'off.png': OFF_ICON,
    'on.png': ON_ICON,
    'save-as.png': SAVEAS_ICON,
    'save.png': SAVE_ICON,
    'toon-icon.ico': TOON_ICON
}

for KEY in icon_data:
    icon_path = f'{__path__}/{KEY}'
    if path.isfile(icon_path) == False:
        with open(icon_path, 'wb') as image:
                image.write(base64.b64decode(icon_data[KEY]))
    
WINDOW_ICON = f'{__path__}/toon-icon.ico'