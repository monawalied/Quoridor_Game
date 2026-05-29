# Quoridor Strategy Engine

A full implementation of the abstract strategy board game **Quoridor**, built with Python and Tkinter. Supports Human vs Human and Human vs AI gameplay with three difficulty levels.

---

##  Game Description

Quoridor is a 2-player strategy board game played on a 9×9 grid. Each player starts at the center of their baseline and must race to reach the opposite side. On each turn, a player can either **move their pawn** one square orthogonally, or **place a wall** to block the opponent — but walls can never completely cut off a player's path to their goal.

---

##  Screenshots


---

##  Installation & Running

### Requirements
- Python 3.8+
- Tkinter (usually included with Python standard installation)

### Steps

```bash
# 1. Clone the repository
git clone [https://github.com/monawalied/Quoridor_Game.git](https://github.com/monawalied/Quoridor_Game.git)

# 2. Navigate into the project directory
cd Quoridor_Game

# 3. Run the game
python main.py

```
---

##  Controls

| Action | How to Perform |
| :--- | :--- |
| **Move pawn** | Click on any valid destination square |
| **Place wall** | Hover near a cell edge and click |
| **Rotate wall** | Press `Space` key to switch between Horizontal & Vertical |
| **Reset game** | Click the **Reset Game** button at the bottom |
| **Return to menu** | Click the **Main Menu** button to go back |

---

##  Game Modes

- **Human vs Human** — Two players take turns competing on the same computer.
- **Human vs Computer** — Play against an AI opponent with three distinct difficulty levels:
  - 🟢 **Easy** — AI greedily moves its pawn directly toward its goal.
  - 🟡 **Medium** — AI dynamically balances between moving and placing blocking walls when you are ahead.
  - 🔴 **Hard** — AI utilizes the **Minimax Algorithm with Alpha-Beta Pruning** (depth 3) to make highly strategic decisions.

---

##  Project Structure

```text
quoridor/
├── main.py          # Entry point, launches the Tkinter main menu
├── board_ui.py      # GUI layout, board rendering, and user interactions
├── game_logic.py    # Core game rules, wall validations, and move generation
├── ai.py            # AI decision making logic (Easy / Medium / Hard)
└── README.md        # Project documentation

```
---

## Demo Video

[Watch the demo here] linkkkkkkkkkkkk

---
