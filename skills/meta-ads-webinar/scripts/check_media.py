import argparse
import json
import subprocess
from pathlib import Path


def inspect_media(expected_ratio, filename):
    path = Path(filename).resolve(strict=True)
    width_ratio, height_ratio = map(int, expected_ratio.split(":"))
    if width_ratio <= 0 or height_ratio <= 0 or not path.is_file():
        raise ValueError("Zadejte soubor a kladný poměr stran, například 4:5.")
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(path)],
        capture_output=True, text=True, timeout=30,
    )
    if probe.returncode:
        raise ValueError(f"Soubor {path.name} se nepodařilo přečíst.")
    streams = json.loads(probe.stdout)["streams"]
    visuals = [
        stream for stream in streams
        if stream["codec_type"] == "video" and not stream.get("disposition", {}).get("attached_pic")
    ]
    if not visuals:
        raise ValueError(f"Soubor {path.name} nemá obrazovou stopu.")
    visual = visuals[0]
    width = visual["width"]
    height = visual["height"]
    rotation = next((item["rotation"] for item in visual.get("side_data_list", []) if "rotation" in item), 0)
    if round(rotation) % 180 == 90:
        width, height = height, width
    return {
        "file": path.name,
        "width": width,
        "height": height,
        "expected_ratio": expected_ratio,
        "matches": width * height_ratio == height * width_ratio,
        "has_audio": any(stream["codec_type"] == "audio" for stream in streams),
    }


def main():
    parser = argparse.ArgumentParser(description="Ověř poměry stran a přítomnost zvuku v podkladech.")
    parser.add_argument("--asset", action="append", nargs=2, metavar=("POMĚR", "SOUBOR"), required=True)
    try:
        result = [inspect_media(ratio, filename) for ratio, filename in parser.parse_args().asset]
    except FileNotFoundError as error:
        parser.exit(1, f"Chybí ffprobe nebo zadaný soubor ({error.filename or error}).\n")
    except (KeyError, TypeError, ValueError, subprocess.TimeoutExpired) as error:
        parser.exit(1, f"{error}\n")
    print(json.dumps(result, ensure_ascii=False))
    if not all(asset["matches"] for asset in result):
        parser.exit(1)


if __name__ == "__main__":
    main()
