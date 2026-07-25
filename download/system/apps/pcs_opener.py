def install():
    return {
        "name": "pcs_opener",
        "version": "0.1",
        "autor": "ZiDi"
    }

def main(file):
    from zipfile import ZipFile
    zip_path = f"{file}.psc"
    output_folder = f"/apps/{file}"

    with ZipFile(zip_path, "r") as archive:
        archive.extractall(output_folder)

    print("Extracted!")