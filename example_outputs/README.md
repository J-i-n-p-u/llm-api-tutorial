# Example Outputs

These files were generated on 2026-05-19 by running the commands from the root
README. They are included so students can compare their own terminal output with
a known successful run.

The API key is loaded from `.env` at runtime and is not printed or stored here.

Model responses are not deterministic, so your exact wording may differ.

## Files

| File | What it shows |
| --- | --- |
| `help.txt` | Output from `python .\test_model_service_vision.py --help`. |
| `available_models.txt` | Output from `python .\test_model_service_vision.py --list-models`. |
| `default_gpt-5.5_construction_site.txt` | Default model, default prompt, default construction image. |
| `my_first_run.txt` | Same default call, saved with the README `--output` example. |
| `gpt-5.5_construction_site.txt` | GPT example on `construction_site.png`. |
| `claude-sonnet-4-6_drawing1.txt` | Claude example on `drawing1.png`. |
| `gemini-2.5-flash_construction_site.txt` | Gemini example on `construction_site.png`. |
| `qwen3.5-plus_drawing2.txt` | Qwen example on `drawing2.png`. The first run was slow, so this saved run used `--timeout 60`. |
| `Kimi-K2.5_drawing3.txt` | Kimi example on `drawing3.png`. |
| `deepseek-v4-pro_drawing4.txt` | DeepSeek example on `drawing4.png`. |
| `glm-5.1_drawing5.txt` | GLM example on `drawing5.png`. It returned text saying no image was attached, which suggests this model or endpoint did not process the image input. |
| `base-url_gpt-5.5_construction_site.txt` | GPT example with the base URL passed explicitly through `--base-url`. |

## Notes For Students

If your call succeeds but the answer is worded differently, that is normal.

If a model says it cannot see the image, your code may still be correct. Some
models listed by a provider do not support image input through the same endpoint.
Try a model that is known to handle vision input, such as the successful GPT,
Claude, Gemini, Kimi, DeepSeek, or Qwen examples above.

If a request is slow, try adding a timeout:

```powershell
python .\test_model_service_vision.py --model qwen3.5-plus --image .\test_images\drawing2.png --timeout 60
```
