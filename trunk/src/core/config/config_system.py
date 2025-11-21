import configparser
import sys
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


class ConfigSystem:
    _instance = None
    _ui_config: configparser.ConfigParser = None
    _app_config: configparser.ConfigParser = None
    _tools_config: configparser.ConfigParser = None
    _config_dir: Path = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        self._config_dir = self._get_config_dir()
        self._load_all_configs()
    
    @staticmethod
    def _get_config_dir() -> Path:
        if getattr(sys, 'frozen', False):
            base_path = Path(sys.executable).parent
        else:
            base_path = Path(__file__).parent.parent.parent.parent
        return base_path / 'config'

    def _load_all_configs(self):
        self._ui_config = configparser.ConfigParser()
        self._app_config = configparser.ConfigParser()
        self._tools_config = configparser.ConfigParser()

        ui_file = self._config_dir / 'ui.ini'
        app_file = self._config_dir / 'app.ini'
        tools_file = self._config_dir / 'tools.ini'

        if ui_file.exists():
            self._ui_config.read(ui_file, encoding='utf-8')

        if app_file.exists():
            self._app_config.read(app_file, encoding='utf-8')

        if tools_file.exists():
            self._tools_config.read(tools_file, encoding='utf-8')

    def save_ui_config(self):
        ui_file = self._config_dir / 'ui.ini'
        with open(ui_file, 'w', encoding='utf-8') as f:
            self._ui_config.write(f)

    def save_app_config(self):
        app_file = self._config_dir / 'app.ini'
        with open(app_file, 'w', encoding='utf-8') as f:
            self._app_config.write(f)

    def save_tools_config(self):
        tools_file = self._config_dir / 'tools.ini'
        with open(tools_file, 'w', encoding='utf-8') as f:
            self._tools_config.write(f)

    def _get_str(self, config: configparser.ConfigParser, section: str, key: str, default: str = '') -> str:
        return config.get(section, key, fallback=default)

    def _get_int(self, config: configparser.ConfigParser, section: str, key: str, default: int = 0) -> int:
        return config.getint(section, key, fallback=default)

    def _get_bool(self, config: configparser.ConfigParser, section: str, key: str, default: bool = False) -> bool:
        return config.getboolean(section, key, fallback=default)

    def _set(self, config: configparser.ConfigParser, section: str, key: str, value: Any):
        if not config.has_section(section):
            config.add_section(section)
        config.set(section, key, str(value))

    @property
    def app(self):
        return AppConfig(self)

    @property
    def window(self):
        return WindowConfig(self)

    @property
    def layout(self):
        return LayoutConfig(self)

    @property
    def components(self):
        return ComponentsConfig(self)

    @property
    def fonts(self):
        return FontsConfig(self)

    @property
    def colors(self):
        return ColorsConfig(self)

    @property
    def styles(self):
        return StylesConfig(self)

    @property
    def user(self):
        return UserConfig(self)

    @property
    def features(self):
        return FeaturesConfig(self)

    @property
    def paths(self):
        return PathsConfig(self)

    @property
    def categories(self):
        return CategoriesConfig(self)

    @property
    def tools(self):
        return ToolsConfig(self)

    @property
    def favorites(self):
        return FavoritesConfig(self)

    @classmethod
    def instance(cls) -> 'Config':
        return cls()


class AppConfig:
    def __init__(self, config: ConfigSystem):
        self._config = config

    @property
    def name(self) -> str:
        return self._config._get_str(self._config._app_config, 'App', 'Name', 'CJGameStudio')

    @property
    def version(self) -> str:
        return self._config._get_str(self._config._app_config, 'App', 'Version', '1.0.0')

    @property
    def title(self) -> str:
        return self._config._get_str(self._config._app_config, 'App', 'Title', 'CJGameStudio')

    @property
    def subtitle(self) -> str:
        return self._config._get_str(self._config._app_config, 'App', 'Subtitle', '游戏开发工具集成平台')


class WindowConfig:
    def __init__(self, config: ConfigSystem):
        self._config = config

    @property
    def default_width(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Window', 'DefaultWidth', 1400)

    @property
    def default_height(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Window', 'DefaultHeight', 900)

    @property
    def min_width(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Window', 'MinWidth', 1200)

    @property
    def min_height(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Window', 'MinHeight', 800)

    @property
    def width(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Window', 'Width', self.default_width)

    @property
    def height(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Window', 'Height', self.default_height)

    @property
    def maximized(self) -> bool:
        return self._config._get_bool(self._config._ui_config, 'Window', 'Maximized', False)

    def save_state(self, width: int, height: int, maximized: bool):
        self._config._set(self._config._ui_config, 'Window', 'Width', width)
        self._config._set(self._config._ui_config, 'Window', 'Height', height)
        self._config._set(self._config._ui_config, 'Window', 'Maximized', maximized)
        self._config.save_ui_config()


class LayoutConfig:
    def __init__(self, config: ConfigSystem):
        self._config = config

    @property
    def sidebar_width(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Layout', 'SidebarWidth', 250)

    @property
    def sidebar_padding(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Layout', 'SidebarPadding', 20)

    @property
    def sidebar_spacing(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Layout', 'SidebarSpacing', 15)

    @property
    def header_height(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Layout', 'HeaderHeight', 80)

    @property
    def header_padding_h(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Layout', 'HeaderPaddingH', 30)

    @property
    def header_padding_v(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Layout', 'HeaderPaddingV', 15)

    @property
    def header_spacing(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Layout', 'HeaderSpacing', 20)

    @property
    def banner_height(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Layout', 'BannerHeight', 320)

    @property
    def content_padding(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Layout', 'ContentPadding', 30)

    @property
    def content_spacing(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Layout', 'ContentSpacing', 20)

    @property
    def card_width(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Layout', 'CardWidth', 300)

    @property
    def card_height(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Layout', 'CardHeight', 200)

    @property
    def card_padding(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Layout', 'CardPadding', 15)

    @property
    def card_spacing(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Layout', 'CardSpacing', 20)

    @property
    def card_border_radius(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Layout', 'CardBorderRadius', 12)


class ComponentsConfig:
    def __init__(self, config: ConfigSystem):
        self._config = config

    @property
    def avatar_size(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Components', 'AvatarSize', 80)

    @property
    def icon_size(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Components', 'IconSize', 45)

    @property
    def user_button_size(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Components', 'UserButtonSize', 45)

    @property
    def button_height(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Components', 'ButtonHeight', 35)

    @property
    def button_width(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Components', 'ButtonWidth', 80)

    @property
    def icon_button_size(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Components', 'IconButtonSize', 36)

    @property
    def launch_button_width(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Components', 'LaunchButtonWidth', 70)

    @property
    def launch_button_height(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Components', 'LaunchButtonHeight', 30)

    @property
    def favorite_button_size(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Components', 'FavoriteButtonSize', 30)

    @property
    def dialog_width(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Components', 'DialogWidth', 400)

    @property
    def dialog_height(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Components', 'DialogHeight', 500)


class FontsConfig:
    def __init__(self, config: ConfigSystem):
        self._config = config

    @property
    def family(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Fonts', 'Family', 'Microsoft YaHei UI')

    @property
    def size_small(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Fonts', 'SizeSmall', 10)

    @property
    def size_default(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Fonts', 'SizeDefault', 12)

    @property
    def size_medium(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Fonts', 'SizeMedium', 14)

    @property
    def size_large(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Fonts', 'SizeLarge', 16)

    @property
    def size_title(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Fonts', 'SizeTitle', 20)


class ColorsConfig:
    def __init__(self, config: ConfigSystem):
        self._config = config

    @property
    def background(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Colors', 'Background', '#1e1e1e')

    @property
    def background_secondary(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Colors', 'BackgroundSecondary', '#252526')

    @property
    def surface(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Colors', 'Surface', '#252526')

    @property
    def surface_hover(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Colors', 'SurfaceHover', '#2d2d30')

    @property
    def primary(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Colors', 'Primary', '#0e639c')

    @property
    def primary_hover(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Colors', 'PrimaryHover', '#1177bb')

    @property
    def primary_active(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Colors', 'PrimaryActive', '#00b8e6')

    @property
    def text(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Colors', 'Text', '#cccccc')

    @property
    def text_secondary(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Colors', 'TextSecondary', '#858585')

    @property
    def text_disabled(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Colors', 'TextDisabled', '#858585')

    @property
    def border(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Colors', 'Border', '#3e3e42')

    @property
    def border_hover(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Colors', 'BorderHover', '#555555')

    @property
    def success(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Colors', 'Success', '#4ec9b0')

    @property
    def warning(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Colors', 'Warning', '#ce9178')

    @property
    def error(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Colors', 'Error', '#f48771')

    @property
    def transparent(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Colors', 'Transparent', 'transparent')

    @property
    def black(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Colors', 'Black', '#000000')

    @property
    def dark_gray(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Colors', 'DarkGray', '#3a3a3a')

    @property
    def medium_gray(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Colors', 'MediumGray', '#4a4a4a')

    @property
    def gray(self) -> str:
        return self._config._get_str(self._config._ui_config, 'Colors', 'Gray', '#555555')


class StylesConfig:
    def __init__(self, config: ConfigSystem):
        self._config = config

    @property
    def border_radius_small(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Styles', 'BorderRadiusSmall', 8)

    @property
    def border_radius_medium(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Styles', 'BorderRadiusMedium', 12)

    @property
    def border_radius_large(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Styles', 'BorderRadiusLarge', 22)

    @property
    def border_width(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Styles', 'BorderWidth', 2)

    @property
    def shadow_blur(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Styles', 'ShadowBlur', 10)

    @property
    def shadow_offset(self) -> int:
        return self._config._get_int(self._config._ui_config, 'Styles', 'ShadowOffset', 2)


class UserConfig:
    def __init__(self, config: ConfigSystem):
        self._config = config

    @property
    def last_user(self) -> str:
        return self._config._get_str(self._config._app_config, 'User', 'LastUser', '')

    @property
    def auto_login(self) -> bool:
        return self._config._get_bool(self._config._app_config, 'User', 'AutoLogin', False)

    @property
    def last_category(self) -> str:
        return self._config._get_str(self._config._app_config, 'User', 'LastCategory', 'production_pipeline')

    @property
    def user_name(self) -> str:
        return self._config._get_str(self._config._app_config, 'User', 'UserName', '开发者')

    @property
    def user_role(self) -> str:
        return self._config._get_str(self._config._app_config, 'User', 'UserRole', '客户端程序')

    def save_last_user(self, username: str):
        self._config._set(self._config._app_config, 'User', 'LastUser', username)
        self._config.save_app_config()

    def save_last_category(self, category: str):
        self._config._set(self._config._app_config, 'User', 'LastCategory', category)
        self._config.save_app_config()

    def save_user_info(self, name: str, role: str):
        self._config._set(self._config._app_config, 'User', 'UserName', name)
        self._config._set(self._config._app_config, 'User', 'UserRole', role)
        self._config.save_app_config()


class FeaturesConfig:
    def __init__(self, config: ConfigSystem):
        self._config = config

    @property
    def auto_save(self) -> bool:
        return self._config._get_bool(self._config._app_config, 'Features', 'AutoSave', True)

    @property
    def auto_update(self) -> bool:
        return self._config._get_bool(self._config._app_config, 'Features', 'AutoUpdate', False)

    @property
    def analytics(self) -> bool:
        return self._config._get_bool(self._config._app_config, 'Features', 'Analytics', False)

    @property
    def debug_mode(self) -> bool:
        return self._config._get_bool(self._config._app_config, 'Features', 'DebugMode', False)

    @property
    def show_usage_stats(self) -> bool:
        return self._config._get_bool(self._config._app_config, 'Features', 'ShowUsageStats', True)

    @property
    def enable_favorites(self) -> bool:
        return self._config._get_bool(self._config._app_config, 'Features', 'EnableFavorites', True)


class PathsConfig:
    def __init__(self, config: ConfigSystem):
        self._config = config

    @property
    def data_dir(self) -> str:
        return self._config._get_str(self._config._app_config, 'Paths', 'DataDir', 'data')

    @property
    def logs_dir(self) -> str:
        return self._config._get_str(self._config._app_config, 'Paths', 'LogsDir', 'logs')

    @property
    def config_dir(self) -> str:
        return self._config._get_str(self._config._app_config, 'Paths', 'ConfigDir', 'config')

    @property
    def cache_dir(self) -> str:
        return self._config._get_str(self._config._app_config, 'Paths', 'CacheDir', 'cache')

    @property
    def tools_dir(self) -> str:
        return self._config._get_str(self._config._app_config, 'Paths', 'ToolsDir', 'tools')

    @property
    def assets_dir(self) -> str:
        return self._config._get_str(self._config._app_config, 'Paths', 'AssetsDir', 'assets')


class CategoriesConfig:
    def __init__(self, config: ConfigSystem):
        self._config = config

    def get_all(self) -> Dict[str, str]:
        if self._config._tools_config.has_section('Categories'):
            return dict(self._config._tools_config.items('Categories'))
        return {}

    def get_name(self, key: str) -> str:
        return self._config._get_str(self._config._tools_config, 'Categories', key, key)

    def get_list(self) -> List[Dict[str, str]]:
        categories = self.get_all()
        return [{'key': key, 'name': name} for key, name in categories.items()]


class ToolsConfig:
    def __init__(self, config: ConfigSystem):
        self._config = config

    def get_all_tools(self) -> List[Dict[str, Any]]:
        tools = []
        for section in self._config._tools_config.sections():
            if section.startswith('Tool:'):
                tool_id = section.replace('Tool:', '')
                tool_data = {
                    'id': tool_id,
                    'name': self._config._get_str(self._config._tools_config, section, 'Name', ''),
                    'description': self._config._get_str(self._config._tools_config, section, 'Description', ''),
                    'category': self._config._get_str(self._config._tools_config, section, 'Category', ''),
                    'tool_type': self._config._get_str(self._config._tools_config, section, 'Type', 'common'),
                    'executable_path': self._config._get_str(self._config._tools_config, section, 'ExecutablePath', ''),
                    'icon': self._config._get_str(self._config._tools_config, section, 'Icon', ''),
                    'enabled': self._config._get_bool(self._config._tools_config, section, 'Enabled', True)
                }
                tools.append(tool_data)
        return tools


class FavoritesConfig:
    def __init__(self, config: ConfigSystem):
        self._config = config

    def get_favorites(self) -> List[str]:
        favorites_str = self._config._get_str(self._config._app_config, 'Favorites', 'toolids', '')
        if favorites_str:
            return [tool_id.strip() for tool_id in favorites_str.split(',') if tool_id.strip()]
        return []

    def save_favorites(self, favorites: List[str]):
        favorites_str = ','.join(favorites)
        self._config._set(self._config._app_config, 'Favorites', 'toolids', favorites_str)
        self._config.save_app_config()
