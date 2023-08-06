from PIL import Image, ImageDraw
import pandas as pd
import os
import numpy as np

# Define the dimensions of the images
image_size = (384, 384)

# Define the number of images to generate for each set
n_images = {
    "train": 1000,
    "val": 200,
    "test": 200,
}

# Define the range of the number of circles to generate in each image
n_circles_range = (1, 10)

# Define the range of the radius of the circles
radius_range = (5, 10)

# Define the data directory
data_dir = "mock"

for set_name, n_set_images in n_images.items():
    # Create a directory for this set
    set_dir = os.path.join(data_dir, set_name)
    os.makedirs(set_dir, exist_ok=True)

    # Initialize a DataFrame to store the labels
    labels = pd.DataFrame(columns=["filename", "label"])

    # Generate the images
    for i in range(n_set_images):
        # Create a new image with a black background
        image = Image.new("RGB", image_size, "black")
        draw = ImageDraw.Draw(image)

        # Determine the number of circles to draw
        n_circles = np.random.randint(*n_circles_range)

        # Draw the circles
        for _ in range(n_circles):
            # Determine the center and radius of the circle
            center = np.random.uniform(
                radius_range[1], image_size[0] - radius_range[1], 2
            )
            radius = np.random.uniform(*radius_range)

            # Draw the circle
            bounding_box = [center - radius, center + radius]
            draw.ellipse(list(np.ravel(bounding_box)), "white")

        # Save the image
        filename = f"image{i + 1}.jpg"
        image_path = os.path.join(set_dir, filename)
        image.save(image_path)

        # Add the label to the DataFrame
        labels.loc[i] = [filename, n_circles]

    # Save the labels
    labels_path = os.path.join(set_dir, "annotations.txt")
    labels.to_csv(labels_path, index=False)
