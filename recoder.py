import pickle
import time
from pynput import mouse
from pynput import keyboard

class MouseKeyboardRecorder:
    def __init__(self):
        self.events = []
        self.mouse_listener = None
        self.keyboard_listener = None
        self.last_click_time = 0  # 最後にクリックした時間を保存する変数
    # マウスの移動を受け取る関数
    def on_move(self, x, y):
        self.events.append(('mouse_move', x, y))

    # クリックイベントを受け取る関数
    def on_click(self, x, y, button, pressed):
        action = 'press' if pressed else 'release'
        current_time = time.time()  # 現在の時間を取得（秒単位）

        # 前回のクリックからの経過時間が0.5秒以下であれば、ダブルクリックとみなす
        if current_time - self.last_click_time <= 0.5:
            action = 'double_click'
            self.last_click_action = None  # ダブルクリックを検出したら、最後のクリックアクションをリセット
        else:
            self.last_click_action = 'single_click' if action == 'release' else None
        self.events.append(('mouse_click', x, y, button, action))

        # 最後にクリックした時間を更新
        self.last_click_time = current_time if action != 'double_click' else 0  # ダブルクリックの場合はリセット
        
    # スクロールイベントを受け取る関数
    def on_scroll(self, x, y, dx, dy):
        self.events.append(('mouse_scroll', x, y, dx, dy))

    # キーイベントを受け取る関数
    def on_key_press(self, key):
        try:
            self.events.append(('key_press', key.char))
        except AttributeError:
            # special keys
            self.events.append(('key_press', str(key)))
    # キーイベントを受け取る関数
    def on_key_release(self, key):
        if key == keyboard.Key.esc:
            self.stop()
        try:
            self.events.append(('key_release', key.char))
        except AttributeError:
            # special keys
            self.events.append(('key_release', str(key)))
    # 録画を開始する関数
    def start(self):
        self.mouse_listener = mouse.Listener(
            on_move=self.on_move, 
            on_click=self.on_click, 
            on_scroll=self.on_scroll)
        self.mouse_listener.start()

        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press, 
            on_release=self.on_key_release)
        self.keyboard_listener.start()
    
    # 録画を終了する関数
    def stop(self):
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        return self.events
    
    def save_events_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.events, file)  # イベントをpickleファイルに保存

    @staticmethod
    def load_events_from_file(filename):
        with open(filename, 'rb') as file:
            events = pickle.load(file)  # pickleファイルからイベントを読み込み
        return events

if __name__ == '__main__':
    recorder = MouseKeyboardRecorder()
    try:
        recorder.start()
        recorder.mouse_listener.join()
        recorder.keyboard_listener.join()
    except KeyboardInterrupt:
        pass  # Ctrl+Cが押された場合、エラーを無視
    finally:
        recorder.save_events_to_file('events.pkl')  # イベントをpickleファイルに保存
        print('Events saved to events.pkl')  # 保存が完了したことを通知
