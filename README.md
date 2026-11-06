# Wizard Duel

A text-based wizard duel RPG for the terminal, with a Czech interface. Pick a character, cast spells, chain combos and survive fights against the dark side. Unofficial fan project, not affiliated with or endorsed by Warner Bros. or J.K. Rowling.

## Features

- **Three game modes:** duel, survival and a story campaign
- **Playable characters** with different strengths and weaknesses
- **Enemies with personality:** Lucius Malfoy, Bellatrix Lestrange and Voldemort, each with voiced lines for fight start, spell casting, hits and defeat
- **Spell combos** that reward the right sequence of spells
- **Quick-time events** during fights
- **Stamina and health bars** and ASCII spell effects drawn with colored output
- **Persistent stats:** wins, losses, matches, level and defeated enemies
- Background music and sound effects
- Integrity check that detects modified game files
- Optional pygame "Wizard Maze" exploration module

## Tech Stack

- Python 3.10+
- colorama (terminal UI)
- pygame and playsound (audio)
- ElevenLabs (only to generate new voice lines)
- PyInstaller (Windows `.exe` build)

## Getting Started

### Prerequisites

- Python 3.10+
- A terminal with color support

### Installation

```bash
git clone https://github.com/Exo-Studios-Code/wizard-duel-game.git
cd wizard-duel-game
pip install -r requirements.txt
```

### Run

```bash
python 5.py
```

In the menu choose **1** to play, then enter the character ID and mode (`1` duel, `2` survival, `3` story). Menu option **4** shows your stats.

### Build an executable

```bash
pip install pyinstaller
pyinstaller 5.spec
```

### Generate new voice lines (optional)

```bash
pip install elevenlabs
export ELEVENLABS_API_KEY=your_key
python vois_generator1.py
```

### Developer note

`anticheat.py` stores SHA-256 hashes of `5.py` and `game_ui.py`. After changing either file, update the hashes there or the integrity check will fail.
