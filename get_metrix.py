
import sys
import os.path
from fontTools import ttLib
from fontTools.ttLib import TTFont

# Clean font.
def get_metrix(input_file):
    font = TTFont(input_file)
    hhea_table = font['hhea']

    print(f"'hhea' : ascent = {hhea_table.ascent}, descent = {hhea_table.descent}")

    # Iterate through each glyph in the font
    for glyph_name in font.getGlyphOrder():
        glyph = font['glyf'][glyph_name]
        yMax = glyph.yMax if hasattr(glyph, 'yMax') else None
        yMin = glyph.yMin if hasattr(glyph, 'yMin') else None
        
        #print(f"'{glyph_name}' : yMax = {yMax}, yMin = {yMin}")
        if yMax != None:
            #print(f"'{glyph_name}' : {(yMax-yMin)/(hhea_table.ascent-hhea_table.descent)},") # scale
            print(f"'{glyph_name}' : {(yMin-hhea_table.descent)/(hhea_table.ascent-hhea_table.descent)},") # offset

# Check arguments.
if len(sys.argv) < 2:
    print("Please provide an input TTF file as an argument.")
    print(f"Usage: python {os.path.basename(sys.argv[0])} <ttf-path>")
    sys.exit(1)

# Check input file.
input_filename = sys.argv[1]
if not os.path.isfile(input_filename):
    print(f"Error: Not exists - {input_filename}")
    sys.exit(1)

# Get font metrix.
get_metrix(input_filename)