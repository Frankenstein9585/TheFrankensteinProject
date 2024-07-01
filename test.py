import pyautogui
import os

# with pag.hold('win'):
#     pag.press('4')

# def gesture_mapping(gesture):
#     if gesture == 'mute':
#         pag.press('volumemute')
#
#     if gesture == 'ok':
#         with pag.hold('win'):
#             pag.press('prtscr')
#
#     if gesture == 'fist':
#         with pag.hold('win'):
#             pag.press('d')


gesture_to_action = {
    'call': lambda: pyautogui.hotkey('win', 'h'),
    'dislike': lambda: pyautogui.hotkey('alt', 'f4'),
    # 'fist': lambda: os.system('shutdown /p'),
    'four': lambda: pyautogui.hotkey('win' '4'),
    'like': lambda: pyautogui.hotkey('win', 'n'),
    'mute': lambda: pyautogui.press('volumemute'),
    'ok': lambda: pyautogui.hotkey('win', 'e'),
    'one': lambda: pyautogui.hotkey('win', '1'),
    'palm': lambda: pyautogui.hotkey('win', 'd'),
    'peace': lambda: pyautogui.hotkey('ctrl', 'shift', 'esc'),
    'peace_inverted': lambda: pyautogui.hotkey('alt', 'tab'),
    'rock': lambda: os.system('calc'),
    'stop': lambda: pyautogui.press('playpause'),
    'stop_inverted': lambda: pyautogui.hotkey('win', 'prtscr'),
    # 'three': lambda: pyautogui.hotkey('win', '3'),
    # 'three2': lambda: pyautogui.hotkey('win', 'i'),
    'three': lambda: pyautogui.press('nexttrack'),
    'three2': lambda: pyautogui.press('prevtrack'),
    'two_up': lambda: pyautogui.hotkey('win', 'shift', 'm'),
    'two_up_inverted': lambda: pyautogui.hotkey('win', 'm')
}
