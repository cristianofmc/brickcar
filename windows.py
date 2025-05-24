import platform

def set_dpi_awareness():
    if platform.system() == 'Windows':
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
    else:
        # Em Linux/Mac não é necessário ou não existe esse ajuste
        pass