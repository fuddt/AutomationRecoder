# Importing the necessary module to read the pickle file
import pickle
import pyautogui
import time
# Read the content of the uploaded pickle file
pickle_file_path = 'events.pkl'
with open(pickle_file_path, 'rb') as f:
    events_data_pickle = pickle.load(f)

# 各イベントを処理
for event in events_data_pickle:
    event_type = event[0]  # イベントタイプを取り出す

    if event_type == 'mouse_move':
        x, y = event[1], event[2]
        pyautogui.moveTo(x, y)  # マウスカーソルを指定された座標に移動

    elif event_type == 'mouse_click':
        x, y, button, action = event[1], event[2], event[3], event[4]
        button_str = str(button).split('.')[1].lower()  # Buttonオブジェクトを文字列に変換
        pyautogui.click(x, y, button=button_str)  # マウスクリックを再現
        
        if action == 'double_click':
            pyautogui.doubleClick(x, y, button=button_str)  # ダブルクリックを再現
        else:
            pyautogui.click(x, y, button=button_str)  # 通常のクリックを再現
            
    elif event_type == 'mouse_click':
        x, y, button, action = event[1], event[2], event[3], event[4]
        pyautogui.click(x, y, button=button.lower())  # マウスクリックを再現

    elif event_type == 'key_press':
        key = event[1]
        pyautogui.press(key)  # キー押下を再現

    elif event_type == 'key_release':
        # pyautoguiではキーの「押下」と「解放」を個別に制御する機能はありませんが、
        # 'press'関数は押下と解放の両方を行います。
        pass


# 処理が完了したら、完了メッセージを表示
print("Events have been successfully replicated.")
