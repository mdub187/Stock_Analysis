# __init__.py
#
from login import login_window
from revive import run_main_app


# cli executable
def main():
    from login import login_window
    login_window()
