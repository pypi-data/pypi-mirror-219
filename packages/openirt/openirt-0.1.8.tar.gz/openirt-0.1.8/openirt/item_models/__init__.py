from pathlib import Path
import sys
if str(Path(__file__).parent) not in sys.path:
    sys.path.append(str(Path(__file__).parent))
from model import Model
from pl1 import PL1
from pl2 import PL2
from pl3 import PL3
# from norm import Norm
