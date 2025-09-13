# 🔥 NERUPPU DAA - Survive the Fire Stones!

An addictive terminal-based survival game built with Python! Dodge falling fire stones, collect power-ups, and compete for high scores in this colorful ASCII adventure.

![Game Preview](https://img.shields.io/badge/Python-3.6%2B-blue) ![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey) ![License](https://img.shields.io/badge/License-MIT-green)

## 🎮 Game Features

- **Pure ASCII Graphics** - Beautiful colorful terminal display with fire & brimstone theme
- **HARDCORE MODE** - One hit and you're out! Ultimate survival challenge
- **Progressive Difficulty** - Fire stones get faster as you survive longer
- **Power-up System** - 4 different power-ups to help you survive
- **High Score Tracking** - Compete against your best runs
- **Cross-Platform** - Works on Windows, macOS, and Linux
- **Reliable Controls** - Built with pynput for smooth gameplay
- **Dynamic Audio** - Background music and sound effects enhance the experience

## 🚀 Quick Start

### Prerequisites
- **Python 3.6+** - [Download here](https://www.python.org/downloads/)
- **Terminal/Command Prompt** - Any modern terminal

### Installation & Play

#### Option 1: Git Clone (Recommended)
```bash
git clone https://github.com/repl-prithiviraj-jayapal/neruppu-daa.git
cd neruppu-daa
pip install -r requirements.txt
python3 neruppu_daa.py
```

#### Option 2: Direct Download
```bash
# Download neruppu_daa.py to any folder
pip install pynput pygame numpy
python3 neruppu_daa.py
```

### Platform-Specific Setup

#### 🪟 Windows
```cmd
pip install pynput pygame numpy
python neruppu_daa.py
```

#### 🍎 macOS
```bash
pip3 install pynput pygame numpy
python3 neruppu_daa.py
```

#### 🐧 Linux
```bash
pip3 install pynput pygame numpy
python3 neruppu_daa.py
```

**That's it!** Just install the dependencies and you're ready to survive the inferno with full audio! 🔥🎵

## 🕹️ How to Play

### Controls
- **A/D or ← → Arrow Keys** - Move left and right
- **SPACEBAR** - Start game
- **Q** - Quit game
- **R** - Restart after game over

### Objective
**NERUPPU DAA** is a hardcore survival game where you dodge falling fire stones (`o`, `O`, `^`, `v`, `x`, `%`, `&`, `~`) and survive as long as possible while collecting blue power-ups!

### Power-ups
| Symbol | Effect | Duration |
|--------|--------|----------|
| `*` | **Double Points** | 6 seconds |
| `+` | **Shield Boost** | Instant protection |
| `!` | **Slow Motion** | 4 seconds |
| `#` | **Shield** | Until hit |

### Scoring
- **Survival**: +2 points per frame (or +3 with Double Points)
- **Power-ups**: +50 points each
- **Lives**: HARDCORE MODE - One life only!

## 🖥️ Game Screenshots

```
🔥  NERUPPU DAA - HARDCORE MODE 🔥
Score: 1,247 | High: 2,891 | Life: ♥ | Level: 8
Effects: 2X PTS | SHIELD

┌──────────────────────────────────────────────────────────┐
│  o       O           *        ^                          │
│     v        o         %      x                         │
│        &          ~      O             +                │
│              @                                           │
│                               ^    x                    │
│     %              v                        &           │
│                                                         │
└──────────────────────────────────────────────────────────┘
A/D or ←/→ to Move | Q=Quit
```

## 🎯 About NERUPPU DAA

**NERUPPU DAA** is an intense, fiery challenge in this hardcore survival game. The game combines:

- **Unique Gameplay**: Fast-paced fire stone dodging action
- **Hardcore Challenge**: One life only - every move counts!
- **Progressive Difficulty**: The longer you survive, the faster the fire stones fall
- **Fire & Brimstone Theme**: Dodge deadly falling fire stones from above

## 🌟 What Makes This Special

- **Unique Title**: Memorable game name with clear gameplay description
- **Hardcore Mode**: Unlike typical games with multiple lives, this is pure survival
- **Reliable Input**: Built with pynput library for consistent keyboard handling across platforms
- **Progressive Challenge**: Difficulty scales dynamically based on survival time
- **Pure ASCII**: No external graphics - runs anywhere Python runs

## 📁 Files Included

- `neruppu_daa.py` - **Main game file**
- `README.md` - This documentation
- `requirements.txt` - Dependencies (pynput)
- `LICENSE` - MIT License

## 🛠️ Technical Details

- **Language**: Python 3.6+
- **Dependencies**: pynput (for reliable keyboard input)
- **Graphics**: ANSI escape codes for colors and positioning
- **Input**: Cross-platform keyboard handling with pynput
- **Performance**: ~10 FPS smooth gameplay
- **Memory**: Lightweight, minimal resource usage

## 🏆 High Score Challenge

Can you beat **5,000 points** in HARDCORE MODE? Share your high scores and strategies!

Current categories:
- 🥉 **Bronze**: 1,000+ points
- 🥈 **Silver**: 2,500+ points  
- 🥇 **Gold**: 5,000+ points
- 💎 **Diamond**: 10,000+ points
- 🔥 **Inferno Master**: 15,000+ points

## 🐛 Troubleshooting

### Game doesn't start
- Ensure Python 3.6+ is installed: `python3 --version`
- Install dependencies: `pip install pynput pygame numpy`
- Try: `python neruppu_daa.py` (without the 3)

### No sound/audio issues
- Game will run without sound if pygame/numpy aren't installed
- Install audio dependencies: `pip install pygame numpy`
- Audio automatically disabled if installation fails

### Keys don't work
- Make sure terminal window has focus
- pynput should handle keyboard input reliably on all platforms

### Colors don't show
- Use a modern terminal (Windows Terminal, iTerm2, etc.)
- Most terminals support ANSI colors by default

### Permission errors on macOS
- Grant accessibility permissions to Terminal in System Preferences > Security & Privacy > Accessibility

## 🤝 Contributing

Found a bug? Have an idea? Contributions welcome!

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📜 License

MIT License - Feel free to use, modify, and distribute!

## 🎪 About

**NERUPPU DAA** was created as an original terminal-based survival game with hardcore gaming mechanics. The name reflects the intense, fiery challenge players face in this action-packed ASCII adventure.

Perfect example of how modern development tools can create engaging gaming experiences that work across all platforms!

---

**Ready to survive the inferno?** 🔥 Run `python3 neruppu_daa.py` and start dodging those fire stones!