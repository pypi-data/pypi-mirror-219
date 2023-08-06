"""
QVSED - Qt-Based Volatile Small Editor
A cross-platform simple and volatile text editor by Arsalan Kazmi
See README.md or "Get Help" inside QVSED for more info
"""

# pylint: disable=no-name-in-module
# pylint: disable=attribute-defined-outside-init
# pylint: disable=broad-exception-caught
# pylint: disable=line-too-long

import os
import sys
import shutil
import importlib.util
import pkg_resources
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFileDialog,
    QAction, QShortcut, QDialog
)
from PyQt5.QtGui import (
    QKeySequence, QFont, QDragEnterEvent, QDropEvent,
    QTextCursor
)
from PyQt5.QtCore import (
    Qt, QTextCodec, QEvent, QObject, QTimer
)
from PyQt5.uic import loadUi


class QVSEDApp:
    """
    The main application class for QVSED.
    """

    def __init__(self):
        """
        Initialize the QVSED application.
        """
        self.app = QApplication([])
        self.window = QVSEDWindow()

    def run(self):
        """
        Run the QVSED application.
        """
        self.window.show()
        self.app.exec()


class QVSEDWindow(QMainWindow):
    """
    The main window class for QVSED.
    """

    def __init__(self):
        """
        Initialize the QVSED window.
        """
        super().__init__()
        self.load_ui_file()
        self.focus_text_area()
        self.install_event_filter()
        self.set_text_area_encoding("UTF-8")
        self.set_up_text_area_handlers()
        self.set_up_action_deck()
        self.echo_area_update(f"Welcome to QVSED v{self.get_qvsed_version()}!")
        self.load_config()
        self.set_up_fonts()
        if self.check_if_file_parameter():
            self.load_from_file(sys.argv[1])

    def apply_style_sheet(self, text_color, background_color, button_color, button_text_color,
                            button_hover_color, button_pressed_color, text_area_color,
                            text_area_text_color, echo_area_color, echo_area_text_color,
                            scroll_bar_color, scroll_bar_background_color, scroll_bar_hover_color,
                            scroll_bar_pressed_color):
        """
        Generate and apply a style sheet based on the config.py file.
        """

        stylesheet = f"""
QMainWindow, QDialog {{
    color: {text_color};
    background: {background_color};
}}

QLabel {{
    color: {text_color};
}}

QPlainTextEdit, QLineEdit {{
    padding: 8px;
    border: none;
}}

QPlainTextEdit {{
    color: {text_area_text_color};
    background: {text_area_color};
}}

QLineEdit {{
    color: {echo_area_text_color};
    background: {echo_area_color};
}}

QPushButton {{
    color: {button_text_color};
    border: 2px solid {button_hover_color};
    background: {button_color};
    padding: 2px;
}}

QPushButton:hover {{
    color: {text_color};
    background: {button_hover_color};
}}

QPushButton:pressed {{
    color: {text_color};
    background: {button_pressed_color};
}}

QScrollBar:vertical {{
    background-color: {scroll_bar_background_color};
    width: 16px;
    margin: 16px 0 16px 0;
}}

QScrollBar::handle:vertical {{
    background-color: {scroll_bar_color};
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {scroll_bar_hover_color};
}}

QScrollBar::handle:vertical:pressed {{
    background-color: {scroll_bar_pressed_color};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    background: none;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}
        """

        # Apply the stylesheet to the app
        self.setStyleSheet(stylesheet)

    def check_if_file_parameter(self):
        """
        Check if a file path was specified at the parameter.
        """
        if len(sys.argv) < 2:
            return False

        file_path = sys.argv[1]
        return os.path.isfile(file_path)

    def clear_text_area(self):
        """
        Clear the Text Area.
        """
        text_area = self.textArea

        if text_area.toPlainText() == "":
            self.echo_area_update("Text Area is already blank.")
            return

        text_area.clear()

        self.echo_area_update("Text Area has been cleared.")

    def connect_command_buttons(self):
        """
        Connect the Action Deck command buttons to their respective functions.
        """
        self.clearButton.clicked.connect(self.clear_text_area)
        self.saveButton.clicked.connect(self.save_text_contents)
        self.openButton.clicked.connect(self.load_from_file)
        self.helpButton.clicked.connect(self.show_help)
        self.quitButton.clicked.connect(self.quit_app)
        self.fullscreenButton.clicked.connect(self.toggle_fullscreen)

    def connect_key_bindings(self):
        """
        Connect the QVSED keybindings to their respective functions.
        """
        # Action Deck
        self.clear_shortcut.activated.connect(self.clear_text_area)
        self.save_shortcut.activated.connect(self.save_text_contents)
        self.open_shortcut.activated.connect(self.load_from_file)
        self.help_shortcut.activated.connect(self.show_help)
        self.quit_shortcut.activated.connect(self.quit_app)
        self.fullscreen_shortcut.activated.connect(self.toggle_fullscreen)

        # Cursor movement
        self.shortcut_up.activated.connect(lambda: self.move_cursor(QTextCursor.Up))
        self.shortcut_down.activated.connect(lambda: self.move_cursor(QTextCursor.Down))
        self.shortcut_left.activated.connect(lambda: self.move_cursor(QTextCursor.Left))
        self.shortcut_right.activated.connect(lambda: self.move_cursor(QTextCursor.Right))
        self.shortcut_home.activated.connect(lambda: self.move_cursor(QTextCursor.StartOfLine))
        self.shortcut_end.activated.connect(lambda: self.move_cursor(QTextCursor.EndOfLine))
        self.shortcut_fwrdword.activated.connect(lambda: self.move_cursor(QTextCursor.NextWord))
        self.shortcut_backword.activated.connect(lambda: self.move_cursor(QTextCursor.PreviousWord))

        # Page movement
        self.shortcut_pgup.activated.connect(lambda: self.move_half_page(QTextCursor.Up))
        self.shortcut_pgdn.activated.connect(lambda: self.move_half_page(QTextCursor.Down))

    def drag_enter_event(self, event: QDragEnterEvent):
        """
        Handle the drag enter event for the Text Area.
        """
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def drop_event(self, event: QDropEvent):
        """
        Handle the drop event for the Text Area.
        """
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.load_from_file(file_path)
        text_area = self.textArea
        text_area.repaint()

    def echo_area_timeout_clear(self, interval):
        """
        Clear the Echo Area after a duration of time.
        """
        echo_area = self.echoArea
        self.clear_timer = QTimer()
        self.clear_timer.setSingleShot(True)
        self.clear_timer.setInterval(interval)
        self.clear_timer.timeout.connect(echo_area.clear)
        self.clear_timer.start()

    def echo_area_update(self, message):
        """
        Update the Echo Area with the given message.
        """
        echo_area = self.echoArea
        echo_area.setText(message)
        echo_area.setCursorPosition(0)
        self.echo_area_timeout_clear(3000)

    def focus_text_area(self):
        """
        Set the Text Area to have focus.
        """
        text_area = self.textArea
        text_area.setFocus()

    def generate_config(self):
        """
        Generate the config file for QVSED.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_default = os.path.join(current_dir, "config_default.py")

        if os.name == "nt":  # Windows
            user_config_dir = os.path.join(os.environ["APPDATA"], "QVSED")
        else:  # *nix
            user_config_dir = os.path.expanduser("~") + "/.config/QVSED"

        if not os.path.exists(user_config_dir):
            os.makedirs(user_config_dir)
        user_config_file = os.path.join(user_config_dir, "config.py")

        shutil.copyfile(config_default, user_config_file)

        # Update the first line of config.py
        with open(user_config_file, "r+", encoding="utf-8") as config_file:
            lines = config_file.readlines()
            if lines:
                lines[0] = "# This is QVSED's config file, you can change its options here.\n"
                config_file.seek(0)
                config_file.writelines(lines)
                config_file.truncate()

        self.echo_area_update(f"Config generated at {user_config_file}.")

    def get_qvsed_version(self):
        """
        Return the QVSED version specified in setup.py.
        """
        try:
            return pkg_resources.get_distribution('qvsed').version
        except pkg_resources.DistributionNotFound:
            return "?.?.?"

    def install_event_filter(self):
        """
        Install the `keyPressFilter` to the Text Area.

        Used to handle incorrect key combinations.
        """
        text_area = self.textArea
        self.keyPressFilter = KeyPressFilter(self)
        text_area.installEventFilter(self.keyPressFilter)

    def load_config(self):
        """
        Load the configuration for QVSED.
        """
        if os.name == "nt":  # Windows
            user_config_dir = os.path.join(os.environ["APPDATA"], "QVSED")
        else:  # *nix
            user_config_dir = os.path.expanduser("~") + "/.config/QVSED"

        user_config_file = os.path.join(user_config_dir, "config.py")

        if not os.path.isfile(user_config_file):
            self.generate_config()

        spec = importlib.util.spec_from_file_location("qvsed_config", user_config_file)
        qvsed_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(qvsed_config)

        self.font_family = qvsed_config.font_family
        self.font_size = qvsed_config.font_size

        # Load the colour scheme settings from the config file
        # We use the shorter American spellings because it's standard, I guess
        text_color = getattr(qvsed_config, 'text_color', None)
        background_color = getattr(qvsed_config, 'background_color', None)

        button_color = getattr(qvsed_config, 'button_color', None)
        button_text_color = getattr(qvsed_config, 'button_text_color', text_color)
        button_hover_color = getattr(qvsed_config, 'button_hover_color', getattr(qvsed_config, 'button_focus_color', None))
        button_pressed_color = getattr(qvsed_config, 'button_pressed_color', background_color)

        text_area_color = getattr(qvsed_config, 'text_area_color', button_hover_color)
        text_area_text_color = getattr(qvsed_config, 'text_area_text_color', text_color)
        echo_area_color = getattr(qvsed_config, 'echo_area_color', button_hover_color)
        echo_area_text_color = getattr(qvsed_config, 'echo_area_text_color', text_color)

        scroll_bar_color = getattr(qvsed_config, 'scroll_bar_color', button_color)
        scroll_bar_background_color = getattr(qvsed_config, 'scroll_bar_background_color', button_hover_color)
        scroll_bar_hover_color = getattr(qvsed_config, 'scroll_bar_hover_color', button_pressed_color)
        scroll_bar_pressed_color = getattr(qvsed_config, 'scroll_bar_pressed_color', button_pressed_color)

        self.apply_style_sheet(text_color, background_color, button_color, button_text_color,
                               button_hover_color, button_pressed_color, text_area_color,
                               text_area_text_color, echo_area_color, echo_area_text_color,
                               scroll_bar_color, scroll_bar_background_color, scroll_bar_hover_color,
                               scroll_bar_pressed_color)

        if None in (text_color, background_color, button_color, button_hover_color):
            self.echo_area_update("config.py appears to be broken, generating a new one.")
            self.generate_config()

    def load_from_file(self, file_path=None):
        """
        Open a file dialog, and load the contents of a file into the Text Area.
        """
        text_area = self.textArea

        if not file_path:
            dialog_box = FileDialogBox("open", self)
            if dialog_box.exec_():
                file_path = dialog_box.get_selected_file_path()
            else:
                return

        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    text_area.setPlainText(file.read())
                file_name = os.path.basename(file_path)
                self.echo_area_update(f"Opened file {file_name}.")
            except Exception as error:
                self.echo_area_update(f"Error opening file: {str(error)}")
        else:
            self.echo_area_update("Invalid or missing file path.")

    def load_ui_file(self):
        """
        Load the UI file for the QVSED window.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(current_dir, "qvsed.ui")
        loadUi(ui_file, self)

    def move_cursor(self, direction):
        """
        Move the cursor in the Text Area.

        Used for the Vim-style A-h, A-j, A-k and A-l commands.
        """
        text_area = self.textArea
        cursor = text_area.textCursor()
        cursor.movePosition(direction)
        text_area.setTextCursor(cursor)

    def move_half_page(self, direction):
        """
        Move the page up or down in the Text Area.

        Used for the Vim-style A-u and A-d commands.
        """
        text_area = self.textArea
        scroll_bar = text_area.verticalScrollBar()
        scroll_value = scroll_bar.value()
        scroll_maximum = scroll_bar.maximum()
        scroll_step = scroll_bar.singleStep()
        cursor = text_area.textCursor()

        half_page_steps = int(scroll_bar.pageStep() / 2)

        if direction == QTextCursor.Up:
            scroll_bar.setValue(max(scroll_value - half_page_steps * scroll_step, 0))
        elif direction == QTextCursor.Down:
            scroll_bar.setValue(min(scroll_value + half_page_steps * scroll_step, scroll_maximum))

        cursor.movePosition(direction, QTextCursor.MoveAnchor, half_page_steps)
        text_area.setTextCursor(cursor)

    def quit_app(self):
        """
        Quit QVSED.
        """
        QApplication.quit()

    def save_text_contents(self):
        """
        Open a file dialog, and save the contents of the Text Area to a file.
        """
        text_area = self.textArea

        if text_area.toPlainText() == "":
            self.echo_area_update("Text Area is blank, will not save.")
            return

        dialog_box = FileDialogBox("save", self)
        if dialog_box.exec_():
            file_path = dialog_box.get_selected_file_path()
        else:
            return

        if not os.path.exists(file_path):
            saved = "Saved new"
            with open(file_path, "w", encoding="UTF-8"):
                pass
        else:
            saved = "Saved"

        if file_path:
            try:
                with open(file_path, "w", encoding="UTF-8") as file:
                    file.write(text_area.toPlainText())
                file_name = os.path.basename(file_path)
                self.echo_area_update(f"{saved} file {file_name}.")
            except Exception as error:
                self.echo_area_update(f"Error saving file: {str(error)}")


    def set_text_area_encoding(self, encoding):
        """
        Set the Text Area encoding.

        Args:
            encoding (str): The encoding to set for the Text Area.
        """
        QTextCodec.setCodecForLocale(QTextCodec.codecForName(encoding))

    def set_up_action_deck(self):
        """
        Set up the Action Deck for the QVSED window.

        This module does nothing by itself, but it's used to run the
        below three modules, which are all components of the Action Deck.
        """
        self.set_up_actions()
        self.set_up_shortcuts()
        self.set_up_action_deck_handlers()

    def set_up_actions(self):
        """
        Set up the Action Deck commands for the QVSED window.
        """
        self.clear_action = QAction("Clear Text", self)
        self.save_action = QAction("Save File", self)
        self.open_action = QAction("Open File", self)
        self.help_action = QAction("Get Help", self)
        self.quit_action = QAction("Quit QVSED", self)

    def set_up_action_deck_handlers(self):
        """
        Set up the event handlers for the Action Deck.
        """
        self.connect_command_buttons()
        self.connect_key_bindings()

    def set_up_text_area_handlers(self):
        """
        Set up the event handlers for the Text Area.
        """
        text_area = self.textArea

        text_area.dragEnterEvent = self.drag_enter_event
        text_area.dragMoveEvent = self.drag_enter_event
        text_area.dropEvent = self.drop_event

    def set_up_fonts(self):
        """
        Set up the fonts for the QVSED window.
        """
        text_area = self.textArea
        font = QFont()
        font.setFamilies(self.font_family)
        if sys.platform == "darwin":
            # macOS fonts should be bigger
            self.font_size += 4
        font.setPointSize(self.font_size)
        text_area.setTabStopWidth(4 * text_area.fontMetrics().width(' '))
        QApplication.instance().setFont(font)
        self.update_widget_fonts(self)

    def set_up_shortcuts(self):
        """
        Set up the key bindings for QVSED.
        """
        # Action Deck
        self.clear_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.open_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        self.help_shortcut = QShortcut(QKeySequence("Ctrl+H"), self)
        self.quit_shortcut = QShortcut(QKeySequence("Alt+Q"), self)
        self.fullscreen_shortcut = QShortcut(QKeySequence("Alt+F"), self)

        # Vim-style movement with Alt/Option key
        self.shortcut_left = QShortcut(QKeySequence("Alt+H"), self)
        self.shortcut_down = QShortcut(QKeySequence("Alt+J"), self)
        self.shortcut_up = QShortcut(QKeySequence("Alt+K"), self)
        self.shortcut_right = QShortcut(QKeySequence("Alt+L"), self)

        self.shortcut_pgup = QShortcut(QKeySequence("Alt+U"), self)
        self.shortcut_pgdn = QShortcut(QKeySequence("Alt+D"), self)

        self.shortcut_fwrdword = QShortcut(QKeySequence("Alt+W"), self)
        self.shortcut_backword = QShortcut(QKeySequence("Alt+B"), self)

        # Emacs-style C-a and C-e, but with Alt instead
        self.shortcut_home = QShortcut(QKeySequence("Alt+A"), self)
        self.shortcut_end = QShortcut(QKeySequence("Alt+E"), self)

    def show_help(self):
        """
        Display the help message in the Text Area.
        """
        text_area = self.textArea

        help_message = """QVSED - Qt-based Volatile Small Editor
========================================
QVSED is a stateless, volatile text editor with a minimalist approach, hovering solely on text editing without file metadata or prompts for potentially destructive actions.

This is the Text Area, where the actual editing takes place. Type anything you want into here, and edit as you please.
Down there, at the bottom of the window, is the Echo Area, where messages and errors will be displayed.
On the left of the QVSED window is the Action Deck, containing commands to clear the Text Area, open or save a file, display this help text, toggle in and out of full screen mode or quit QVSED.

I hope you enjoy using QVSED! I enjoyed writing it, and it's a nice little venture into my first Qt project.

- Arsalan Kazmi <sonicspeed848@gmail.com>, That1M8Head on GitHub"""

        self.echo_area_update("Help message shown in Text Area.")

        text_area.setPlainText(help_message)

    def toggle_fullscreen(self):
        """
        Toggle the QVSED window between fullscreen and normal mode.
        """
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def update_widget_fonts(self, widget):
        """
        Iteratively update the fonts of the given widget and its children.

        Used to update QVSED's font face.

        Args:
            widget (QWidget): The widget to update the fonts for.
        """
        if widget is None:
            return

        widget.setFont(QApplication.instance().font())

        for child_widget in widget.findChildren(QWidget):
            self.update_widget_fonts(child_widget)

class KeyPressFilter(QObject):
    """
    Subclasses QObject.
    """
    def __init__(self, window):
        super().__init__()
        self.window = window

    def eventFilter(self, obj, event):
        # yes, Pylint, I know it's not snake_case, wanna fight about it?
        """
        Override the eventFilter and use QEvent.KeyPress to handle invalid key bindings.
        """
        if event.type() == QEvent.KeyPress:
            if (event.modifiers() & (Qt.ControlModifier | Qt.AltModifier)) and event.key() not in [Qt.Key_Control, Qt.Key_Alt, Qt.Key_Shift]:
                keys = []
                if event.modifiers() & Qt.ControlModifier:
                    keys.append("C")
                if event.modifiers() & Qt.AltModifier:
                    keys.append("A")
                if event.modifiers() & Qt.ShiftModifier:
                    keys.append("S")
                if event.key() != Qt.Key_No:
                    is_os_shortcut = any(event.matches(shortcut) for shortcut in [
                        QKeySequence.Copy, QKeySequence.Cut, QKeySequence.Paste,
                        QKeySequence.Undo, QKeySequence.Redo, QKeySequence.SelectAll,
                        QKeySequence.MoveToPreviousWord, QKeySequence.MoveToNextWord,
                        QKeySequence.SelectPreviousWord, QKeySequence.SelectNextWord,
                        QKeySequence.SelectStartOfDocument, QKeySequence.SelectEndOfDocument,
                        QKeySequence.DeleteStartOfWord, QKeySequence.DeleteEndOfWord
                    ])
                    if is_os_shortcut:
                        return super().eventFilter(obj, event)

                    key_name = QKeySequence(event.key()).toString().lower()
                    keys.append(key_name)

                key_combination = "-".join(keys)
                undefined_message = f"<{key_combination}> is undefined."
                self.window.echo_area_update(undefined_message)
                return True
        return super().eventFilter(obj, event)

class FileDialogBox(QDialog):
    """
    Class for QVSED file dialogs.
    """
    def __init__(self, operation, parent=None):
        super(FileDialogBox, self).__init__(parent)
        self.load_ui_file()

        home_dir = os.path.expanduser("~")
        cwd = os.getcwd().replace(home_dir, "~").replace("\\", "/")
        self.cwdLabel.setText(f"Current working directory is {cwd}")

        self.operation = operation
        self.selected_file_path = ""

        self.setWindowTitle(f"{self.operation.capitalize()} File")

        self.set_shortcuts()
        self.update_labels()

    def set_shortcuts(self):
        """
        Self-explanatory.
        """
        self.confirmButton.clicked.connect(self.accept)
        self.confirmButton.setShortcut(QKeySequence(Qt.Key_Return))

        self.cancelButton.clicked.connect(self.reject)
        self.cancelButton.setShortcut(QKeySequence(Qt.Key_Escape))
        self.cancelButton.setShortcut(QKeySequence("Alt+Q"))

        self.openSystemDialogButton.clicked.connect(self.open_system_dialog)
        self.openSystemDialogButton.setShortcut(QKeySequence("Ctrl+D"))

    def load_ui_file(self):
        """
        Load the UI file for the QVSED dialog box.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(current_dir, "qvsed_dialog.ui")
        loadUi(ui_file, self)

    def open_system_dialog(self):
        """
        Used to open the system's file dialog.
        """
        file_dialog = QFileDialog()

        if self.operation == "save":
            file_path, _ = file_dialog.getOpenFileName(self, "Save File")
        elif self.operation == "open":
            file_path, _ = file_dialog.getOpenFileName(self, "Open File")

        if file_path:
            self.filePathBox.setText(file_path)
            self.selected_file_path = file_path
            self.accept()

    def get_selected_file_path(self):
        """
        Return the file path specified in the file path box.
        """
        file_path = self.filePathBox.text()
        if os.name == 'nt' and file_path.startswith('~'):
            file_path = os.path.expanduser(file_path.replace('~', os.path.expanduser('~')))
        if file_path:
            return file_path
        return None

    def update_labels(self):
        """
        Update the labels depending on the operation
        """
        self.mainLabel.setText(f"Enter the file path to {self.operation} (relative or absolute)")
        self.confirmButton.setText(self.operation.capitalize())

def main():
    """
    The entry point for the QVSED application.
    """
    app = QVSEDApp()
    app.run()


if __name__ == "__main__":
    main()
