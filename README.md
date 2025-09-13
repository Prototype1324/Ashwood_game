# Ashwood Game

A narrative-driven detective adventure game built with Python and Tkinter.

## Features
- Immersive story with branching dialog and choices
- Progress bar and scene/step info for each screen
- Satisfying click sound effect on every button press
- Seamless background music that plays throughout the game
- Save/load system and pause menu
- Automated GUI test harness for robust feature verification

## Getting Started

### Requirements
- Python 3.10+
- pygame
- tkinter (usually included with Python)
- ffmpeg (optional, for audio conversion)

### Installation
1. Clone this repository:
   ```bash
   git clone <repo-url>
   cd Ashwood_game
   ```
2. Install dependencies:
   ```bash
   pip install pygame
   ```
3. (Optional) Install ffmpeg for audio conversion:
   ```bash
   sudo apt-get install ffmpeg
   ```

### Running the Game
```bash
python3 'new game files/main.py'
```

### Running the Test Harness
```bash
python3 'new game files/test_game_template.py'
```

## Project Structure
```
Ashwood_game/
├── new game files/
│   ├── main.py                # Game entry point
│   ├── graphics_main.py       # UI, sound, and menu logic
│   ├── dialog.py              # Narrative structure
│   ├── test_game_template.py  # Automated GUI test harness
│   ├── sound effects/         # Click sound (click_sound.wav)
│   └── music/                 # Background music (background_music_piano.wav)
├── old game files/            # Legacy code
└── ...
```

## Audio
- Place your click sound as `new game files/sound effects/click_sound.wav`.
- Place your background music as `new game files/music/background_music_piano.wav` (or .ogg).

## Customization
- Edit `dialog.py` to change the story, scenes, and dialog options.
- Replace audio files to change sound effects or music.

## License
This project is for educational and personal use. For commercial use, ensure all assets (music, sound, images) are properly licensed.

---
Enjoy your adventure in Ashwood!
