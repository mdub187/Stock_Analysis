# __init__.py

from .login import login_window
from .revive import main_frame


# cli executable
def main():
    from .login import login_window
    login_window()
