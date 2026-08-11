import os
import capnp
from importlib.resources import as_file, files

capnp.remove_import_hook()

with as_file(files("openpilot.cereal")) as fspath, as_file(files("opendbc")) as opendbc_path:
  CEREAL_PATH = fspath.as_posix()
  opendbc_dir = os.path.realpath(opendbc_path.as_posix())
  opendbc_import_path = os.path.join(opendbc_dir, 'car')
  if not os.path.exists(os.path.join(opendbc_import_path, 'car.capnp')):
    root = os.path.dirname(os.path.dirname(CEREAL_PATH))
    alt_opendbc = os.path.join(root, 'opendbc_repo', 'opendbc', 'car')
    if os.path.exists(os.path.join(alt_opendbc, 'car.capnp')):
      opendbc_import_path = alt_opendbc
  log = capnp.load(os.path.join(CEREAL_PATH, "log.capnp"), imports=[CEREAL_PATH, opendbc_dir, opendbc_import_path])
  custom = capnp.load(os.path.join(CEREAL_PATH, "custom.capnp"), imports=[CEREAL_PATH, opendbc_dir, opendbc_import_path])
  car = capnp.load(os.path.join(opendbc_import_path, "car.capnp"), imports=[CEREAL_PATH, opendbc_dir, opendbc_import_path])
