from aqt import mw
from aqt.qt import *
from aqt.editor import Editor
from aqt.utils import showInfo

from .config_manager import  get_field
from .phonetic_converter import convert_word, convert_words


def on_strike(editor: Editor):
    convert_word(editor)


def symbol_button(buttons, editor):
    addon_dir = os.path.dirname(os.path.realpath(__file__))
    icon_path = os.path.join(addon_dir, 'resources/SymbolIcon.png')

    editor._links['symbol_button'] = on_strike

    button = editor._addButton(
        icon_path,
        "symbol_button",  # Button name
        "symbol_button"  # Button label
    )


    if isinstance(button, QPushButton):
        button.setStyleSheet("""
            QPushButton {
                width: 40px;  # Set width
                height: 40px;  # Set height
                padding: 0px;  # Remove padding
            }
            QPushButton:pressed {
                background-color: #dddddd;  # Background color when pressed
            }
        """)
    else:
        print("Error: The returned button is not a QPushButton.")

    return buttons + [button]


def get_selected_cards_from_browser(browser):
    selected_card_ids = browser.selectedCards()
    if not selected_card_ids:
        showInfo("Please select cards.")
        return []
    return selected_card_ids


def process_selected_cards_in_browser(browser):

    selected_card_ids = get_selected_cards_from_browser(browser)
    if not selected_card_ids:
        return

    failed_count = 0
    success_count = 0

    for card_id in selected_card_ids:
        card = mw.col.getCard(card_id)

        note = card.note()
        if not convert_words(note):
            failed_count += 1
        else:
            success_count += 1

    display_info = "".join(
            [f"{success_count} words success\n {failed_count} words failed"]
    )
    showInfo(f"{display_info}")


def add_browser_menu_button(browser):
    action = QAction("Convert selected words - PSG", browser)
    action.triggered.connect(lambda: process_selected_cards_in_browser(browser))
    browser.form.menuEdit.addAction(action)
