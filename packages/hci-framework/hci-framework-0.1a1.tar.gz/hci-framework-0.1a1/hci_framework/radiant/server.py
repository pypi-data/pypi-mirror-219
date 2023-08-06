from radiant.framework.server import RadiantAPI, RadiantServer
from radiant.framework.utils import environ, run_script

import os


FigureStream = None

########################################################################
class FrameworkAPI(RadiantAPI):
    """Rename Randiant with a arand new class."""

    # ---------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # ----------------------------------------------------------------------
    def __new__(self, *args, **kwargs):
        """"""
        FrameworkServer(self.__name__, *args, **kwargs)



# ----------------------------------------------------------------------
def FrameworkServer(class_, *args, **kwargs):
    """Rename `RadiantServer` with a preconfigured `StimuliServer`."""

    # brython_environ = {k: os.environ[k] for k in os.environ if k.startswith('BCISTREAM_')}
    # brython_environ = {
        # k: os.environ.get(k)
        # for k in dict(os.environ)
        # if k.startswith('BCISTREAM_')
    # }
    brython_environ = {
        'STREAM': environ('STREAM', '5001'),
        'RADIANT': environ('RADIANT', '5002'),
    }

    if scripts := kwargs.get('scripts'):
        for script, port in scripts:
            if environ(port):
                port = environ(port)
            run_script(script, port)

    return RadiantServer(
        class_,
        path=os.path.realpath(os.path.join(os.path.dirname(__file__), 'brython')),
        # handlers=(
            # [
                # r'^/ws',
                # (
                    # os.path.realpath(
                        # os.path.join(
                            # os.path.dirname(__file__), 'tornado_handlers.py'
                        # )
                    # ),
                    # 'WSHandler',
                # ),
                # {},
            # ],
            # [
                # r'^/dashboard',
                # RadiantHandler,
                # {
                    # 'mode': 'dashboard',
                # },
            # ],
            # [
                # r'^/mode',
                # (
                    # os.path.realpath(
                        # os.path.join(
                            # os.path.dirname(__file__), 'tornado_handlers.py'
                        # )
                    # ),
                    # 'ModeHandler',
                # ),
                # {},
            # ],
        # ),

        template=os.path.realpath(
            os.path.join(os.path.dirname(__file__), 'template.html')
        ),

        modules=[
            'md_git',
            'material_symbols',
            'material_icons',
        ],

        environ=brython_environ,
        port=environ('RADIANT', '5002'),
        host='0.0.0.0',

        # theme=os.path.realpath(
            # os.path.join(os.path.dirname(__file__), 'colors.xml')
        # ),

        # callbacks=[(os.path.realpath(os.path.join(
        # os.path.dirname(__file__), 'tornado_handlers.py')), 'consumer')]
        debug_level=0,
        brython_version='3.11.1',
        **kwargs,
    )

