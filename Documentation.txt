# Automatic Speech Recognition

## Overview
We are utilizing the **Whisper CPP** open-source library for real-time transcription.

### Why Whisper CPP?
- **Lightweight & Dependency-Free**: Minimal setup required.
- **Efficient Processing**: Optimized performance for real-time applications.
- **C-style API**: Simplifies integration across various platforms.
- **Multilingual Support**: Dynamically detects languages during runtime.
- **Accuracy & Robustness**: Maintains high transcription precision.

## Considered Alternatives
We evaluated **VOSK** but found that:
- It lacks a **unified model** for multilingual transcription.
- Requires separate models for different languages.
- Unable to **auto-detect** language during runtime.

Thus, Whisper CPP was selected for its ability to **identify audio language dynamically** without requiring predefined models.

## Chosen Model in Whisper CPP
We are using **ggml-small-q8_0**, a quantized version of the small model. Below are key differences:

| Feature           | ggml-small.bin (Full Precision) | ggml-small-q8_0.bin (Quantized) |
|-------------------|--------------------------------|----------------------------------|
| **Weight Precision** | FP32 or FP16 | 8-bit integers (q8_0 quantization) |
| **File Size** | Large | Smaller |
| **Accuracy** | Highest (reference) | Very close to full precision, minimal loss |
| **Inference Speed** | Slower | Faster |
| **Memory Usage** | High | Lower |
| **Use Case** | Maximum accuracy with abundant resources | Balanced accuracy, speed & lower memory footprint |

In essence, `ggml-small-q8_0.bin` is a compressed version optimized for performance and reduced CPU load, with **minimal accuracy trade-off**. For most real-time applications, **q8_0** or **q5_k_m** models are highly recommended.

## Setting Up Whisper CPP
### Commands for Installation:
```sh
cmake . --fresh
msbuild ALL_BUILD.vcxproj /p:Configuration=Release

Download Model:
curl <model download url> -o models/<model-name>.bin

Running Whisper CPP:
.\whisper-cli -m models/<model-name>.bin -f samples/<audio>.mp3 -t 8
.\whisper-cli -m models/ggml-small-q8_0.bin -f samples/<audio>.mp3 -l auto -t 4

Here, -t 4 specifies the use of 4 CPU threads for transcription.

Gen-AI Component
(Reserved space for Gen-AI-related content 🚀)