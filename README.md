# Minesweeper AI Agent
### CS-199 Final Project

** Author(s): Serena Nguyen, Justin Chung **

### Overview
This is an autonomous Minesweeper agent that intelligently solves Minesweeper boards using:
- Frontier analysis
- Constraint satisfaction
- Model checking
Developed as a final project for CS-199 at UC Irvine.

---

### Authors
- Serena Nguyen
- Justin Chung

---

### File Descriptions:
| File         | Description |
|--------------|-------------|
| `Main.py`    | Entry point. Sets up game environment and runs the chosen AI agent. |
| `World.py`   | Handles the Minesweeper game board logic, including cell generation and mine placement. |
| `AI.py`      | Abstract base class for all AI agents. |
| `ManualAI.py`| Allows human input to manually play the game for testing purposes. |
| `MyAI.py`    | Custom AI agent implementation. Core logic lives here. |
| `RandomAI.py`| Baseline agent that makes random moves (used for benchmarking). |
| `Action.py`  | Contains enums/constants used to define agent actions. |
| `test.world` | Sample input board to test the agent. |
| `Group8-1.pdf`| Final project report submitted for grading. |

---
### How to Run
'''bash
python3 Main.py -f test.world

