import pathlib

def main():
    print(pathlib.Path(__file__).parent.absolute())
    print(pathlib.Path().absolute())