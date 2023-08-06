from pathlib import Path
import sys
if str(Path(__file__).parent) not in sys.path:
    sys.path.append(str(Path(__file__).parent))
from generic import Generic
