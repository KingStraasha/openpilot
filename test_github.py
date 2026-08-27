import requests
import json
url = "https://api.github.com/repos/sunnypilot/sunnypilot/commits?path=selfdrive/ui/sunnypilot/models/fetcher.py&per_page=5"
response = requests.get(url)
if response.status_code == 200:
    for commit in response.json():
        print(f"Commit: {commit['commit']['message']}")
        print(f"Date: {commit['commit']['author']['date']}")
        print(f"URL: {commit['html_url']}")
        print("---")
else:
    print(f"Failed: {response.status_code}")
