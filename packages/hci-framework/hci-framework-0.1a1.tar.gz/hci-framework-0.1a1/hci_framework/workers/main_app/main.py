from hci_framework.radiant.server import FrameworkAPI
from browser import html


########################################################################
class BareMinimum(FrameworkAPI):

    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        self.body <= html.H1('Main App')


if __name__ == '__main__':
    BareMinimum()
