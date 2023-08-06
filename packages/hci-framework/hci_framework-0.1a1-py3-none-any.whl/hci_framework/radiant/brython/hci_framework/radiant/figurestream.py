from hci_framework.radiant.utils import environ
from urllib.parse import urlencode
from datetime import datetime
from browser import document, html


########################################################################
class FigureStream:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, port=None):
        """Constructor"""

        if port is None:
            self.port = environ.STREAM
        else:
            self.port = port


        self.URL = f'http://127.0.0.1:{self.port}/figure.jpeg'
        self.query_dict = {
            'width': '12',
            'height': '4',
            'color': 'C0',
        }


    # ----------------------------------------------------------------------
    def set(self, variable, value):
        """"""
        self.query_dict[variable] = value

    # ----------------------------------------------------------------------
    @property
    def query_string(self):
        """"""
        self.query_dict['v'] = datetime.now().timestamp()
        return urlencode(self.query_dict)


    # ----------------------------------------------------------------------
    @property
    def full_path(self):
        """"""
        return f'{self.URL}?{self.query_string}'


    # ----------------------------------------------------------------------
    @property
    def container(self):
        """"""
        self.container_div = html.DIV(f'<img src="{self.full_path}"></img>')
        return self.container_div


    # ----------------------------------------------------------------------
    def update(self):
        """"""
        print(self.full_path)
        self.container_div.html = f'<img src="{self.full_path}"></img>'

