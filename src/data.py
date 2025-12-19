import json
import pandas as pd

chunks = []
with open("/Users/ojasdhapse/.cache/huggingface/hub/datasets--ealvaradob--phishing-dataset/snapshots/55caf9af01ae498d68ff44886ff69a4b165eb54b/texts.json") as f:
    data = json.load(f)  # Or use streaming with ijson for huge files

    for entry in data:
        flat_entry = entry.copy()
        if 'features' in entry:
            flat_entry.update(entry['features'])
            del flat_entry['features']
        chunks.append(flat_entry)

df = pd.DataFrame(chunks)
df.to_csv("data/phishing_text_dataset.csv", index=False)
