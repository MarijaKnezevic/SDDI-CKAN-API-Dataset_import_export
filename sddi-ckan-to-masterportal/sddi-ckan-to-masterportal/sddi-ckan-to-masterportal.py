import os
import requests
import json
import re
import sys
from datetime import datetime
import subprocess

# === Utility Functions ===

def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', '_', name)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def append_if_not_exists(entry, target_list, key='id'):
    if entry.get(key) not in [e.get(key) for e in target_list]:
        target_list.append(entry)
        return True
    return False

def select_datasets(datasets):
    print("\n📚 Available datasets:")
    for i, ds in enumerate(datasets, 1):
        print(f"{i}. {ds.get('title', 'unknown_title')}")

    input_str = input("\nEnter indices to export (comma-separated) or 'all': ").strip().lower()
    if input_str == 'all':
        return datasets
    try:
        selected_indices = [int(i.strip()) - 1 for i in input_str.split(',')]
        return [datasets[i] for i in selected_indices if 0 <= i < len(datasets)]
    except Exception as e:
        print(f"❌ Invalid selection: {e}")
        sys.exit()

def main():
    # === Input ===
    catalog_url = input("Enter the CKAN catalog URL to export from: ").strip()
    catalog_name = catalog_url.split('//')[1].split('/')[0].replace('.', '_')
    api_url = f"{catalog_url}/api/3/action/package_search"
    params = {'q': '*:*', 'start': 0, 'rows': 1000}

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_folder = 'export'
    os.makedirs(export_folder, exist_ok=True)

    # === Fetch Datasets ===
    print("🔄 Fetching dataset list...")
    response = requests.get(api_url, params=params)
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return

    datasets = response.json().get('result', {}).get('results', [])
    if not datasets:
        print("⚠️ No datasets found.")
        return

    selected_datasets = select_datasets(datasets)

    print(f"\n📦 Exporting {len(selected_datasets)} dataset(s)...")
    datasets_exported = 0

    for ds in selected_datasets:
        title = ds.get('title', 'unknown_title')
        base_name = clean_filename(title)
        dataset_filename = f"{base_name}_{timestamp}.json"
        dataset_path = os.path.join(export_folder, dataset_filename)
        save_json(dataset_path, ds)
        print(f"✅ Exported dataset: {dataset_filename}")

        # === Extract WMS info ===
        try:
            resource = ds['resources'][0]
        except (KeyError, IndexError):
            print(f"⚠️ Skipped '{title}' — no valid resources.")
            continue

        description_lines = resource.get('description', '').splitlines()
        layers = []
        version = "1.3.0"
        for line in description_lines:
            if line.lower().startswith("layers"):
                layers = [l.strip() for l in line.split('=')[1].split(',')]
            elif line.lower().startswith("version"):
                version = line.split('=')[1].strip()

        layer_id = base_name
        layer_name = resource.get("name", title)
        url_val = resource.get("url", "")
        format_type = "image/png"

        service_entry = {
            "id": layer_id,
            "name": layer_name,
            "url": url_val,
            "typ": "WMS",
            "layers": layers,
            "version": version,
            "gfiAttributes": "showAll",
            "gfiTheme": "default",
            "layerAttribution": "© Bayerische Vermessungsverwaltung",
            "legendURL": "",
            "transparent": True,
            "format": format_type,
            "urlIsVisible": True
        }

        config_entry = {
            "id": layer_id,
            "name": layer_name,
            "typ": "WMS",
            "url": url_val,
            "layers": layers,
            "format": format_type,
            "styles": [""],
            "transparent": False,
            "opacity": 1.0,
            "visible": True,
            "showInLayerTree": True
        }

        # === Save config/service files ===
        config_file = os.path.join(export_folder, f"{base_name}-config.json")
        service_file = os.path.join(export_folder, f"{base_name}-service.json")
        save_json(config_file, config_entry)
        save_json(service_file, service_entry)

        print(f"✅ Created: {os.path.basename(config_file)}")
        print(f"✅ Created: {os.path.basename(service_file)}")
        datasets_exported += 1

    print(f"\n🎉 Done! Exported {datasets_exported} dataset(s) to folder: {export_folder}/")

    # === Select files to import ===
    print("\n📥 Select files to import into Masterportal:")
    config_files = [f for f in os.listdir(export_folder) if f.endswith("-config.json")]
    if not config_files:
        print("❌ No '*-config.json' files found in the export folder.")
        return

    for i, fname in enumerate(config_files, 1):
        print(f"{i}. {fname}")

    try:
        indices = input("\nEnter the numbers of config files to import (comma-separated): ")
        selected_indices = [int(i.strip()) - 1 for i in indices.split(',')]
        selected_files = [config_files[i] for i in selected_indices if 0 <= i < len(config_files)]
    except Exception as e:
        print(f"❌ Invalid selection: {e}")
        return

    # === Load Masterportal config/service files ===
    mp_config_path = os.path.join("..", "examples", "Basic", "config.json")
    mp_services_path = os.path.join("..", "examples", "Basic", "resources", "services.json")

    try:
        mp_config = load_json(mp_config_path)
        mp_layers = mp_config["layerConfig"]["subjectlayer"]["elements"]
    except Exception as e:
        print(f"\n❌ Error reading Masterportal config.json: {e}")
        return

    try:
        mp_services = load_json(mp_services_path)
        if not isinstance(mp_services, list):
            raise ValueError("services.json must contain a list.")
    except Exception as e:
        print(f"\n❌ Error reading Masterportal services.json: {e}")
        return

    # === Import selected files ===
    print("\n🛠️ Importing into Masterportal...")

    for config_fname in selected_files:
        base_name = config_fname.replace("-config.json", "")
        service_fname = f"{base_name}-service.json"

        config_path = os.path.join(export_folder, config_fname)
        service_path = os.path.join(export_folder, service_fname)

        if not os.path.exists(service_path):
            print(f"⚠️ Skipped '{base_name}': service file missing")
            continue

        try:
            config_entry = load_json(config_path)
            service_entry = load_json(service_path)
        except Exception as e:
            print(f"❌ Failed to load JSON for {base_name}: {e}")
            continue

        if append_if_not_exists(config_entry, mp_layers):
            print(f"✅ Added '{config_entry['id']}' to config.json")
        else:
            print(f"⚠️ Skipped '{config_entry['id']}' (already in config.json)")

        if append_if_not_exists(service_entry, mp_services):
            print(f"✅ Added '{service_entry['id']}' to services.json")
        else:
            print(f"⚠️ Skipped '{service_entry['id']}' (already in services.json)")

    # === Save updated Masterportal files ===
    try:
        save_json(mp_config_path, mp_config)
        save_json(mp_services_path, mp_services)
        print("\n✅ Masterportal files updated successfully.")
    except Exception as e:
        print(f"\n❌ Failed to save updated files: {e}")

    launch_preview = input("\n🌐 Launch local Masterportal preview? (yes/no): ").strip().lower()
    if launch_preview == "yes":
        os.chdir(os.path.join("..", "examples", "Basic"))
        print("🚀 Starting local HTTP server at http://localhost:8000")
        try:
            subprocess.run(["python", "-m", "http.server", "8000"])
        except Exception as e:
            print(f"❌ Failed to start server: {e}")

if __name__ == "__main__":
    main()