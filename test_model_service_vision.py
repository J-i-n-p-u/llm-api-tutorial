from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
from pathlib import Path

from openai import APIConnectionError, APIError, APIStatusError, APITimeoutError, OpenAI


ROOT = Path(__file__).resolve().parent
DEFAULT_IMAGE = ROOT / "test_images" / "construction_site.png"
DEFAULT_MODEL = "gpt-5.5"
MODELS_FILE = ROOT / "available_models.json"
API_KEY_PLACEHOLDERS = {"PASTE_YOUR_API_KEY_HERE", "YOUR_API_KEY_HERE"}
DEFAULT_PROMPT = (
    "Describe the image, then summarize it in three bullet points."
)
EXAMPLES = f"""examples:
  python .\\test_model_service_vision.py --list-models
  python .\\test_model_service_vision.py --model {DEFAULT_MODEL}
  python .\\test_model_service_vision.py --model gemini-2.5-flash
  python .\\test_model_service_vision.py --model claude-sonnet-4-6
  python .\\test_model_service_vision.py --model deepseek-v4-pro
  python .\\test_model_service_vision.py --model glm-5.1 --prompt "Describe the image, then summarize it in three bullet points."
  python .\\test_model_service_vision.py --model gpt-5.5 --image .\\test_images\\drawing1.png
  python .\\test_model_service_vision.py --model gpt-5.5 --output .\\example_outputs\\my_run.txt
"""


def load_env_file(path: Path) -> None:
    """Load simple KEY=VALUE pairs without requiring python-dotenv."""
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def configure_console_encoding() -> None:
    """Use UTF-8 so model responses with symbols do not crash Windows terminals."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def image_to_data_url(image_path: Path) -> str:
    mime_type = mimetypes.guess_type(image_path.name)[0] or "image/png"
    image_b64 = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{image_b64}"


def load_available_models(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []

    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("models", [])


def format_available_models() -> str:
    models = load_available_models(MODELS_FILE)
    if not models:
        return f"No available models file found at {MODELS_FILE}"

    lines: list[str] = []
    current_provider = None
    for model in models:
        provider = model.get("provider", "Unknown")
        if provider != current_provider:
            if current_provider is not None:
                lines.append("")
            lines.append(f"{provider}:")
            current_provider = provider
        lines.append(f"  {model['id']}")

    return "\n".join(lines)


def save_text(output_path: Path, text: str) -> Path:
    path = output_path if output_path.is_absolute() else ROOT / output_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return path


def main() -> int:
    configure_console_encoding()
    load_env_file(ROOT / ".env")

    parser = argparse.ArgumentParser(
        description="Test the OpenAI-compatible model service with a local image.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EXAMPLES,
    )
    parser.add_argument(
        "--image",
        type=Path,
        default=DEFAULT_IMAGE,
        help=f"Image file to send. Relative paths are resolved from this folder. Default: {DEFAULT_IMAGE.name}",
    )
    parser.add_argument(
        "--prompt",
        default=DEFAULT_PROMPT,
        help="Question or instruction to send with the image.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model id to call. Use --list-models to see examples. Default: {DEFAULT_MODEL}",
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="Print model ids copied from the provider website screenshots.",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("MODEL_SERVICE_BASE_URL", "https://model.service-inference.ai/v1"),
        help="OpenAI-compatible API base URL. Usually set this in .env.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional text file where the model response or model list will be saved.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=120.0,
        help="Request timeout in seconds. Default: 120.",
    )
    args = parser.parse_args()

    if args.list_models:
        output = format_available_models()
        print(output)
        if args.output:
            saved_path = save_text(args.output, output)
            print(f"\nSaved output to {saved_path}")
        return 0

    api_key = os.environ.get("MODEL_SERVICE_API_KEY")
    if not api_key or api_key in API_KEY_PLACEHOLDERS:
        print(
            "Missing MODEL_SERVICE_API_KEY. Replace the placeholder in .env or set it as an environment variable.",
            file=sys.stderr,
        )
        return 1

    image_path = args.image if args.image.is_absolute() else ROOT / args.image
    if not image_path.exists():
        print(f"Image not found: {image_path}", file=sys.stderr)
        return 1

    client = OpenAI(api_key=api_key, base_url=args.base_url, timeout=args.timeout)

    try:
        response = client.chat.completions.create(
            model=args.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": args.prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": image_to_data_url(image_path)},
                        },
                    ],
                }
            ],
        )
    except APIConnectionError as exc:
        print(
            "Could not connect to the model service. Check your network, VPN, and MODEL_SERVICE_BASE_URL.",
            file=sys.stderr,
        )
        print(f"Details: {exc}", file=sys.stderr)
        return 1
    except APITimeoutError:
        print(
            f"The request timed out after {args.timeout} seconds. Try again or increase --timeout.",
            file=sys.stderr,
        )
        return 1
    except APIStatusError as exc:
        print(
            f"The model service returned HTTP {exc.status_code}. Check the model id, image support, and API key.",
            file=sys.stderr,
        )
        print(f"Details: {exc.message}", file=sys.stderr)
        return 1
    except APIError as exc:
        print(f"The model service returned an API error: {exc}", file=sys.stderr)
        return 1

    output = response.choices[0].message.content or ""
    print(output)
    if args.output:
        saved_path = save_text(args.output, output)
        print(f"\nSaved output to {saved_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
