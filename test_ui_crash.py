import sys
import mock
sys.modules['pyray'] = mock.MagicMock()

# We need to mock a ton of OpenPilot imports...
