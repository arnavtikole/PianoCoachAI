import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from .models import Score
from .parse_metadata import (get_title,get_composer,get_tempo)
from .parse_measures import parse_measure


def parse_score(xml_file):
    xml_file = Path(xml_file)

    if xml_file.suffix.lower() == ".mxl":
        with zipfile.ZipFile(xml_file, "r") as archive:
            container = ET.fromstring(archive.read("META-INF/container.xml"))
            rootfile = container.find(".//rootfile").get("full-path")
            root = ET.fromstring(archive.read(rootfile))

    else:
        tree = ET.parse(xml_file)
        root = tree.getroot()

    title = get_title(root)
    composer = get_composer(root)
    tempo = get_tempo(root)

    measures = []

    state = {
        "divisions": None,
        "beats_per_measure": None,
        "beat_unit": None,
        "key_sig": None,
        "current_beat": 1.0
    }

    for part in root.findall("part"):
        for measure_element in part.findall("measure"):
            measures.append(parse_measure(measure_element,state))

    return Score(title=title,composer=composer,tempo=tempo,measures=measures)

