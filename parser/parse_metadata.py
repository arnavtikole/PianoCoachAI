import xml.etree.ElementTree as ET

def get_title(root):
    work = root.find("work")

    if work is None:
        return None

    title = work.find("work-title")

    if title is None:
        return None

    return title.text

def get_composer(root):
    identification = root.find("identification")

    if identification is None:
        return None

    for creator in identification.findall("creator"):
        if creator.get("type")=="composer":
            return creator.text

    return None

def get_tempo(root):
    for sound in root.iter("sound"):
        tempo = sound.get("tempo")

        if tempo is not None:
            return float(tempo)

    return None

