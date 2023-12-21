import os
import sys
import scan
import shutil
import normalize
from pathlib import Path


def handle_file(path, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize.normalize(path.name))


def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    del_folder = root_folder/path
    new_name = normalize.normalize(path.name.replace(".zip", '').replace(".tar", '').replace(".gz", ''))

    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))

    except OSError:
        shutil.rmtree(archive_folder)
        os.remove(del_folder)
        return

    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def main(folder_path):
    print(folder_path)
    scan.scan(folder_path)


       # відеофайли ('AVI', 'MP4', 'MOV', 'MKV')
    for files in scan.video:
        for file in files:
            handle_file(file, folder_path, "video")

        # музика ('MP3', 'OGG', 'WAV', 'AMR')
    for files in scan.audio:
        for file in files:
            handle_file(file, folder_path, "audio")

        # зображення ('JPEG', 'PNG', 'JPG', 'SVG')
    for files in scan.images:
        for file in files:
            handle_file(file, folder_path, "images")

        # документи ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
    for files in scan.documents:
        for file in files:
            handle_file(file, folder_path, "documents")

        # архіви ('ZIP', 'GZ', 'TAR')
    for files in scan.archives:
        for file in files:
            handle_archive(file, folder_path, "archives")
        # усі інші файли
    for file in scan.others:
        handle_file(file, folder_path, "others")

    remove_empty_folders(folder_path)


if __name__ == '__main__':
    path = sys.argv[1]
    print(f'Start in {path}')

    
    folder = Path(path)
    main(folder.resolve())

    with open(f"{path}/Resume.txt", 'w+', encoding='utf-8') as file:
        file.write("Video: {}\n".format(" *|* ".join(([file.name for files in scan.video for file in files]))))
        file.write("Audio: {}\n".format(" *|* ".join(([file.name for files in scan.audio for file in files]))))
        file.write("Images: {}\n".format(" *|* ".join(([file.name for files in scan.images for file in files]))))
        file.write("Documents: {}\n".format(" *|* ".join(([file.name for files in scan.documents for file in files]))))
        file.write("Archives: {}\n".format(" *|* ".join(([file.name for files in scan.archives for file in files]))))
        file.write("Others: {}\n".format(" *|* ".join(([file.name for file in scan.others]))))
        file.write("Known extensions: {}\n".format(scan.extensions))
        file.write("Unknown extensions: {}\n".format(scan.unknown))
 