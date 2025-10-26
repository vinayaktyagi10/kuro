
#!/usr/bin/env python3

import sys
import os

# Add kuro's directory to sys.path for imports like mistral_agent
sys.path.insert(0, os.path.expanduser("~/kuro"))

from kuro import main  # assuming kuro.py has main()

if __name__ == "__main__":
    main(sys.argv)
