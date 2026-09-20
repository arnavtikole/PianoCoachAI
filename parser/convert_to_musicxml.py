from pathlib import Path
import subprocess
import os

if os.name == "nt":
    AUDIVERIS_PATH = Path(r"C:\Program Files\Audiveris\Audiveris.exe")
else:
    AUDIVERIS_PATH = Path("/opt/audiveris/bin/Audiveris")

def convert_pdf_to_musicxml(pdf_path):
    pdf_path = Path(pdf_path)

    if not AUDIVERIS_PATH.exists():
        raise FileNotFoundError(f"Audiveris was not found at {AUDIVERIS_PATH}")

    if not pdf_path.exists():
        raise FileNotFoundError(f"{pdf_path} does not exist.")

    result = subprocess.run(
        [
            str(AUDIVERIS_PATH),
            "-batch",
            "-export",
            str(pdf_path)
        ],
        capture_output=True,
        text=True,
    )

    print("STDOUT:")
    print(result.stdout)

    print("STDERR:")
    print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(f"Audiveris failed:\n{result.stderr}")

    musicxml = pdf_path.with_suffix(".mxl")

    if not musicxml.exists():
        musicxml = pdf_path.with_suffix(".xml")

    if not musicxml.exists():
        raise FileNotFoundError("Audiveris did not create a MusicXML file.")

    return musicxml