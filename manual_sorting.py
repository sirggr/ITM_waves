import cv2
import numpy as np

def manual_sort(source: str):
    # Load the image
    image = cv2.imread(source)

    # Display the image
    cv2.imshow('image', image)
    cv2.waitKey(0)

    # Get the label from the user
    label = input('Enter the label (1 or 0): ')

    # Save the image and label to a file
    np.save('image.npy', image)
    np.save('label.npy', label)
