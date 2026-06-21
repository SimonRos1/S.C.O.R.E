from __future__ import annotations

import base64
import json
import sys
from pathlib import Path


def read_text_sidecar(image_path: Path) -> str:
    sidecar_path = image_path.with_suffix(".txt")
    if sidecar_path.exists():
        return sidecar_path.read_text(encoding="utf-8").strip()
    return ""


def encode_image_file(image_path: Path) -> dict[str, str]:
    image_bytes = image_path.read_bytes()
    image_base64 = base64.b64encode(image_bytes).decode("ascii")
    return {
        "file": image_path.name,
        "image_base64": image_base64,
        "text": read_text_sidecar(image_path),
    }


def collect_inputs(input_path: Path) -> list[Path]:
    if input_path.is_file():
        return [input_path]

    if input_path.is_dir():
        return [path for path in sorted(input_path.iterdir()) if path.is_file()]



def main() -> int:
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("output.json")

    files = collect_inputs(input_path)
    payload = {"output": [encode_image_file(file_path) for file_path in files]}

    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())