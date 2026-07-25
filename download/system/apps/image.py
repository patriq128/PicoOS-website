import struct

def install():
    return {
        "name": "image",
        "version": "0.1",
        "autor": "ZiDi"
    }


def main(path):
    try:
        with open(path,"rb") as f:

            magic = f.read(4)

            if magic != b"PXI1":
                raise Exception("Not PXI")

            width,height = struct.unpack(">HH", f.read(4))


            for y in range(height):

                for x in range(width):

                    r = f.read(1)[0]
                    g = f.read(1)[0]
                    b = f.read(1)[0]

                    print(
                        f"\033[38;2;{r};{g};{b}m██",
                        end=""
                    )

                print()
    except:
        print(f"File {path} doesn't exist.")