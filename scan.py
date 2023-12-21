import sys
from pathlib import Path


category_files = {
    'video': ('AVI', 'MP4', 'MOV', 'MKV'),
    'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
    'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
    'archives': ('ZIP', 'GZ', 'TAR'), }

registered_extensions = {}
video = []
audio = []
documents = []
images = []
archives = []
folders = list()
archives = list()
others = list()
unknown = set()
extensions = set()


for key,value in category_files.items():
    for exten in value:
        globals()[f"{key}_{exten.lower()}_files"] = list()
        registered_extensions.update(zip([exten], [globals()[f"{key}_{exten.lower()}_files"]]))
        
        video.append(globals()[f"{key}_{exten.lower()}_files"]) if key == "video" else ...
        audio.append(globals()[f"{key}_{exten.lower()}_files"]) if key == "audio" else ...
        documents.append(globals()[f"{key}_{exten.lower()}_files"]) if key == "documents" else ...
        images.append(globals()[f"{key}_{exten.lower()}_files"]) if key == "images" else ...
        archives.append(globals()[f"{key}_{exten.lower()}_files"]) if key == "archives" else ...


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('video', 'audio', 'images', 'documents', 'archives',  'others'):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        
        if not extension:
            others.append(new_name)
        
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
        
            except KeyError:
                unknown.add(extension)
                others.append(new_name)


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    folder = Path(path)

    scan(folder)
