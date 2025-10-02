# 🖐️ Virtual Hand Gesture Keyboard

This project is a **Virtual Keyboard** built with **Python, OpenCV, and CVZone**.  
It allows users to type using **hand gestures** tracked via a webcam, without a physical keyboard.  

The system detects hand movements (index finger) to select keys on a virtual keyboard displayed on the screen.  
Features include typing characters, navigation with arrows `< >`, spacebar, and delete functionality.

---

## 🚀 Features
- ✅ Virtual keyboard with **multi-row layout** (letters, numbers, and symbols).  
- ✅ Cursor navigation support (`<` = left, `>` = right).  
- ✅ Functional **SPACE** and **DELETE** keys.  
- ✅ Visual **cursor position indicator** in the text field.  
- ✅ Gesture-based selection by holding the index finger on a key for **0.25s**.  
- ✅ Real-time text display with automatic wrapping.  
- ✅ Simple, intuitive UI using OpenCV.  

---

## 📸 Demo (Example Workflow)
1. Run the script.  
2. A virtual keyboard will appear on the screen.  
3. Place your **index finger** above a key.  
4. Hold for **0.25 seconds** to select the key.  
5. Typed text will appear in the text box below the keyboard.  
6. Use:
   - `<` → Move cursor left  
   - `>` → Move cursor right  
   - `SPACE` → Insert space  
   - `DELETE` → Remove last character  

---

## 🛠️ Tech Stack
- [Python 3](https://www.python.org/)
- [OpenCV](https://opencv.org/)
- [CVZone](https://github.com/cvzone/cvzone) – for hand tracking
- [pynput](https://pypi.org/project/pynput/) – for keyboard control
- [NumPy](https://numpy.org/)

---

## 📂 Project Structure

📦 Virtual Keyboard
┣ 📜 virtual_keyboard.py # Main project file
┣ 📜 requirements.txt # Dependencies
┗ 📜 README.md # Documentation


---

## ⚙️ Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/virtual-keyboard.git
   cd virtual-keyboard

pip install -r requirements.txt


Run the project:
python virtual_keyboard.py


🎮 Controls

✋ Point your index finger at a key.

⏱️ Hold for 0.25 seconds to type.

⌨️ Special keys:

< : Move cursor left

> : Move cursor right

SPACE : Insert a space

DELETE : Remove previous character