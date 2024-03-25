import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
def detection_contours(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detection
    edged = cv2.Canny(blurred, 30, 150)
#edges = cv2.Canny(gray, 100, 200)
    # Find contours
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours

if __name__ == "__main__":
    # Charger l'image
    path = "/home/aissa/Desktop/PROJECT COMP/projet-image/Code/sigma.png" 

    image = cv2.imread(path)

    contours=detection_contours(image)

    height, width = image.shape[:2]
    canvas = np.zeros((height, width, 3), dtype=np.uint8)

    for contour in contours:
        if cv2.contourArea(contour) > 0.5:
            cv2.drawContours(canvas, [contour], -1, (0, 255, 0), 2)

    image_height, image_width = image.shape[:2]

    for i, contour in enumerate(contours):
        mask = np.zeros((image_height, image_width), dtype=np.uint8)
        
        cv2.drawContours(mask, [contour], -1, (255), thickness=cv2.FILLED)
        
        segment = cv2.bitwise_and(image, image, mask=mask)
        
"""         # Afficher ou sauvegarder le segment pour une analyse ultérieure
        plt.figure(figsize=(8, 8))  # You can adjust the figure size as needed
        plt.imshow(cv2.cvtColor(segment, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for correct coloring
        plt.title(f'Segment {i}')  # Display the segment number as the title
        plt.axis('off')  # Hide the axis to focus on the image content
        plt.show()
    cv2.destroyAllWindows() """

