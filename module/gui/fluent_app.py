# This Python file uses the following encoding: utf-8
# @author runhey
# github https://github.com/runhey
import sys
import os

# --- DLL 预加载（必须在 import PySide6 之前执行）-----------------------------
# 背景：module/gui/FluentUI/fluentuiplugin.dll 依赖 fluentui.dll（在 <项目根>/toolkit）
# 以及 Qt6Core/Qt6Qml/Qt6Quick/Qt6Gui（在 PySide6 目录）。
#
# 坑：Qt 加载 QML 插件时**只按 PATH 环境变量**搜索依赖，Python 的
#     os.add_dll_directory() 对它无效（实测对比过：只加 PATH 成功，只加
#     add_dll_directory 失败）。所以从 IDE 或任意终端直接跑 gui.py 时，如果 PATH
#     里没有那两个目录，就会报：
#         无法加载库 ...\fluentuiplugin.dll：找不到指定的模块。
#
# 解法：在导入 Qt 之前用 ctypes 把这些 DLL 预加载进进程，之后 Qt 加载插件时
#       依赖已在内存里，不再依赖 PATH。实测在 PATH 被清空的情况下依然可用。
def _preload_qt_dlls():
    try:
        import ctypes
    except Exception:  # noqa: BLE001
        return

    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    candidates = []
    try:
        import PySide6
        candidates.append(os.path.dirname(PySide6.__file__))
    except Exception:  # noqa: BLE001
        pass
    candidates.append(os.path.join(repo_root, 'toolkit'))

    for d in candidates:
        if not os.path.isdir(d):
            continue
        # 同时写 PATH 兜底（对某些 Qt 版本仍有帮助）
        os.environ['PATH'] = d + os.pathsep + os.environ.get('PATH', '')
        try:
            names = sorted(os.listdir(d))
        except OSError:
            continue
        for name in names:
            if not name.lower().endswith('.dll'):
                continue
            try:
                ctypes.WinDLL(os.path.join(d, name))
            except OSError:
                pass  # 个别 DLL 加载不了不影响，Qt 会自己再试


_preload_qt_dlls()
# --------------------------------------------------------------------------

from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide6.QtCore import Qt, QObject, QTranslator, QLocale, Slot
from pathlib import Path

from module.gui.utils import get_work_path
from module.gui.Bridge import bridge
from module.logger import logger

# import module.gui.qml_rcc
import module.gui.res_rcc

class FluentApp():
    app = None
    engine = None
    translator = None
    dpi = None

    def __init__(self):
        super().__init__()
        # 适配高分辨率、声明、设置Logo、设置软件名字
        # 后面的这三条失效了 使用 QGuiApplication.setHighDpiScaleFactorRoundingPolicy
        # https://blog.weimo.info/archives/602/
        # QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        # QGuiApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
        # QGuiApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
        os.putenv("QT_QUICK_CONTROLS_STYLE", "Basic")

        FluentApp.app = QGuiApplication(sys.argv)
        QGuiApplication.setWindowIcon(QIcon(os.fspath(Path(__file__).resolve().parent / "res/icon.ico")))
        QGuiApplication.setApplicationName("oas")
        QGuiApplication.setOrganizationName("oas")

        FluentApp.engine = QQmlApplicationEngine()
        FluentApp.engine.addImportPath(os.fspath(Path(__file__).resolve().parent))

        FluentApp.translator = Translator(engine=FluentApp.engine, app=FluentApp.app)
        FluentApp.dpi = DpiScale()
        self.set_context_property(context=FluentApp.translator, name='translator')
        self.set_context_property(context=FluentApp.dpi, name='dpi')

    @classmethod
    def run(cls):
        FluentApp.engine.load(os.fspath(Path(get_work_path() / 'module' / 'gui' / 'qml' / 'app.qml')))
        if not FluentApp.engine.rootObjects():
            sys.exit(-1)
        sys.exit(FluentApp.app.exec())

    @classmethod
    def set_context_property(cls, context, name: str) -> None:
        """
        设置上下文
        :param name:
        :param context:
        :return:
        """
        FluentApp.engine.rootContext().setContextProperty(name, context)



    def qml_register_type(self, Class, qml_class: str) -> None:
        """
        注册qml类型
        :param Class:
        :param qml_class:
        :return:
        """
        qmlRegisterType(Class, "Oas", 1, 0, qml_class)


class Translator(QObject):

    def __init__(self, engine, app) -> None:
        super(Translator, self).__init__()
        self._engine = engine
        self._app = app
        self.path_en_US = str((Path.cwd() / "module" / "config" / "i18n" / "en_US.qm").resolve())
        self.path_zh_CN = str((Path.cwd() / "module" / "config" / "i18n" / "zh_CN.qm").resolve())

        self.translator = QTranslator()

    @Slot(str)
    def set_language(self, language: str) -> None:
        """
        设置语言
        :param language:
        :return:
        """
        if language == "简体中文":
            if not self.translator.load(self.path_zh_CN):
                logger.error("load language 简体中文 failed!")
            QGuiApplication.installTranslator(self.translator)
            self._engine.retranslate()
            return

        if language == "English":
            if not self.translator.load(self.path_en_US):
                logger.error("load language English failed!")
            QGuiApplication.installTranslator(self.translator)
            self._engine.retranslate()
            return

class DpiScale(QObject):
    def __init__(self) -> None:
        super().__init__()

    @Slot(str)
    def set_dpi_scale(self, strategy: str) -> None:
        """
        设置dpi缩放
        :param strategy:
        :return:
        """
        match strategy:
            case "default": QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)  # 不缩放
            case "round": QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Round)  # 设备像素比0.5及以上的，进行缩放
            case "floor": QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Floor)  # 始终不缩放
            case "ceil": QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Ceil)  # 始终缩放
            case "round_prefer_floor": QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.RoundPreferFloor)  # 设备像素比0.75及以上的，进行缩放
            case _: QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)



