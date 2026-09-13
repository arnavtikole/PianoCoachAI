import tempfile
from pathlib import Path


def save_uploaded_file(uploaded_file):
    file_extension = Path(uploaded_file.name).suffix

    with tempfile.NamedTemporaryFile(delete=False,suffix=file_extension,) as temp:
        temp.write(uploaded_file.getbuffer())

    return temp.name