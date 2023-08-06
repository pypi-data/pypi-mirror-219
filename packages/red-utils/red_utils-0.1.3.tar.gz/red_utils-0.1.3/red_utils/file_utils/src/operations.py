from __future__ import annotations

from datetime import datetime
import json

from pathlib import Path
import time
from typing import Any, Union

from .constants import default_json_dir, ts


def export_json(
    input: Union[str, list[list, dict], dict[str, Any]] = None,
    output_dir: str = default_json_dir,
    output_filename: str = f"{ts()}_unnamed_json.json",
):
    if not Path(output_dir).exists():
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    if isinstance(input, dict):
        input = json.dumps(input)

    if Path(f"{output_dir}/{output_filename}").exists():
        raise FileExistsError(
            f"JSON file already exists: {output_dir}/{output_filename}"
        )

    if output_dir.endswith("/"):
        output_dir = output_dir[:-1]

    if not output_filename.endswith(".json"):
        output_filename = f"{output_filename}.json"

    output_path: str = f"{output_dir}/{output_filename}"

    print(f"Output path: {output_path}")

    if not Path(output_path).exists():
        try:
            with open(output_path, "w+") as f:
                f.write(input)
        except FileExistsError as file_exists_exc:
            raise FileExistsError(file_exists_exc)
        except FileNotFoundError as file_not_found_exc:
            raise FileNotFoundError(file_not_found_exc)
        except Exception as exc:
            raise Exception(
                f"Unhandled exception writing JSON to file: {output_path}. Details: {exc}"
            )
