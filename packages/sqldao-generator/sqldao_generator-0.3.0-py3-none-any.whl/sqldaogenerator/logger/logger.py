from datetime import datetime


def info(text: str):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} INFO {text}")
