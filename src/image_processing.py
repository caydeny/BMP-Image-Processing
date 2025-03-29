def bgr_to_rgb(pixel_data):
    # Create an empty list to store converted RGB rows
    rgb_rows = []
    
    # Loop through each row in the pixel data
    for row in pixel_data:
        # Initialize an empty bytearray for the current RGB row
        rgb_row = bytearray(len(row)) # Same length as input row
        
        # Map BGR to RGB
        rgb_row[::3] = row[2::3]  # R = B
        rgb_row[1::3] = row[1::3]  # G = G
        rgb_row[2::3] = row[::3]  # B = R
        
        # Append the RGB row list of RGB rows
        rgb_rows.append(rgb_row)
    
    # Return the list of RGB rows
    return rgb_rows

def adjust_brightness(pixel_data, brightness_value):
    # Convert brightness percentage to a decimal factor
    brightness_factor = brightness_value / 100.0
    adjusted_rows = [] # List to store rows of adjusted pixel data
    
    for row in pixel_data:
        # Initialize a bytearray to store adjusted pixel values
        adjusted_row = bytearray(len(row))
        # Calculate the number of pixels in the row
        width = len(row) // 3
        
        # Loop through each pixel in the row
        for pixel in range(width):
            i = pixel * 3 # Starting index for current pixel

            # Extract original BRG colour values
            b, g, r = int(row[i]), int(row[i + 1]), int(row[i + 2])
            
            # Calculate YUV components
            y = (0.299 * r + 0.587 * g + 0.114 * b) * brightness_factor
            u = (-0.147 * r - 0.289 * g + 0.436 * b)
            v = (0.615 * r - 0.515 * g - 0.100 * b)
            
            # Convert back to RGB
            r = y + 1.140 * v
            g = y - 0.395 * u - 0.581 * v
            b = y + 2.032 * u
            
            # Store adjusted values in BGR order
            adjusted_row[i] = max(0, min(255, int(round(b))))
            adjusted_row[i+1] = max(0, min(255, int(round(g))))
            adjusted_row[i+2] = max(0, min(255, int(round(r))))
                    
        # Append the adjusted row to the adjusted_rows list
        adjusted_rows.append(adjusted_row)
    
    # Return the list of adjusted rows
    return adjusted_rows

def adjust_scale(pixel_data, original_width, original_height, scale_value):
    # Calculate the scale factor based on the scale value
    if scale_value > 0:
        scale_factor = scale_value / 100.0
    else:
        scale_factor = 0.01 # Prevent division by 0

    # Calculate the new dimensions of the image
    new_width = max(1, int(original_width * scale_factor)) # Use max to ensure > 0 pixels
    new_height = max(1, int(original_height * scale_factor))
    
    # Calculate the ratio of the original dimensions to the new dimensions
    x_ratio = original_width / new_width
    y_ratio = original_height / new_height
    
    # Store final scaled image data by rows
    scaled_rows = []
    
    # Loop through each row in the new image
    for new_y in range(new_height):
        # Initialize an empty bytearray for the current scaled row
        scaled_row = bytearray(new_width * 3)

        # Map current scaled row position back to original image
        original_y = min(int(new_y * y_ratio), original_height - 1)
        
        # Ensure the source row is within bounds of original pixel data
        if original_y < len(pixel_data): 
            # Loop through each pixel in the new row
            for new_x in range(new_width):
                # Map current scaled pixel position back to original image
                original_x = min(int(new_x * x_ratio), original_width - 1)

                # Calculate byte positions in the row data
                new_position = new_x * 3 # 3 bytes (BGR)
                original_position = original_x * 3

                # Copy BGR values from original image to scaled image
                scaled_row[new_position:new_position+3] = pixel_data[original_y][original_position:original_position+3]
        
        # Add completed row to scaled image
        scaled_rows.append(scaled_row)

    return scaled_rows

def apply_toggle_colour(pixel_data, channels):
    toggled_rows = [] # Store processed rows

    for row in pixel_data:
        # Create a new bytearray for the current row
        toggled_row = bytearray(len(row))
        # Calculate the number of pixels in the row
        width = len(row) // 3
        
        for pixel in range(width):
            i = pixel * 3 # Starting index for current pixel

            if channels["blue"]:
                toggled_row[i] = row[i] # Keep the blue value
            else:
                toggled_row[i] = 0 # Set blue to 0

            if channels["green"]:
                toggled_row[i + 1] = row[i + 1] # Keep the green value
            else:
                toggled_row[i + 1] = 0 # Set green to 0

            if channels["red"]:
                toggled_row[i + 2] = row[i + 2] # Keep the red value
            else:
                toggled_row[i + 2] = 0 # Set red to 0
        
        toggled_rows.append(toggled_row)
    
    return toggled_rows