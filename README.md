# Technology Detection Tool

This is a Python-based tool that uses `WhatWeb` to detect technologies and gather information about a given target (URL, IP, or CIDR). It parses the output of `WhatWeb` into a structured JSON format for easy analysis.

---

## Features

- **Technology Detection**: Identifies technologies and their versions (e.g., `Apache[2.4.56]`).
- **Detailed Information Extraction**: Gathers information such as HTTP status, title, IP address, country, and plugins.
- **Structured Output**: Converts `WhatWeb` output into a well-structured JSON format.
- **Regex-Based Parsing**: Uses customizable regex patterns for extracting data from raw `WhatWeb` output.

---

## Requirements

- Python 3.7+
- [WhatWeb](https://github.com/urbanadventurer/WhatWeb) installed and accessible in your system's PATH.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/technology-detection-tool.git
   cd technology-detection-tool
   ```

2. Install Python dependencies (if any are added in the future):
   ```bash
   pip install -r requirements.txt
   ```

3. Install `WhatWeb` (if not already installed):
   ```bash
   git clone https://github.com/urbanadventurer/WhatWeb.git
   cd WhatWeb
   sudo ./install.sh
   ```

---

## Usage

Run the script using the following command:

```bash
python technology_detection.py <target>
```

