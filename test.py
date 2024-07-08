import pyautogui
import os

gesture_to_action = {
    'call': lambda: pyautogui.hotkey('win', 'h'),
    'dislike': lambda: pyautogui.hotkey('alt', 'f4'),
    'fist': lambda: os.system('shutdown /p'),
    'like': lambda: pyautogui.hotkey('win', 'n'),
    'mute': lambda: pyautogui.press('volumemute'),
    'ok': lambda: pyautogui.hotkey('win', 'e'),
    'one': lambda: pyautogui.hotkey('win', '1'),
    'palm': lambda: pyautogui.hotkey('win', 'd'),
    'peace': lambda: pyautogui.press('nexttrack'),
    'peace_inverted': lambda: (pyautogui.press('prevtrack'), pyautogui.press('prevtrack')),
    'rock': lambda: os.system('calc'),
    'stop': lambda: pyautogui.press('playpause'),
    'stop_inverted': lambda: pyautogui.hotkey('win', 'prtscr'),
    'three': lambda: pyautogui.hotkey('ctrl', 'shift', 'esc'),
    'three2': lambda: pyautogui.hotkey('win', 'i'),
    'two_up': lambda: pyautogui.scroll(-1000),
    'two_up_inverted': lambda: pyautogui.scroll(1000)
}
