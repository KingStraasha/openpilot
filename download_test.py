from openpilot.common.params import Params
from openpilot.sunnypilot.models.fetcher import ModelFetcher
from openpilot.sunnypilot.models.manager import ModelManagerSP

params = Params()
fetcher = ModelFetcher(params)
bundles = fetcher.get_available_bundles()
if bundles:
    print("Bundles available:", len(bundles))
    try:
        manager = ModelManagerSP()
        manager._download_bundle(bundles[0], "/tmp/models_test")
        print("Success")
    except Exception as e:
        import traceback
        traceback.print_exc()
else:
    print("No bundles")
