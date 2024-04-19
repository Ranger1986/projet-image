import io
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def detect_jpeg_ghosts(image_path, min_quality=30, max_quality=130, step=5, save_path='diff_images'):
    # Create the directory if it does not exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    # Load the original image
    original = Image.open(image_path)
    original = np.array(original.convert('RGB'))
    
    qualities = range(min_quality, max_quality + 1, step)
    diffs = []

    for quality in qualities:
        # Recompress the image at a different quality
        img_buffer = io.BytesIO()
        original_img = Image.fromarray(original)
        original_img.save(img_buffer, format="JPEG", quality=quality)
        
        # Reload the recompressed image and calculate difference
        recompressed_img = Image.open(img_buffer)
        recompressed = np.array(recompressed_img.convert('RGB'))
        
        # Calculate the sum of squared differences
        diff = np.sum((original - recompressed) ** 2, axis=2)
        diffs.append(diff)

        # Convert the difference image to a PIL Image and ensure it's in RGB mode
        diff_img = Image.fromarray(np.uint8(plt.cm.viridis(diff / np.max(diff)) * 255))
        diff_img = diff_img.convert('RGB')  # Ensure the image is in RGB mode
        diff_img.save(f'{save_path}/diff_quality_{quality}.jpeg')

    # Plotting the differences
    fig, axes = plt.subplots(1, len(diffs), figsize=(20, 10))
    for i, diff in enumerate(diffs):
        ax = axes[i]
        im = ax.imshow(diffs[i], cmap='viridis')
        ax.axis('off')
        ax.set_title(f'Quality {qualities[i]}')
    fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.6)
    plt.show()

    return diffs


if __name__ == "__main__":
    # Usage
    path = '/home/aissa/Desktop/PROJECT COMP/projet-image/Code/hi.jpg'  # Specify the path to your image
    detect_jpeg_ghosts(path)
