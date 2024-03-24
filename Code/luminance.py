"""Réalise la luminance d'une image"""
import numpy as np

def luminance(image: np.ndarray)->np.ndarray:
    image_luminance = np.empty(image.shape[:2],np.uint8)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
                image_luminance[i,j]=float(image[i,j,0])*0.299+float(image[i,j,1])*0.587+float(image[i,j,2])*0.114

    return image_luminance
                
# Exemple d'utilisation
if __name__ == "__main__":
    from file_manipulation import read_image, write_image
    image_path = "../Image/splicing-01.png"
    output_path = "splicing-01.png"
    image = read_image(image_path)
    img_lum=luminance(image)
    write_image(img_lum,output_path)