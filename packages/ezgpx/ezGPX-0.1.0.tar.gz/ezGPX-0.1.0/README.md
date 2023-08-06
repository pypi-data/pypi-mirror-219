# 🗺️ ezGPX

## 🔎 Description
Easy to use Python GPX library.

## 🛠️ Installation

```bash
pip install ezgpx
```

## 🏁 Get started

```python
import ezgpx

# Parse GPX file
gpx = ezgpx.GPX("file.gpx")

# Simplify (using Ramer-Dougle-Peucker algorithm)
gpx.simplify()

# Plot with Matplotlib
gpx.matplotlib_plot(title="Track", base_color="#FF0000",
                    start_stop=True, way_points=False, file_path="img_1")

# Plot with Matplotlib Basemap Toolkit
gpx.matplotlib_basemap_plot(title="Track", base_color="#00FF00",
                            start_stop=False, way_points=False, file_path="img_2")

# Plot with gmap (Google Maps)
gpx.gmap_plot(title="Track", base_color="#0000FF", start_stop=True,
              way_points=True, file_path="map_1.html", open=True)

# Plot with Folium
gpx.folium_plot(title="Track", tiles="OpenStreetMap", base_color="#000000", start_stop=True,
                way_points=True, minimap=True, coord_popup=True, file_path="map_2.html", open=True)

# Remove metadata
gpx.remove_metadata()

# Write new simplified GPX file
gpx.to_gpx("new_file.gpx")
```

## 📚 References:

### 🧭 Other Python GPX Library
- [gpxpy](https://github.com/tkrajina/gpxpy)

## 👤 Author
- Fabien ALLEMAND