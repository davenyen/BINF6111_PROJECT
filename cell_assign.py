import os
import sys

# Read in matrix csv
# - Associate barcode from read one to sequence in read two
# - When file is list of groups, a list of cell barcodes from those groups are
# created
# - Identify cell barcode from read one, allocate sequence from read 2 to a
# particular group 