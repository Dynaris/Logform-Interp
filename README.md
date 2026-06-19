# Logform Interp

Logform Interp is a Python desktop application that combines dictionary-based log parsing with a locally hosted Large Language Model (LLM) - currently supporting Ollama as the local LLM provider - to generate structured troubleshooting reports from log files.

The application identifies potentially relevant log entries, submits the findings to a local AI model through Ollama, and produces summaries, likely causes, recommended actions, and confidence estimates.

Currently, the public demo supports `.log` and `.txt` files. For best results, use a model with at least 14 billion parameters, such as `qwen2.5:14b`.

## Disclaimer

- This software is provided for personal and educational use only. The author assumes no responsibility or liability for any loss or damage resulting from the use of the information provided by this tool.

- If you have any doubts about a troubleshooting, ensure you take the appropriate caution and see your local technician.

- Issues and pull requests may not be reviewed promptly, as this is a fun project of mine.

## Demo

![Logform Interp Demo](src/video_demo/GIF_demonstration.gif)

Full video [here](https://github.com/user-attachments/assets/a61ae1e8-9f8a-414c-be84-da6f9a7de441) or in `src/video_demo`.


## Installation

Download your preferred Ollama model:

1. Follow the installation instructions for Ollama [by clicking here](https://o2llama.com/download);
2. Download preferred model: 

    - If using **Linux**:
    ```bash
    ollama pull [full model name]
    ```
    - Example:
    ```bash
    ollama pull qwen2.5:14b
    ```
    - If using **Windows**, follow the installation path provided by the executable.

3. Open `src/LLM/config.py` and configure `OLLAMA_MODEL`.

Clone the repository:

```bash
git clone https://github.com/Dynaris/Logform-Interp.git
cd logform-interp
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

- Linux/macOS:
    ```bash
    source .venv/bin/activate
    ```

- Windows:
    ```bash
    .venv\Scripts\activate
    ```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage/Examples

```bash
python main.py
```

or if you use UV:

```bash
uv run main.py
```

## Features

- Log file validation
- Dictionary-based log parsing
- Local LLM integration through Ollama
- Structured troubleshooting reports
- Keyword-based issue detection
- Support for `.txt` and `.log` files

## Tech Stack

- Python 3
- Tkinter
- Ollama

## Contributing

Given the current project status and end goal, no contributions are being accepted at the moment.


## License
See the [LICENSE](./LICENSE) file for full details.  

