import keyword
import os
import re
import shutil
import qtsass

HEADER_SCSS = '''// ---------------------------------------------------------------------------
//
//    File created programmatically
//
//    The definitions are in the "qdarkstyle.palette" module
//
//    WARNING! All changes made in this file will be lost!
//
//----------------------------------------------------------------------------
'''

HEADER_QSS = '''/* ---------------------------------------------------------------------------

    Created by the qtsass compiler v{}

    The definitions are in the "qdarkstyle.qss._styles.scss" module

    WARNING! All changes made in this file will be lost!

--------------------------------------------------------------------------- */
'''

def _dict_to_scss(data):
    """Create a scss variables string from a dict."""
    lines = []
    template = "${}: {};"
    for key, value in data.items():
        line = template.format(key, value)
        lines.append(line)

    return '\n'.join(lines)


def _scss_to_dict(string):
    """Parse variables and return a dict."""
    data = {}
    lines = string.split('\n')

    for line in lines:
        line = line.strip()

        if line and line.startswith('$'):
            key, value = line.split(':')
            key = key[1:].strip()
            key = key.replace('-', '_')
            value = value.split(';')[0].strip()

            data[key] = value

    return data


def _create_scss_variables(variables_scss_filepath, palette,
                           header=HEADER_SCSS):
    """Create a scss variables file."""
    scss = _dict_to_scss(palette.to_dict())
    data = header + scss + '\n'

    with open(variables_scss_filepath, 'w') as f:
        f.write(data)


def _create_qss(main_scss_path, qss_filepath, header=HEADER_QSS):
    """Create a styles.qss file from qtsass."""
    data = ''

    qtsass.compile_filename(main_scss_path, qss_filepath,
                            output_style='expanded')

    with open(qss_filepath, 'r') as f:
        data = f.read()

    data = header.format(qtsass.__version__) + data

    with open(qss_filepath, 'w') as f:
        f.write(data)

    return data


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QSS_FILEPATH = os.path.join(BASE_DIR, 'test.qss')
MAIN_SCSS_FILEPATH = os.path.join(BASE_DIR, 'scss/main.scss')
VARIABLES_SCSS_FILEPATH = os.path.join(BASE_DIR, 'scss/_variables.scss')
from ZzClient.resource.qss.theme.dark.palette import DarkPalette


def create_qss(qss_filepath=QSS_FILEPATH, main_scss_filepath=MAIN_SCSS_FILEPATH,
               variables_scss_filepath=VARIABLES_SCSS_FILEPATH,
               palette=DarkPalette):
    """Create variables files and run qtsass compilation."""
    _create_scss_variables(variables_scss_filepath, palette)
    stylesheet = _create_qss(main_scss_filepath, qss_filepath)

    return stylesheet


if __name__ == '__main__':
    create_qss()