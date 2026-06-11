from gui import gui_launch

def launch():
    try:
        print("GUI launching...\n")
        gui_launch()
    except Exception as e:
        print(f"It was not possible to load GUI due to error: {e}")

if __name__ == "__main__":
    launch()