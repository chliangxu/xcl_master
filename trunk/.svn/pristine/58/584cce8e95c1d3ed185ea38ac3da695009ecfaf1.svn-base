import os
import sys


class ResourceUtils:
    @staticmethod
    def get_path(relative_path):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

        return os.path.join(base_path, relative_path)

    @staticmethod
    def get_ui_path(module_path, ui_filename):
        if getattr(sys, 'frozen', False):
            module_dir = os.path.dirname(module_path)
            relative_dir = module_dir.split('src' + os.sep, 1)[-1] if 'src' in module_dir else ''
            base_path = sys._MEIPASS
            ui_dir = os.path.join(base_path, 'src', relative_dir)
        else:
            ui_dir = os.path.dirname(os.path.abspath(module_path))

        return os.path.join(ui_dir, ui_filename)

    @staticmethod
    def exists(relative_path):
        return os.path.exists(ResourceUtils.get_path(relative_path))
