# BMP Image Processor

A Python tool for processing BMP images with real-time manipulation capabilities. Read metadata, adjust colors, resize, and modify images interactively.

![Example Processing Pipeline](images/example1.png)  
*Original image (left) and processed version with blue channel removed (right)*

## Features

- **Metadata Extraction**:
  - Display image width, height, and dimensions
  - Show file size and color depth (bits per pixel)
  - Read BMP header information

- **Image Manipulation**:
  - Color channel removal (R/G/B)
  - Brightness adjustment via YUV conversion
  - Image scaling/resizing
  - Real-time preview of changes

- **Performance**:
  - Efficient pixel-level operations
  - Interactive processing feedback

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/bmp-processor.git
   cd bmp-processor
   ```
2. Install dependencies:
   ```bash
    pip install -r requirements.txt
   ```
3. Run:
    ```bash
    python main.py    
    ``` 