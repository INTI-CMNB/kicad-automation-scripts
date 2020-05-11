# Default W,H for recording
REC_W = 1366
REC_H = 768

# Return error codes
# Positive values are ERC/DRC errors
NO_SCHEMATIC = 1
EESCHEMA_CFG_PRESENT = 2
KICAD_CFG_PRESENT = 3
NO_PCB = 4
PCBNEW_CFG_PRESENT = 5
WRONG_LAYER_NAME = 6
WRONG_PCB_NAME = 7
WRONG_SCH_NAME = 8
PCBNEW_ERROR = 9
# Wait 25 s to pcbnew/eeschema window to be present
WAIT_START = 25


__version__ = '1.1.6'
