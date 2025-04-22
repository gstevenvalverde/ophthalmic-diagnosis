import matplotlib.pyplot as plt
import os


def display_text_file_graphically(file_path, font_size=12):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        plt.figure(figsize=(10, 6))
        plt.text(
            0.5,
            0.5,
            content,
            ha="center",
            va="center",
            wrap=True,
            fontsize=font_size,
            family="monospace",
        )
        plt.axis("off")
        plt.title(f"Contenido de: {os.path.basename(file_path)}")
        plt.show()

    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no existe.")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
