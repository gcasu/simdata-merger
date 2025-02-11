import json
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from jsonschema import validate, ValidationError

# Define file paths
SIMDATA_FILE = "simdata.json"
SIMMODS_FILE = "simmods.json"
OUTPUT_FILE = "simdata.simjson"

# Define JSON Schema
SIMDATA_SCHEMA = {
    "type": "object",
    "properties": {
        "visuals": {"type": "array"},
        "animdata": {"type": "array"}
    },
    "required": ["visuals", "animdata"],
    "additionalProperties": False
}

# Track last modified timestamp to prevent duplicate triggers
last_modified_time = 0

class JsonFileHandler(FileSystemEventHandler):
    """Handler that reacts to changes in simmods.json."""
    
    def on_modified(self, event):
        global last_modified_time

        if event.src_path.endswith(SIMMODS_FILE):
            # Get current modification time
            current_modified_time = os.path.getmtime(SIMMODS_FILE)

            # Avoid duplicate events
            if current_modified_time == last_modified_time:
                return  # Skip redundant calls
            last_modified_time = current_modified_time

            print(f"[INFO] Detected change in {SIMMODS_FILE}")
            self.process_file()

    def process_file(self):
        """Validate simmods.json against schema and merge it with simdata.json correctly."""
        try:
            with open(SIMMODS_FILE, "r", encoding="utf-8") as f:
                simmods_data = json.load(f)
            print("[INFO] simmods.json is a valid JSON.")

            # Validate against schema
            try:
                validate(instance=simmods_data, schema=SIMDATA_SCHEMA)
                print("[INFO] simmods.json matches the required schema.")
            except ValidationError as e:
                print(f"[ERROR] simmods.json does not match schema: {e.message}")
                return

            # Check if simdata.json exists
            if not os.path.exists(SIMDATA_FILE):
                print(f"[WARNING] {SIMDATA_FILE} not found. Skipping merge and waiting for next modification.")
                return

            # Load simdata.json
            with open(SIMDATA_FILE, "r", encoding="utf-8") as f:
                simdata = json.load(f)

            # Ensure simdata.json has expected structure
            simdata.setdefault("visuals", [])
            simdata.setdefault("animdata", [])

            # Merge arrays (combine unique values)
            merged_visuals = list({json.dumps(v) for v in simdata["visuals"] + simmods_data["visuals"]})  # Unique merge
            merged_animdata = list({json.dumps(a) for a in simdata["animdata"] + simmods_data["animdata"]})

            # Convert back from JSON strings to objects
            merged_visuals = [json.loads(v) for v in merged_visuals]
            merged_animdata = [json.loads(a) for a in merged_animdata]

            # Construct merged JSON
            merged_data = {
                "visuals": merged_visuals,
                "animdata": merged_animdata
            }

            # Write merged data to a new JSON file
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(merged_data, f, separators=(',', ':'))
            print(f"[SUCCESS] Merged JSON written to {OUTPUT_FILE}")

        except json.JSONDecodeError:
            print("[ERROR] Invalid JSON detected in simmods.json. Waiting for next modification.")

def main():
    path = os.getcwd()  # Watch the current directory
    event_handler = JsonFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    
    print(f"[INFO] Watching {SIMMODS_FILE} for changes...")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("[INFO] Stopping file watcher.")
    observer.join()

if __name__ == "__main__":
    main()
