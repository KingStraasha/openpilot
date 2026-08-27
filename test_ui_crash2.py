from openpilot.common.params import Params
params = Params()
print("Putting string...")
params.put("ModelManager_DownloadIndex", "1")
print("Putting int...")
params.put("ModelManager_DownloadIndex", 1)
