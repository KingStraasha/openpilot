import requests
import re
import json

html = requests.get("https://sunnylink-wiki-service-32842449811.us-central1.run.app/models").text
match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
if match:
    data = json.loads(match.group(1))
    print(json.dumps(data)[:500])
else:
    # Next.js app dir structure uses self.__next_f
    lines = html.split('\n')
    for line in lines:
        if 'models_v' in line or 'driving_models' in line:
            print(line[:200])
