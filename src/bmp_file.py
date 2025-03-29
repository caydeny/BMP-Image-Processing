from tkinter import messagebox

class BMPFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.bmp_bytes = self._read_file()
        self._parse_header()
        self.pixel_data = self._extract_pixel_data()
    
    # Read file into byte array
    def _read_file(self):
        with open(self.file_path, "rb") as f:
            bmp_bytes = f.read()
            
        # Validate bmp signature
        if bmp_bytes[0:2] != b"BM":
            messagebox.showerror("Error", "Invalid file signature. Please enter a file with a bmp signature.")
            raise ValueError("Invalid BMP signature")
        
        return bmp_bytes

    # Parse bmp header for required metadata
    def _parse_header(self):
        self.image_width = int.from_bytes(self.bmp_bytes[18:22], "little")
        self.image_height = int.from_bytes(self.bmp_bytes[22:26], "little")
        self.bits_per_pixel = int.from_bytes(self.bmp_bytes[28:30], "little")
        self.file_size = str(int.from_bytes(self.bmp_bytes[2:6], "little"))
        self.pixel_array_offset = int.from_bytes(self.bmp_bytes[10:14], "little")

        # Validate bits per pixel
        if self.bits_per_pixel not in [1, 4, 8, 24]:
            messagebox.showerror("Error", "Unsupported bits per pixel. Please enter a bmp file with 1, 4, 8, or 24 bits per pixel.")
            raise ValueError("Unsupported bits per pixel")

    # Determine bits per pixel for bmp file
    def _extract_pixel_data(self):
        if self.bits_per_pixel == 24:
            return self._extract_24bit()
        # Else 1, 4, 8 bits per pixel
        return self._extract_indexed()

    def _extract_24bit(self):
        # Extract pixel data starting from the pixel array offset
        pixel_data = self.bmp_bytes[self.pixel_array_offset:]
        
        # Calculate the row padding 
        row_padding = (4 - (self.image_width * 3) % 4) % 4 # Each row is padded to a multiple of 4 bytes
        
        # Initialize empty list to store each row of pixel data
        rows = []
        
        # Process each row of image
        for row_index in range(self.image_height):
            # Calculate the starting byte position for this row
            row_start = row_index * (self.image_width * 3 + row_padding)
            # Calculate the ending byte position for this row
            row_end = row_start + (self.image_width * 3)
            
            # Extract the row data and append it to the rows list
            row = bytearray(pixel_data[row_start:row_end])
            rows.append(row)
        
        # Reverse rows to account for the BMP format storing rows bottom-to-top
        rows.reverse()
        
        return rows

    def _extract_indexed(self):
        # Calculate the number of colours in the palette based on bits per pixel
        palette_size = 2 ** self.bits_per_pixel
        # Extract the colour palette data starting at byte 54
        palette = self.bmp_bytes[54:54 + palette_size * 4]
        
        # Initialize list to store BGR colour values from palette
        palette_bgr = []

        # Process each palette entry (4 bytes)
        for index in range(0, len(palette), 4): # Format is Blue Green Red Reserved
            # Extract just the BGR values
            bgr = palette[index:index+3]
            palette_bgr.append(bgr)

        # Calculate how many pixels can be stored in one byte
        pixels_per_byte = 8 // self.bits_per_pixel
        # Calculate how many bytes are needed to store one row of pixels
        bytes_per_row = (self.image_width + pixels_per_byte - 1) // pixels_per_byte
        # Calculate padding bytes needed
        row_padding = (4 - (bytes_per_row % 4)) % 4
        # Total bytes per row including padding
        stride = bytes_per_row + row_padding

        # Create a bit mask for extracting pixel indices
        mask = (1 << self.bits_per_pixel) - 1
        
        # Initialize an empty list to store rows of pixel data
        rows = []
        # Extract pixel data starting from the pixel array offset
        pixel_data = self.bmp_bytes[self.pixel_array_offset:]
        
        # Process each row of the image from bottom-to-top
        for row_index in range(self.image_height): 
            # Initialize an empty bytearray for the current row
            row = bytearray(self.image_width * 3)
            # Calculate the offset for the current row
            row_offset = row_index * stride
            
            # Initialize the current pixel position
            pixel_position = 0
        
            # Process each byte in the current row
            for byte_offset in range(bytes_per_row):
                # Break if the row offset exceeds the pixel data length
                if row_offset + byte_offset >= len(pixel_data):
                    break
                    
                # Get the current byte
                byte = pixel_data[row_offset + byte_offset]
                
                # Extract each pixel from the current byte
                for bit_pos in range(8 // self.bits_per_pixel):
                    # Break if the pixel position exceeds the image width
                    if pixel_position >= self.image_width:
                        break
                        
                    # Calculate bit shift needed to extract current pixel
                    shift = 8 - (bit_pos + 1) * self.bits_per_pixel

                    # Extract colour index for current pixel using mask
                    index = (byte >> shift) & mask
                    
                    # Look up the BGR colour values in palette and set pixel colour
                    if index < len(palette_bgr):
                        row[pixel_position * 3:pixel_position * 3 + 3] = palette_bgr[index] # Convert to 24 bits per pixel
                    
                    # Increment the pixel position
                    pixel_position += 1
            
            # Append the row to the rows list
            rows.append(row)
            
        # Reverse the rows to account for the BMP format storing rows bottom-to-top
        rows.reverse()
        return rows