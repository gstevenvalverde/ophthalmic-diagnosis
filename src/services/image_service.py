import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os


def display_image(image_path):
    if not os.path.exists(image_path):
        print(f"Error: La ruta '{image_path}' no existe.")
        return

    try:
        img = mpimg.imread(image_path)
        plt.figure(figsize=(8, 6))
        plt.imshow(img)
        plt.axis("off")
        plt.title(f"Visualización: {os.path.basename(image_path)}")
        plt.show()
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
