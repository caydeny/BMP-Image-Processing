import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from bmp_file import BMPFile
from image_processing import bgr_to_rgb, adjust_brightness, adjust_scale, apply_toggle_colour

class GUI:
    def __init__(self, root):
        self.root = root
        self.colour_channels = {"red": True, "green": True, "blue": True}
        self.bmp_file = None
        self._setup_ui()
    
    def _setup_ui(self):
        # File Frame
        file_frame = tk.LabelFrame(self.root, text="File Path")
        file_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        self.file_path_entry = tk.Entry(file_frame, width=50)
        self.file_path_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(file_frame, text="Browse", command=self._browse_file).grid(row=0, column=2, padx=5, pady=5)

        # Image Frame
        image_frame = tk.LabelFrame(self.root, text="Image")
        image_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")
        
        self.image_label = tk.Label(image_frame)
        self.image_label.grid(row=0, column=0, padx=5, pady=5)

        # Metadata Frame
        metadata_frame = tk.LabelFrame(self.root, text="Metadata")
        metadata_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        
        self.file_size_label = tk.Label(metadata_frame, text="File Size:")
        self.file_size_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")

        self.image_width_label = tk.Label(metadata_frame, text="Image Width:")
        self.image_width_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")

        self.image_height_label = tk.Label(metadata_frame, text="Image Height:")
        self.image_height_label.grid(row=2, column=0, padx=5, pady=2, sticky="w")

        self.bits_per_pixel_label = tk.Label(metadata_frame, text="Bits Per Pixel:")
        self.bits_per_pixel_label.grid(row=3, column=0, padx=5, pady=2, sticky="w")

        # Adjustments Frame
        adjustments_frame = tk.LabelFrame(self.root, text="Adjustments")
        adjustments_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        
        # Brightness Scale
        tk.Label(adjustments_frame, text="Brightness").grid(row=0, column=0, padx=5, pady=2)
        self.brightness_scale = tk.Scale(adjustments_frame, orient="horizontal", from_=0, to=100)
        self.brightness_scale.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        self.brightness_scale.set(100)
        self.brightness_scale.bind("<ButtonRelease-1>", self._update_image)

        # Scale Scale
        tk.Label(adjustments_frame, text="Scale").grid(row=1, column=0, padx=5, pady=2)
        self.scale_scale = tk.Scale(adjustments_frame, orient="horizontal", from_=0, to=100)
        self.scale_scale.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        self.scale_scale.set(100)
        self.scale_scale.bind("<ButtonRelease-1>", self._update_image)

        # Colour Channels Frame
        colour_frame = tk.LabelFrame(self.root, text="Colour Channels")
        colour_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        
        R_button = tk.Button(colour_frame, text="R", width=8, relief=tk.RAISED, command=lambda: self._toggle_colour("red"))
        R_button.grid(row=0, column=0, padx=5, pady=5)
        self.R_button = R_button

        G_button = tk.Button(colour_frame, text="G", width=8, relief=tk.RAISED, command=lambda: self._toggle_colour("green"))
        G_button.grid(row=0, column=1, padx=5, pady=5)
        self.G_button = G_button

        B_button = tk.Button(colour_frame, text="B", width=8, relief=tk.RAISED, command=lambda: self._toggle_colour("blue"))
        B_button.grid(row=0, column=2, padx=5, pady=5)
        self.B_button = B_button

    def _update_metadata(self):
        self.file_size_label.config(text=f"File Size: {self.bmp_file.file_size} bytes")
        self.image_width_label.config(text=f"Image Width: {self.bmp_file.image_width} pixels")
        self.image_height_label.config(text=f"Image Height: {self.bmp_file.image_height} pixels")
        self.bits_per_pixel_label.config(text=f"Bits Per Pixel: {self.bmp_file.bits_per_pixel}")

    def _toggle_colour(self, channel):
        # Handle red channel toggle
        if channel == "red":
            # Toggle red channel state
            self.colour_channels["red"] = not self.colour_channels["red"]
            self.R_button.config(relief=tk.SUNKEN if not self.colour_channels["red"] else tk.RAISED)
        
        # Handle green channel toggle  
        elif channel == "green":
            # Toggle green channel state
            self.colour_channels["green"] = not self.colour_channels["green"]
            self.G_button.config(relief=tk.SUNKEN if not self.colour_channels["green"] else tk.RAISED)
        
        # Handle blue channel toggle
        elif channel == "blue":
            # Toggle blue channel state
            self.colour_channels["blue"] = not self.colour_channels["blue"]
            self.B_button.config(relief=tk.SUNKEN if not self.colour_channels["blue"] else tk.RAISED)
        
        # Update the image display with new channel states
        self._update_image()
    
    def _update_image(self, event=None):
        # No BMP file is loaded
        if not self.bmp_file:
            return
                
        # Get current values from adjustment sliders
        brightness_value = self.brightness_scale.get()
        scale_value = self.scale_scale.get()

        # Apply sequence of image processing operations
        data = self.bmp_file.pixel_data # Get original pixel data
        data = adjust_brightness(data, brightness_value) # Adjust brightness
        data = adjust_scale(data, self.bmp_file.image_width, self.bmp_file.image_height, scale_value) # Scale image
        data = apply_toggle_colour(data, self.colour_channels) # Apply color channel toggles
        data = bgr_to_rgb(data) # Convert from BGR to RGB format

        # Convert 2D array of rows into a flat 1D array
        flat_array = bytearray() # frombytes() expects 1D array of bytes
        for row in data:
            flat_array.extend(row)
            
        # Calculate dimensions and create pillow image
        width = len(data[0]) // 3 # Divide by 3 because each pixel has RGB values
        height = len(data)
        image = Image.frombytes("RGB", (width, height), bytes(flat_array))
        photo_image = ImageTk.PhotoImage(image) # Convert to PhotoImage for tkinter
        
        # Update the image display label
        self.image_label.config(image=photo_image)
        self.image_label.image = photo_image # Keep reference to prevent garbage collection
            
    def _browse_file(self):
        # Open file selection dialog
        file_path = tk.filedialog.askopenfilename() 

        # User cancels file selection dialog
        if not file_path:
            return
            
        try:
            # Reset scales
            self.brightness_scale.set(100)
            self.scale_scale.set(100)
            
            # Reset colour channel toggles
            self.colour_channels = {"red": True, "green": True, "blue": True}
            self.R_button.config(relief=tk.RAISED)
            self.G_button.config(relief=tk.RAISED)
            self.B_button.config(relief=tk.RAISED)

            self.bmp_file = BMPFile(file_path) # Load selected bmp file
            
            self.file_path_entry.delete(0, tk.END) # Clear file path before filling
            self.file_path_entry.insert(0, file_path) # Update entry with file path

            # Update image and metadata display
            self._update_image()
            self._update_metadata()

        except (ValueError, Exception) as e:
            return