import os


# ----------------------------------------------------------------------
def select_worker(worker):
    """"""
    return os.path.join(os.path.dirname(__file__), worker)
