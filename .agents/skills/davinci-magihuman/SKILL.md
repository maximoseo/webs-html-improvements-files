# SKILL: daVinci-MagiHuman — Audio-Video Generation Model
**Source:** https://github.com/GAIR-NLP/daVinci-MagiHuman
**Domain:** code
**Trigger:** When generating human-centric audio-video content from text prompts using a 15B transformer

## Summary
Single-stream 15B-parameter Transformer jointly processing text, video, and audio via self-attention only. Generates 5-second 256p video in 2 seconds on H100. Multilingual, SOTA on human evaluation.

## Key Patterns
- Single-stream architecture: no cross-attention, no multi-stream complexity
- Two-stage pipeline: generate at low resolution, refine in latent space (super-resolution)
- DMD-2 distillation: 8 denoising steps, no CFG
- T2V (text-to-video) or TI2V (text+image-to-video) modes

## Usage
Use for AI video generation research or applications requiring high-quality human motion, speech, and audio-video sync.

## Code/Template
```bash
docker pull sandai/magi-human:latest
docker run -it --gpus all --network host --ipc host \
  -v /path/to/repos:/workspace -v /path/to/checkpoints:/models \
  sandai/magi-human:latest bash
# Then: git clone + pip install + download checkpoints from HuggingFace
# python inference.py --prompt "..." --config example/t2v/config.json
```
