import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageOps, ImageChops, ImageEnhance
import numpy as np
import math

from io import BytesIO
from skimage.feature import graycomatrix, graycoprops
from skimage.color import rgb2hsv
from skimage.exposure import histogram
from joblib import load
from sklearn.svm import SVC

def rgb2gray(rgb):
    gray_image = np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])
    # Ensure the output is of the correct type (unsigned integer)
    gray_image = np.clip(gray_image, 0, 255).astype(np.uint8)
    return gray_image

def convert_to_ela_image(image, quality):
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image.astype('uint8'), 'RGB')
    image = image.convert('RGB')
    byte_stream = BytesIO()
    image.save(byte_stream, 'JPEG', quality=quality)
    byte_stream.seek(0)  
    resaved_image = Image.open(byte_stream)
    resaved_image.load()  
    byte_stream.close()  
    ela_image = ImageChops.difference(image, resaved_image)
    ela_image = ela_image.convert('RGB')
    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    scale = 255.0 / max_diff
    return ImageEnhance.Brightness(ela_image).enhance(scale)


def extract_texture_features(image):
    gray_image = rgb2gray(np.array(image))  # Convert PIL image to numpy array and then to grayscale
    glcm = graycomatrix(gray_image, distances=[5], angles=[0], levels=256, symmetric=True, normed=True)
    features = [graycoprops(glcm, prop).flatten() for prop in ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']]
    return np.hstack(features)

def extract_color_features(image):
    hsv_image = rgb2hsv(np.array(image))
    h_hist, _ = histogram(hsv_image[..., 0], nbins=256)
    s_hist, _ = histogram(hsv_image[..., 1], nbins=256)
    v_hist, _ = histogram(hsv_image[..., 2], nbins=256)
    color_features = np.concatenate([h_hist / h_hist.sum(), s_hist / s_hist.sum(), v_hist / v_hist.sum()])
    return color_features

class ImageProcessorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Processor")

        # Variables
        self.original_image = None
        self.new_image = None

        # Create Widgets
        self.left_image_label = tk.Label(self)
        self.right_image_label = tk.Label(self)
        self.select_image_button = tk.Button(self, text="Select Image", command=self.select_image)
        self.process_button = tk.Button(self, text="Download Image", command=self.download_image)
        self.quit_button = tk.Button(self, text="Quit", command=self.quit)
        self.notebook = tk.ttk.Notebook(self)

        #Notebook1 widget
        self.watermark=tk.Canvas(self, height=0,width=0)
        self.watermark_label=tk.Label(self.watermark, text="Watermark")
        self.watermark_text=tk.Entry(self.watermark, textvariable="Watermark")
        self.watermark_button1=tk.Button(self.watermark, text="Set Watermark", command=self.set_watermark)
        self.watermark_button2=tk.Button(self.watermark, text="Check Watermark", command=self.check_watermark)
        self.watermark_psnr=tk.Label(self.watermark, text="PSNR : ")
        self.notebook.add( self.watermark, text="watermark")

        #Notebook1 Layout
        self.watermark_label.grid(row=0, column=0)
        self.watermark_text.grid(row=0, column=1)
        self.watermark_button1.grid(row=1, column=0)
        self.watermark_button2.grid(row=1, column=1)
        self.watermark_psnr.grid(row=2, column=0, columnspan=2)

        #Notebook1 widget
        self.ML=tk.Canvas(self, height=0,width=0)
        self.ML_button=tk.Button(self.ML, text="Check", command=self.machine_learning)
        self.ML_result=tk.Label(self.ML, text="")
        self.notebook.add( self.ML, text="machine learning")

        #Notebook1 Layout
        self.ML_button.grid(row=0, column=0)
        self.ML_result.grid(row=0, column=1)

        # Layout
        self.left_image_label.grid(row=0, column=0)
        self.right_image_label.grid(row=0, column=1)
        self.select_image_button.grid(row=1, column=0, pady=10)
        self.process_button.grid(row=1, column=1, pady=10)
        self.quit_button.grid(row=3, columnspan=2, pady=10)
        self.notebook.grid(row=2, columnspan=2, pady=10)

        self.select_image()

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.display_image(self.original_image, self.left_image_label)
            self.new_image = Image.open(file_path)
            self.display_image(self.new_image, self.right_image_label)

    def download_image(self):
        if self.new_image:
            file_path = filedialog.asksaveasfile(filetypes=[("Image files", "*.png *.jpg *.jpeg")]).name
            if file_path:
                self.new_image.save(file_path)

    def set_watermark(self):
        image = np.array(self.original_image)
        watermark_bits = "".join(format(ord(char), '08b') for char in self.watermark_text.get())
        watermark_length = len(watermark_bits)
        watermark_iterator = 0
        image_with_watermark = image.copy()
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                for k in range(image.shape[2]):
                    pixel = image[i, j, k]
                    watermark_bit = int(watermark_bits[watermark_iterator])
                    new_pixel = (pixel & 0b11111110) | watermark_bit
                    image_with_watermark[i, j, k] = new_pixel
                    watermark_iterator = (watermark_iterator + 1) % watermark_length
        self.new_image=Image.fromarray(image_with_watermark)
        self.display_image(self.new_image, self.right_image_label)

        mse = np.mean((image - image_with_watermark) ** 2)
        if mse == 0:
            return float('inf')
        max_pixel = 255.0
        psnr_value = 20 * math.log10(max_pixel / math.sqrt(mse))
        self.watermark_psnr["text"]="PSNR : " + str(psnr_value*100//1/100)

    def check_watermark(self):
        image = np.array(self.original_image)
        watermark_bits = "".join(format(ord(char), '08b') for char in self.watermark_text.get())
        watermark_length = len(watermark_bits)
        watermark_iterator = 0
        mask = np.zeros_like(image[:,:,0], dtype=np.uint8)

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                for k in range(image.shape[2]):
                    pixel = image[i, j, k]
                    watermark_bit = int(watermark_bits[watermark_iterator])
                    if (pixel & 0b00000001) != watermark_bit:
                        mask[i, j] = 255  # Blanc si le watermark est absent
                    watermark_iterator = (watermark_iterator + 1) % watermark_length
        self.new_image=Image.fromarray(mask)
        self.display_image(self.new_image, self.right_image_label)

    def display_image(self, image, label_widget):
        # Resize image to fit label
        image = image.resize((200, 200))
        photo = ImageTk.PhotoImage(image)
        label_widget.config(image=photo)
        label_widget.image = photo  # Keep a reference to prevent garbage collection
    

    def machine_learning(self):
        image=np.array(self.original_image)
        image = convert_to_ela_image(image, quality=90)
        # Extract texture features
        texture_features = extract_texture_features(image)
        # Extract color features (if added)
        color_features = extract_color_features(image)
        # Combine texture and color features
        combined_features = np.concatenate([texture_features, color_features])


        clf = load('clf.joblib')
        print(clf)
        print(type(clf))
        # Use the trained SVM classifier to predict the label of the image
        predicted_label = clf.predict([combined_features])
        if predicted_label:
            self.ML_result.config(text="Fausse Image")
        else:
            self.ML_result.config(text="Vrai Image")
            

if __name__ == "__main__":
    app = ImageProcessorApp()
    app.mainloop()
