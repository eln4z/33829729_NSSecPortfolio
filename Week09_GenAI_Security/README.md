Week 09 — Generative AI Security and Local Model Testing
Learning Objective

This week examined security issues associated with large language models (LLMs). A locally hosted model was deployed to investigate prompt injection, data poisoning, model extraction and model inversion risks. The aim was to recognise that AI systems can be manipulated through inputs rather than traditional software exploits.

Conceptual Background

LLMs are susceptible to behavioural manipulation because they operate on probabilistic language modelling rather than rule-based logic. Adversaries may coerce models to ignore restrictions, disclose sensitive details, mimic training data or retain maliciously introduced content (Brundage et al., 2020). These threats require governance rather than only technical hardening.

Practical Implementation

Four short scripts interacted with an Ollama-hosted model, each demonstrating a distinct threat category:

Script	Risk Demonstrated
prompt_injection_test.py	Bypassing instructions to reveal internal behaviour
data_poisoning_test.py	Teaching incorrect information through repeated prompts
model_inversion_test.py	Attempting to extract synthetic personal data from model patterns
model_extraction_test.py	Cloning model output behaviour through repeated querying
How to Run the Tools

Install Ollama:

pip install ollama


Download a small model (example):

ollama pull smollm2:1.7b


Run scripts individually:

python prompt_injection_test.py
python data_poisoning_test.py
python model_inversion_test.py
# Week 09 — GenAI Security: Local LLM Red‑Teaming

## Overview

This folder contains a small local red‑team exercise against a locally hosted LLM (example: `smollm2:1.7b` via Ollama). The exercise demonstrates four threat categories: prompt injection, data poisoning, model inversion (privacy), and model extraction.

Files of interest:
- `prompt_injection_test.py` — prompt injection checks
- `data_poisoning_test.py` — simple poisoning/instruction persistence test
- `model_inversion_test.py` — privacy/extraction style queries
- `model_extraction_test.py` — repeated queries to observe extraction patterns

---

## Quick Setup

- Create and activate a Python venv (if you haven't already):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
```

- Install the Python client (for convenience):

```bash
pip install ollama
```

- Install and run the Ollama daemon/CLI (macOS example):

```bash
brew install ollama
# pull a small model (example)
ollama pull smollm2:1.7b
# run the model (keeps process attached)
ollama run smollm2:1.7b
```

Note: the Python client calls the local Ollama HTTP API. If the daemon isn't running, tests will print a helpful error message.

---

## Running The Tests

Run each script from the project root using the venv Python to capture output:

```bash
mkdir -p outputs screenshots/week09
.venv/bin/python prompt_injection_test.py > outputs/prompt_injection_output.txt
.venv/bin/python data_poisoning_test.py > outputs/data_poisoning_output.txt
.venv/bin/python model_inversion_test.py > outputs/model_inversion_output.txt
.venv/bin/python model_extraction_test.py > outputs/model_extraction_output.txt
```

If the Ollama daemon is not running you will see an error similar to:

```
Failed to connect to Ollama. Please check that Ollama is downloaded, running and accessible.
```

---

## Evidence Collection

- Text outputs are saved under: `outputs/` (one file per script).
- Suggested screenshots path: `screenshots/week09/` — capture:
	- model responding normally (`prompt_injection.png`)
	- prompt injection succeeding/ignoring rules (`prompt_injection_injection.png`)
	- poisoned output (`data_poisoning_poisoned.png`)
	- repeated extraction answers (`model_extraction_attempts.png`)

macOS quick screenshot example (one-shot):

```bash
# capture entire screen to file
screencapture -x screenshots/week09/prompt_injection.png
```

---

## Threats Tested

- **Prompt Injection:** adversarial inputs that try to override system instructions.
- **Data Poisoning:** session or instruction‑level poisoning that influences later responses.
- **Model Inversion / Privacy:** queries attempting to surface personal or training data.
- **Model Extraction:** repeated queries to reproduce or clone model behaviour.

---

## Mitigation Recommendations

- **Input sanitisation:** strip or neutralise suspicious directive‑like tokens before forwarding inputs.
- **Output verification:** apply safety filters or classifiers to responses before returning them to users.
- **Rate limiting:** enforce per‑key / per‑IP quotas to slow mass extraction attempts.
- **Monitoring & alerting:** log high‑frequency, near‑duplicate, or cleverly structured prompts and alert for investigation.
- **Access controls & governance:** require authenticated access and maintain usage policies for sensitive models.
- **Supply‑chain verification:** only use models from trusted sources and verify signatures/checksums.
- **Secure fine‑tuning practices:** vet training data for PII, use differential privacy or validation to reduce poisoning risk.
- **Watermarking & telemetry:** watermark model outputs where possible and monitor for cloning attempts.

---

## Short Reflection

Even small local LLMs can be coerced by crafted prompts or influenced by session‑level instructions. The primary failure mode for LLMs is not crashing but obeying — therefore layered controls (sanitisation, verification, monitoring, and governance) are essential.

---

## Files I Edited

- `prompt_injection_test.py`
- `data_poisoning_test.py`
- `model_inversion_test.py`
- `model_extraction_test.py`

---

## Next Steps

- Start the Ollama daemon and re‑run tests to collect `outputs/` and screenshots.
- I can: pull a model and run the daemon locally (requires downloads), parse outputs for concrete examples, and update this README with captured screenshots and excerpts — tell me if you want me to proceed.
