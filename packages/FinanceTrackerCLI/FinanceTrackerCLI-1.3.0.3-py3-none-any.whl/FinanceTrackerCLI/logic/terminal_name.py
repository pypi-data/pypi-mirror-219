import sys


def set_terminal_title(title):
    if sys.platform.startswith('win32'):
        # For Windows
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        # For Linux, macOS, and other Unix-like systems
        sys.stdout.write(f"\033]0;{title}\a")
        sys.stdout.flush()


def get_terminal_title():
    if sys.platform.startswith('win32'):
        # For Windows
        import ctypes
        buff = ctypes.create_unicode_buffer(1024)
        ctypes.windll.kernel32.GetConsoleTitleW(buff, len(buff))
        return buff.value
    else:
        # For Linux, macOS, and other Unix-like systems
        return ""
