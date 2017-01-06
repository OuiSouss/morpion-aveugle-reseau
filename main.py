
#!/usr/bin/env python3

from client import *
from serveur import *

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        main_s()
    sys.exit(0)
