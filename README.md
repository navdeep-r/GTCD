# Googol Test Cheating Detector 🛡️

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A sophisticated AI-powered cheating detection system for online exams and tests that monitors:
- Screen activity (window switching)
- Keyboard shortcuts (potential LLM access attempts)
- Visual attention (face and eye tracking)
- Physical presence (camera monitoring)

## Features ✨

- **Real-time monitoring dashboard**
- **Window activity detection** (flags browser/LLM usage)
- **Keyboard shortcut monitoring** (detects Alt/Cmd key presses)
- **Visual attention tracking** (face position analysis)
- **Alert system** with audible warnings
- **Comprehensive logging** with timestamped events
- **Camera feed integration** with focus zone visualization

## Installation ⚙️

1. Clone the repository:
   ```bash
   git clone https://github.com/NAVDEEP-09coder/GTCD.git
   cd GTCD
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage 🚀

1. Run the application:
   ```bash
   python main.py
   ```

2. System will automatically:
   - Detect and initialize camera
   - Begin monitoring keyboard and window activity
   - Display real-time camera feed with focus zone
   - Log all suspicious activity

3. View detailed logs by clicking "View Full Logs" button

## System Requirements 💻

- **OS**: Windows (Linux/macOS support possible with modifications)
- **Python**: 3.8+
- **Webcam**: Required for visual monitoring
- **Permissions**: Administrator rights recommended for full monitoring

## Screenshots 📸

![Application Interface](screenshots/interface.png)
*Main monitoring interface with camera feed and live logs*

![Alert Example](screenshots/alert.png)
*Example of a cheating detection alert*

## Configuration ⚙️

Modify these parameters in the code for customization:
- `focus_area` in `GoogolCheatingDetectorAI` - Adjust the acceptable face position zone
- `distance` threshold - Change sensitivity for attention deviation
- `cheat_counter` warning frequency - Modify how often audible alerts trigger

## Limitations ⚠️

- Currently optimized for single-monitor setups
- Requires well-lit environment for face detection
- May trigger false positives with certain applications
- Windows-specific sound alerts (winsound)

## License 📜

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing 🤝

Contributions are welcome! Please open an issue or pull request for any improvements.

---

### Directory Structure Recommendation:
```
/GTCD
│   main.py                # Main application code
│   requirements.txt       # Python dependencies
│   README.md              # Project documentation
│   LICENSE                # License file
│
└───screenshots/           # Folder for application screenshots
        interface.png
        alert.png
```