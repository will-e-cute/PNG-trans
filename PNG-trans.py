import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk


class ZoomableImageViewer:
    def __init__(self, master):
        self.master = master
        master.title("Image Viewer Pro")
        master.geometry("900x650")
        master.attributes("-alpha", 0.95)

        self.image = None
        self.tk_image = None

        self.zoom = 1.0
        self.img_alpha = 1.0

        self.offset_x = 0
        self.offset_y = 0

        self.drag_start_x = 0
        self.drag_start_y = 0

        # --- Layout ---
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        # Canvas (IMPORTANT pour pan)
        self.canvas = tk.Canvas(master, bg="black", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # --- Controls ---
        control = tk.Frame(master)
        control.grid(row=1, column=0, sticky="ew")

        ttk.Button(control, text="Open", command=self.open_image).pack(side=tk.LEFT, padx=5)

        ttk.Label(control, text="Zoom").pack(side=tk.LEFT)
        self.zoom_var = tk.DoubleVar(value=1.0)
        ttk.Scale(control, from_=0.2, to=5.0, variable=self.zoom_var,
                  command=self.on_zoom_slider).pack(side=tk.LEFT, fill="x", expand=True)

        ttk.Label(control, text="Alpha").pack(side=tk.LEFT)
        self.alpha_var = tk.DoubleVar(value=1.0)
        ttk.Scale(control, from_=0.1, to=1.0, variable=self.alpha_var,
                  command=self.on_alpha_slider).pack(side=tk.LEFT, fill="x", expand=True)

        # --- Events ---
        self.canvas.bind("<MouseWheel>", self.zoom_mouse)     # Windows
        self.canvas.bind("<Button-4>", self.zoom_in)          # Linux
        self.canvas.bind("<Button-5>", self.zoom_out)

        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)

    # ---------- IMAGE ----------
    def open_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            self.image = Image.open(path).convert("RGBA")
            self.zoom = 1.0
            self.offset_x = 0
            self.offset_y = 0
            self.update_image()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------- UPDATE ----------
    def update_image(self):
        if self.image is None:
            return

        img = self.image.copy()

        # appliquer alpha image
        if self.img_alpha < 1.0:
            alpha = img.split()[3]
            alpha = alpha.point(lambda p: int(p * self.img_alpha))
            img.putalpha(alpha)

        # resize
        w, h = img.size
        new_size = (int(w * self.zoom), int(h * self.zoom))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

        self.tk_image = ImageTk.PhotoImage(img)

        self.canvas.delete("all")

        # centre + offset
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()

        x = canvas_w // 2 + self.offset_x
        y = canvas_h // 2 + self.offset_y

        self.canvas.create_image(x, y, image=self.tk_image)

    # ---------- ZOOM ----------
    def zoom_mouse(self, event):
        scale = 1.1 if event.delta > 0 else 0.9
        self.apply_zoom(scale, event.x, event.y)

    def zoom_in(self, event):
        self.apply_zoom(1.1, event.x, event.y)

    def zoom_out(self, event):
        self.apply_zoom(0.9, event.x, event.y)

    def apply_zoom(self, scale, cx, cy):
        old_zoom = self.zoom
        self.zoom *= scale
        self.zoom = max(0.2, min(self.zoom, 5))

        # zoom centré sur la souris
        self.offset_x = (self.offset_x - cx) * (self.zoom / old_zoom) + cx
        self.offset_y = (self.offset_y - cy) * (self.zoom / old_zoom) + cy

        self.zoom_var.set(self.zoom)
        self.update_image()

    def on_zoom_slider(self, _):
        self.zoom = self.zoom_var.get()
        self.update_image()

    # ---------- ALPHA ----------
    def on_alpha_slider(self, _):
        self.img_alpha = self.alpha_var.get()
        self.update_image()

    # ---------- DRAG ----------
    def start_drag(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def drag(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y

        self.offset_x += dx
        self.offset_y += dy

        self.drag_start_x = event.x
        self.drag_start_y = event.y

        self.update_image()


# ---------- RUN ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = ZoomableImageViewer(root)
    root.mainloop()