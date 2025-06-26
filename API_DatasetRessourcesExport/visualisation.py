import os

export_folder = 'export'
kml_files = []

# Walk through export folder and collect all .kml files
for filename in os.listdir(export_folder):
    if filename.lower().endswith('.kml'):
        filepath = os.path.join(export_folder, filename)
        kml_files.append(filepath)

# Print results
if kml_files:
    print(f"\nFound {len(kml_files)} KML file(s):\n")
    for f in kml_files:
        print(f"- {f}")
else:
    print("No KML files found in the export folder.")