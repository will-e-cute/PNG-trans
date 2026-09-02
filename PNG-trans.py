import sys
import json
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QGraphicsView, 
    QGraphicsScene, QGraphicsPixmapItem, QMenu, QToolBar, 
    QSlider, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame
)
from PySide6.QtCore import Qt, QPointF, QRectF, QSize
from PySide6.QtGui import QPixmap, QAction, QColor, QPainter

RECENT_FILES_FILE = "recent_files.json"

class ImageOverlay(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene())
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene().addItem(self.pixmap_item)

        # Performance optimizations
        self.setRenderHint(self.renderHints() | QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)

    def set_image(self, path):
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            self.pixmap_item.setPixmap(pixmap)
            self.setSceneRect(QRectF(0, 0, pixmap.width(), pixmap.height()))
            self.reset_zoom()

    def reset_zoom(self):
        self.resetTransform()
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

    def zoom_in(self):
        self.scale(1.1, 1.1)

    def zoom_out(self):
        self.scale(0.9, 0.9)

    def set_zoom_level(self, level):
        # Reset and then apply scale relative to fitInView if needed, 
        # but simpler to just scale from a baseline.
        # For a slider, we'll need a more controlled approach.
        pass

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()
        super().wheelEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transparent Viewer Pro")
        self.resize(900, 650)

        # Overlay Settings
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.5)

        # UI Components
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.viewer = ImageOverlay()
        self.layout.addWidget(self.viewer)

        # Controls Panel
        self.controls = QHBoxLayout()
        self.controls_widget = QWidget()
        self.controls_widget.setLayout(self.controls)
        self.controls_widget.setFixedHeight(50)
        self.layout.addWidget(self.controls_widget)

        # Alpha Slider
        self.controls.addWidget(QLabel("Window Alpha:"))
        self.win_alpha_slider = QSlider(Qt.Horizontal)
        self.win_alpha_slider.setRange(10, 100)
        self.win_alpha_slider.setValue(50)
        self.win_alpha_slider.setFixedWidth(150)
        self.win_alpha_slider.valueChanged.connect(self.update_window_opacity)
        self.controls.addWidget(self.win_alpha_slider)

        self.controls.addWidget(QLabel(" Image Alpha:"))
        self.img_alpha_slider = QSlider(Qt.Horizontal)
        self.img_alpha_slider.setRange(10, 100)
        self.img_alpha_slider.setValue(100)
        self.img_alpha_slider.setFixedWidth(150)
        self.img_alpha_slider.valueChanged.connect(self.update_image_opacity)
        self.controls.addWidget(self.img_alpha_slider)

        # Zoom Slider
        self.controls.addWidget(QLabel(" Zoom:"))
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(20, 500) # 0.2x to 5.0x
        self.zoom_slider.setValue(100)
        self.zoom_slider.setFixedWidth(150)
        self.zoom_slider.valueChanged.connect(self.update_zoom)
        self.controls.addWidget(self.zoom_slider)

        self.recent_files = self.load_recent_files()
        self.create_menus()

    def create_menus(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")

        open_action = QAction("&Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        close_action = QAction("&Close", self)
        close_action.triggered.connect(self.close_file)
        file_menu.addAction(close_action)

        self.recent_menu = QMenu("Recent Files", self)
        file_menu.addMenu(self.recent_menu)
        self.update_recent_menu()

        file_menu.addSeparator()
        quit_action = QAction("&Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

    def update_window_opacity(self, value):
        self.setWindowOpacity(value / 100.0)

    def update_image_opacity(self, value):
        self.viewer.pixmap_item.setOpacity(value / 100.0)

    def update_zoom(self, value):
        scale = value / 100.0
        # To make the slider consistent, we reset the transform and apply scale
        self.viewer.resetTransform()
        self.viewer.scale(scale, scale)
        # We still want to fit in view initially or keep centered
        self.viewer.centerOn(self.viewer.pixmap_item.sceneBoundingRect().center())

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp);;All files (*.*)"
        )
        if path:
            self.viewer.set_image(path)
            self.add_to_recent(path)
            self.update_recent_menu()

    def close_file(self):
        self.viewer.pixmap_item.setPixmap(QPixmap())

    def load_recent_files(self):
        if os.path.exists(RECENT_FILES_FILE):
            try:
                with open(RECENT_FILES_FILE, "r") as f:
                    return json.load(f)
            except:
                return []
        return []

    def add_to_recent(self, path):
        if path in self.recent_files:
            self.recent_files.remove(path)
        self.recent_files.insert(0, path)
        self.recent_files = self.recent_files[:10] # Keep last 10
        try:
            with open(RECENT_FILES_FILE, "w") as f:
                json.dump(self.recent_files, f)
        except Exception as e:
            print(f"Error saving recent files: {e}")

    def update_recent_menu(self):
        self.recent_menu.clear()
        for path in self.recent_files:
            action = QAction(os.path.basename(path), self)
            action.triggered.connect(lambda checked, p=path: self.open_recent(p))
            self.recent_menu.addAction(action)

    def open_recent(self, path):
        if os.path.exists(path):
            self.viewer.set_image(path)
        else:
            print(f"File no longer exists: {path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
