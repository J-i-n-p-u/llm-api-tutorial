# Model Service API Tutorial

This folder is a small, student-friendly tutorial for making an API call to an
OpenAI-compatible model service. The main script sends a local image to a model
and prints the model's answer.

We are using an API provider from [TokenMart](https://thetokenmart.ai/). The
core workflow is the same as calling OpenAI's API or Anthropic's API: create a
client with an API key and base URL, choose a model id, send messages, and read
the response.

If you are already comfortable calling OpenAI or Anthropic APIs, you probably do
not need this tutorial. The main things you need are the API key, base URL, and
model id.

Minimal OpenAI-style example:

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://model.service-inference.ai/v1",
)

response = client.chat.completions.create(
    model="gpt-5.5",
    messages=[{"role": "user", "content": "Hello!"}],
)

print(response.choices[0].message.content)
```

Minimal Anthropic-style example:

```python
from anthropic import Anthropic

client = Anthropic(
    api_key="YOUR_API_KEY",
    base_url="https://model.service-inference.ai",
)

message = client.messages.create(
    model="gpt-5.5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}],
)

print(message.content[0].text)
```

If any part of this workflow is unfamiliar, you can paste this repo link, this
README, or a specific command into ChatGPT or another large language model and
ask it to explain the API call step by step.

By the end, you should be able to:

- clone this repo to your own computer;
- set up a Python environment;
- keep your API key outside the code;
- choose a model id;
- send an image plus a prompt to the API;
- save an example response to a file.

The main file is `test_model_service_vision.py`.

## 1. Clone This Repo

First, clone this repository to your computer and enter the folder:

```powershell
git clone https://github.com/J-i-n-p-u/llm-api-tutorial.git
cd llm-api-tutorial
```

All commands below should be run from this folder.

## 2. Set Up Python

Use either `venv` or `conda`. You only need one of these options.

### Option A: venv

Run these commands from this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Option B: conda

This creates a conda environment named `llm-api-tutorial` and installs the
required package:

```powershell
conda env create -f environment.yml
conda activate llm-api-tutorial
```

If you already have a Python environment, just install the dependency:

```powershell
python -m pip install -r requirements.txt
```

## 3. Add Your API Key

This public repo includes a placeholder `.env` file for class setup. Replace the
placeholder with your real API key on your own machine:

```env
MODEL_SERVICE_API_KEY=PASTE_YOUR_API_KEY_HERE
MODEL_SERVICE_BASE_URL=https://model.service-inference.ai/v1
```

After you add a real key, keep that modified `.env` private. Do not paste the
API key into the Python script, a notebook, a README file, or a public commit.

## 4. Check The Model List

Before making an API call, list the model ids:

```powershell
python .\test_model_service_vision.py --list-models
```

The same list is also saved in:

- `available_models.json` for code;
- `AVAILABLE_MODELS.md` for reading.

Use the model id exactly as printed.

## 5. Run Your First API Call

Run the default example:

```powershell
python .\test_model_service_vision.py
```

The script sends `test_images/construction_site.png` to the default model,
`gpt-5.5`, with this prompt:

```text
Describe the image, then summarize it in three bullet points.
```

To save the response, add `--output`:

```powershell
python .\test_model_service_vision.py --output .\example_outputs\my_first_run.txt
```

## 6. Try Different Models And Images

The examples below use the same basic pattern:

```powershell
python .\test_model_service_vision.py --model MODEL_ID --prompt "YOUR PROMPT" --image .\test_images\IMAGE_NAME.png
```

GPT example:

```powershell
python .\test_model_service_vision.py --model gpt-5.5 --prompt "Describe the image, then summarize it in three bullet points." --image .\test_images\construction_site.png
```

Claude example:

```powershell
python .\test_model_service_vision.py --model claude-sonnet-4-6 --prompt "Describe the image, then summarize it in three bullet points." --image .\test_images\drawing1.png
```

Gemini example:

```powershell
python .\test_model_service_vision.py --model gemini-2.5-flash --prompt "Describe the image, then summarize it in three bullet points." --image .\test_images\construction_site.png
```

Qwen example. This provider can be slower, so this command includes an explicit
timeout:

```powershell
python .\test_model_service_vision.py --model qwen3.5-plus --prompt "Describe the image, then summarize it in three bullet points." --image .\test_images\drawing2.png --timeout 60
```

Kimi example:

```powershell
python .\test_model_service_vision.py --model Kimi-K2.5 --prompt "Describe the image, then summarize it in three bullet points." --image .\test_images\drawing3.png
```

DeepSeek example:

```powershell
python .\test_model_service_vision.py --model deepseek-v4-pro --prompt "Describe the image, then summarize it in three bullet points." --image .\test_images\drawing4.png
```

GLM example:

```powershell
python .\test_model_service_vision.py --model glm-5.1 --prompt "Describe the image, then summarize it in three bullet points." --image .\test_images\drawing5.png
```

Override the API base URL from the command line:

```powershell
python .\test_model_service_vision.py --base-url https://model.service-inference.ai/v1 --model gpt-5.5 --prompt "Describe the image, then summarize it in three bullet points." --image .\test_images\construction_site.png
```

## 7. Example Outputs

Verified example outputs are stored in `example_outputs/`. They show what the
commands above looked like when they were run, without exposing the API key. See
`example_outputs/README.md` for the file index and notes about model-specific
behavior.

API responses can vary from run to run, so your wording may not match the files
exactly. That is normal.

## Test Images

All included images are in `test_images`:

- `construction_site.png`
- `drawing1.png`
- `drawing2.png`
- `drawing3.png`
- `drawing4.png`
- `drawing5.png`

## Command Reference

Useful arguments:

- `--list-models`: print the known model ids;
- `--model`: choose which model id to call;
- `--prompt`: change the instruction sent with the image;
- `--image`: choose a local image file;
- `--output`: save the printed result to a text file;
- `--base-url`: override `MODEL_SERVICE_BASE_URL`;
- `--timeout`: increase the request timeout if the service is slow.

You can always see the command-line help:

```powershell
python .\test_model_service_vision.py --help
```

## Common Problems

`Missing MODEL_SERVICE_API_KEY`

Your `.env` file is missing or still has the placeholder value. Copy
`.env.example` to `.env` and paste the real key.

`Image not found`

Check that the image path exists. The included images are all inside
`test_images`.

`HTTP 401` or `HTTP 403`

The API key may be missing, expired, or not allowed to use this service.

`HTTP 404` or model errors

The model id may be wrong, unavailable, or not enabled for your account. Run
`--list-models` again and copy the id exactly.

`The model rejects the image request`

Some listed models may not support image input. Try `gpt-5.5`,
`gemini-2.5-flash`, or another vision-capable model from the provider.
