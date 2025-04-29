import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from time import sleep, time
import numpy as np
from pynput.keyboard import Controller

# Initialize the webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Initialize the hand detector
detector = HandDetector(detectionCon=0.7, maxHands=1)

# Define the layout of the keyboard keys
keyboard_keys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
                 ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                 ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
                 ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
                 ["SPACE", "<", ">", "DELETE"]]

final_text = ""
cursor_position = len(final_text)  # Track cursor position
selection_start_time = None  # Track the start time of key selection

# Initialize the keyboard controller
keyboard = Controller()

def draw(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 144, 30), cv2.FILLED)
        cv2.putText(img, button.text, (x + 10, y + 45),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)  # Smaller text
    return img

class Button:
    def __init__(self, pos, text, size=[50, 50]):  # Smaller size
        self.pos = pos
        self.size = size
        self.text = text

# Create button list and add spacebar button with larger size
buttonList = []
for k in range(len(keyboard_keys)):
    for x, key in enumerate(keyboard_keys[k]):
        if key == "SPACE":
            buttonList.append(Button([70 * x + 25, 70 * k + 50], "     ", size=[300, 50]))  # Smaller spacebar size
        elif key == "<":
            buttonList.append(Button([70 * x + 325, 70 * k + 50], key))  # Position < key
        elif key == ">":
            buttonList.append(Button([70 * x + 395, 70 * k + 50], key))  # Position > key
        elif key == "DELETE":
            buttonList.append(Button([70 * x + 465, 70 * k + 50], key, size=[150, 50]))  # Increased DELETE key size
        else:
            buttonList.append(Button([70 * x + 25, 70 * k + 50], key))  # Reduced spacing

# Modify the last row specifically to bring keys closer together
last_row_y = 70 * (len(keyboard_keys) - 1) + 50
buttonList[-4] = Button([25, last_row_y], "SPACE", size=[200, 50])
buttonList[-3] = Button([235, last_row_y], "<")
buttonList[-2] = Button([305, last_row_y], ">")
buttonList[-1] = Button([375, last_row_y], "DELETE", size=[150, 50])  # Increased size for DELETE key

def wrap_text_with_cursor(text, cursor_pos, width, font_scale, thickness):
    wrapped_lines = []
    line = ""
    cursor_line = 0
    cursor_char_index = cursor_pos

    for i, char in enumerate(text):
        if cv2.getTextSize(line + char, cv2.FONT_HERSHEY_PLAIN, font_scale, thickness)[0][0] >= width:
            wrapped_lines.append(line)
            line = char
            if i < cursor_pos:
                cursor_line += 1
                cursor_char_index = cursor_pos - i - 1
        else:
            line += char
            if i == cursor_pos:
                cursor_char_index = len(line) - 1

    wrapped_lines.append(line)
    return wrapped_lines, cursor_line, cursor_char_index

while True:
    success, img = cap.read()
    if not success:
        break

    hands, img = detector.findHands(img)  # Detect hands and draw landmarks
    img = draw(img, buttonList)  # Draw the buttons on the image

    if hands:
        lmList = hands[0]['lmList']  # Landmark list of the first hand
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                if selection_start_time is None:
                    selection_start_time = time()
                elif time() - selection_start_time > 0.25:  # Check if the index finger has been on the button for 0.25 seconds
                    key = button.text.lower()
                    if key == "<":
                        cursor_position = max(cursor_position - 1, 0)
                    elif key == ">":
                        cursor_position = min(cursor_position + 1, len(final_text))
                    elif key == "delete":
                        if cursor_position > 0:
                            final_text = final_text[:cursor_position - 1] + final_text[cursor_position:]
                            cursor_position -= 1
                    elif key == "space":
                        final_text = final_text[:cursor_position] + " " + final_text[cursor_position:]
                        cursor_position += 1
                    else:
                        final_text = final_text[:cursor_position] + key + final_text[cursor_position:]
                        cursor_position += 1
                    
                    cv2.rectangle(img, button.pos, (x + w, y + h),
                                  (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 10, y + 45),
                                cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)  # Smaller text
                    sleep(0.2)  # Reduced sleep duration
                    selection_start_time = None  # Reset the timer
                break
        else:
            selection_start_time = None  # Reset if no button is selected

    # Add a white background for the input display
    max_y = max([button.pos[1] + button.size[1] for button in buttonList])
    display_y_start = max_y + 20  # 20 pixels below the keyboard
    cv2.rectangle(img, (20, display_y_start), (1260, display_y_start + 150), (255, 255, 255), cv2.FILLED)

    # Add a cursor to the final text display
    wrapped_lines, cursor_line, cursor_char_index = wrap_text_with_cursor(final_text, cursor_position, 1220, 1.5, 1)  # Adjust width and font size to fit the display area

    y_offset = display_y_start + 30
    for i, line in enumerate(wrapped_lines):
        if i == cursor_line:
            line = line[:cursor_char_index] + "|" + line[cursor_char_index:]
        cv2.putText(img, line, (30, y_offset),
                    cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 1)
        y_offset += 30  # Adjust line spacing as needed

    cv2.imshow("output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
