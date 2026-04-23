# SKILL: TADA — Text-Acoustic Dual Alignment TTS
**Source:** https://github.com/HumeAI/tada
**Domain:** ai-tools
**Trigger:** Use when implementing high-fidelity text-to-speech, building voice interfaces, generating expressive speech from text in Python, or integrating open-source TTS models with natural prosody.

## Summary
TADA (Text-Acoustic Dual Alignment) by Hume AI is an open-source speech-language model achieving 1:1 token alignment between text and audio — each autoregressive step covers one text token, dynamically determining duration and prosody. ~9GB model, runs on H100/A100.

## Key Patterns
- 1:1 token alignment: no fixed frame rates, no transcript hallucination
- Dynamic duration synthesis: generates full speech for a text token in one step
- Dual-stream generation: text + speech tokens simultaneously
- Prompt caching: `EncoderOutput.save()` / `EncoderOutput.load()` — encode once, reuse
- bf16 support: `torch_dtype=torch.bfloat16` — ~9GB VRAM (3B model)
- `model.compile()` → ~0.12x RTF on H100

## Usage
When user needs expressive, high-fidelity TTS for voice apps, content creation, or audio generation pipelines.

## Code/Template
```python
pip install hume-tada

from tada import TadaForCausalLM, TadaProcessor
model = TadaForCausalLM.from_pretrained("HumeAI/tada-3b", torch_dtype=torch.bfloat16)
processor = TadaProcessor.from_pretrained("HumeAI/tada-3b")

inputs = processor(text="Hello world!", return_tensors="pt")
audio = model.generate(**inputs, max_new_tokens=500)
```
