from kernel.boot import main as main_boot

def main():
    while True:
        try:
            main_boot()
        except:
            main_boot()

if __name__ == "__main__":
    main()
