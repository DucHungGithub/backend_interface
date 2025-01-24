import os
import json

trace = {}

# Add directory existence check and error handling
directory = "non_reroute_"
if not os.path.exists(directory):
    print(f"Error: Directory '{directory}' does not exist")
    exit(1)

try:
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        # print(file_path)
        with open(file_path, "r") as f:
            data_read = f.read()
            data = json.loads(data_read)
            try:
                _ = data["name"]
                if data.get("name") not in trace:
                    trace[data.get("name")] = file_path
                else:
                    os.remove(file_path)
            except Exception as e:
                print("Exception: ", file_path)
                print("-------")
except Exception as e:
    print(f"Error accessing directory: {e}")

print(f"Total unique names found: {len(trace.keys())}")

    
    

