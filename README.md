# 📷 Image Viewer Pro

Un visualiseur d’images en Python avec :

* 🔍 Zoom fluide (molette + slider)
* 🎯 Zoom centré sur la souris
* ✋ Drag & Pan (déplacement à la souris)
* 🪟 Transparence de la fenêtre
* 🌫 Transparence dynamique de l'image
* 🖼 Support PNG / JPG / BMP

***

## 🚀 Aperçu des fonctionnalités

### 🔍 Zoom avancé

* Molette souris (zoom in/out)
* Zoom centré sur le curseur (type Photoshop)
* Slider de contrôle précis

### ✋ Navigation (Pan)

* Clic gauche + drag pour déplacer l’image
* Fluide et sans repositionnement brutal

### 🌫 Transparence

* Transparence globale de la fenêtre
* Transparence de l’image réglable en temps réel

***

## 📦 Prérequis

* Python **3.10+** (testé avec 3.12)
* Bibliothèques :

```bash
pip install pillow
pip instal pyside6
```

***

## ▶️ Lancement

```bash
python image_viewer.py
```

***

## 🎮 Utilisation

| Action                | Description             |
| --------------------- | ----------------------- |
| 🖱 Molette            | Zoom avant / arrière    |
| 🖱 Clic gauche + drag | Déplacer l'image        |
| 🎚 Slider Zoom        | Ajuster le zoom         |
| 🎚 Slider Alpha       | Ajuster la transparence |
| 📂 Open               | Charger une image       |

***

## 🧠 Architecture

Le projet repose sur :

* **Tkinter** → interface graphique
* **Canvas** → rendu et manipulation de l’image (obligatoire pour pan/zoom fluide)
* **Pillow (PIL)** → traitement image (resize, alpha)

***

## ⚙️ Fonctionnement du zoom

Le zoom est :

* basé sur un facteur multiplicatif (`scale`)
* recalculé autour du curseur
* appliqué avec compensation des offsets

```python
self.offset_x = (self.offset_x - cx) * (new_zoom / old_zoom) + cx
```

👉 permet un effet **zoom naturel centré souris**

***

## 📂 Formats supportés

* ✅ PNG (avec transparence)
* ✅ JPG / JPEG
* ✅ BMP

***

## ⚠️ Limitations

* Images très grandes → peut ralentir (resize CPU)
* Pas de cache niveau zoom (optimisation possible)
* Pas encore de multi-images ou onglets

***

## 🔧 Améliorations possibles

* 🧊 Fond damier (transparence type Photoshop)
* ⚡ Optimisation des performances (tiling / cache)
* 🧭 Reset vue (double clic)
* 🧮 Affichage coordonnées / pixels
* 📁 Drag & drop fichier
* 🖥 Mode plein écran
* 🔄 Rotation image

***

## 👨‍💻 Auteur

Wilfried GOUBOT  
Integrator Performance Technician

***

## 📜 Licence

Usage libre pour projet personnel ou interne.
