import math

from typing import List

import segno

CHARACTERS = {
    (False, False): " ",
    (False, True): "▄",
    (True, False): "▀",
    (True, True): "█",
}


def print_qr(qr: segno.QRCode) -> None:
    """Print a single QR code in the terminal."""
    print()
    for half_row in range(math.ceil(len(qr.matrix) / 2)):
        for col in range(len(qr.matrix)):
            upper = bool(qr.matrix[half_row * 2][col])
            lower = (
                False
                if half_row * 2 + 1 >= len(qr.matrix)
                else qr.matrix[half_row * 2 + 1][col]
            )
            print(CHARACTERS[(upper, lower)], end="")
        print()


def show_qrs(urls: List[str]) -> None:
    for url in urls:
        qr = segno.make_qr(url)
        print_qr(qr)
