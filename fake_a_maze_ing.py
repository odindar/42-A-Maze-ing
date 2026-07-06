# sahte (dummy) veri.
# 1 = Duvar, 0 = Yol, 2 = Giriş (Entry), 3 = Çıkış (Exit)
DUMMY_MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 1, 0, 0, 0, 3, 1],
    [1, 1, 0, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1]
]

def render_ascii(maze_data: list[list[int]]) -> None:

    for row in maze_data:
        row_string = ""
        for cell in row:
            if cell == 1:
                row_string += "██"  # Duvar için dolu blok
            elif cell == 0:
                row_string += "  "  # Yol için iki boşluk
            elif cell == 2:
                row_string += "G"  # Start (Giriş)
            elif cell == 3:
                row_string += "C"  # Exit (Çıkış)
        print(row_string)

if __name__ == "__main__":
    print("=== Sahte ===")
    render_ascii(DUMMY_MAZE)