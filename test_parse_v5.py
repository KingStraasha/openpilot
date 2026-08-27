import json

with open("models_v5.json") as f:
    data = json.load(f)

bundles = []
for key, b_data in data.items():
    bundle = {}
    bundle["index"] = int(b_data.get("index", 0))
    bundle["internalName"] = str(key)
    bundle["displayName"] = str(b_data.get("display_name") or "")
    bundle["generation"] = int(b_data.get("generation") or 0)
    bundle["environment"] = str(b_data.get("environment") or "")
    
    # In v5, we have one supercombo model.
    model = {}
    model["type"] = "supercombo"
    
    artifact = {}
    artifact["fileName"] = str(b_data.get("file_name") or "")
    artifact["downloadUri"] = b_data.get("download_uri", {})
    model["artifact"] = artifact
    
    metadata = {}
    metadata["fileName"] = str(b_data.get("file_name_metadata") or "")
    metadata["downloadUri"] = b_data.get("download_uri_metadata", {})
    model["metadata"] = metadata
    
    bundle["models"] = [model]
    
    # We might have a nav model too?
    if b_data.get("file_name_nav"):
        nav_model = {}
        nav_model["type"] = "navigation"
        nav_artifact = {}
        nav_artifact["fileName"] = str(b_data.get("file_name_nav") or "")
        nav_artifact["downloadUri"] = b_data.get("download_uri_nav", {})
        nav_model["artifact"] = nav_artifact
        nav_model["metadata"] = {}
        bundle["models"].append(nav_model)
        
    bundle["ref"] = str(b_data.get("full_name") or "")
    
    bundles.append(bundle)

print(json.dumps(bundles[0], indent=2))
