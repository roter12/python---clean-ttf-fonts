
import sys
import glob
import os.path
from fontTools import ttLib
from fontTools.ttLib import TTFont
from fontTools.misc.transform import Transform
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen

# Comic font database.
db = { 'zero' : 0.5585143658023827, 'one' : 0.5466012613875263, 'two' : 0.5392431674842326, 'three' : 0.5508058864751226, 'four' : 0.5557112824106517, 'five' : 0.5630693763139454, 'six' : 0.5704274702172389, 'seven' : 0.5515066573230554, 'eight' : 0.555010511562719, 'nine' : 0.571478626489138, 'A' : 0.5283812193412754, 'B' : 0.5672740014015417, 'C' : 0.5420462508759636, 'D' : 0.5798878766643307, 'E' : 0.5970567624386826, 'F' : 0.5882971268395235, 'G' : 0.5746320953048353, 'H' : 0.5735809390329363, 'I' : 0.5360896986685354, 'J' : 0.5728801681850035, 'K' : 0.5749824807288016, 'L' : 0.5728801681850035, 'M' : 0.566573230553609, 'N' : 0.5711282410651717, 'O' : 0.5522074281709881, 'P' : 0.5588647512263489, 'Q' : 0.684302733006307, 'R' : 0.5522074281709881, 'S' : 0.5339873861247372, 'T' : 0.5346881569726699, 'U' : 0.5406447091800981, 'V' : 0.5658724597056762, 'W' : 0.5683251576734408, 'X' : 0.5623686054660126, 'Y' : 0.5574632095304836, 'Z' : 0.5466012613875263, 'a' : 0.38892782060266295, 'b' : 0.566573230553609, 'c' : 0.3945339873861247, 'd' : 0.5746320953048353, 'e' : 0.382270497547302, 'f' : 0.6163279607568325, 'g' : 0.5564120532585844, 'h' : 0.5830413454800281, 'i' : 0.5266292922214436, 'j' : 0.7333566923615977, 'k' : 0.5763840224246671, 'l' : 0.5788367203924317, 'm' : 0.43237561317449197, 'n' : 0.40749824807288015, 'o' : 0.3840224246671338, 'p' : 0.5886475122634899, 'q' : 0.5679747722494745, 'r' : 0.3927820602662929, 's' : 0.42116327960756833, 't' : 0.5119131044148564, 'u' : 0.401541695865452, 'v' : 0.3840224246671338, 'w' : 0.39348283111422566, 'x' : 0.4025928521373511, 'y' : 0.5672740014015417, 'z' : 0.39698668535388926 }

# Clean font.
def clean_ttf(input_file, output_file):
    font = TTFont(input_file)
    hhea_table = font['hhea']
    glyphPen = TTGlyphPen(font.getGlyphSet())

    # Iterate through each glyph in the font
    for glyph_name in font.getGlyphOrder():
        glyph = font['glyf'][glyph_name]

        # Avoid double-transforming composite glyphs
        if glyph.isComposite():
            continue

        # Calculate yOffset
        if not hasattr(glyph, 'yMin'):
            yOffset = 0
        else:
            if glyph_name in ['g', 'j', 'p', 'q', 'y', 'comma', 'quotesingle', 'quotedbl', 'hyphenminus', 'asterisk', 'equal', 'asciicircum', 'grave', 'asciitilde']:
                if glyph_name in ['g', 'j', 'p', 'q', 'y']:
                    yOffset = glyph.yMin - hhea_table.descent
                else:
                    yOffset = 0
            else:
                yOffset = glyph.yMin
        
        # Calculate yZoom
        if glyph_name not in db:
            yZoom = 1
        else:
            yZoom = (hhea_table.ascent - hhea_table.descent) * db[glyph_name] / (glyph.yMax - glyph.yMin)

        transformPen = TransformPen(glyphPen, Transform().translate(0, -yOffset*yZoom).scale(1, yZoom))
        glyph.draw(transformPen, font['glyf'])
        font['glyf'][glyph_name] = glyphPen.glyph()

    # Save
    font.save(output_file)
    # font.saveXML(f"{output_file}.xml")

# Check arguments.
if len(sys.argv) < 2:
    print("Please provide an input TTF file or directory as an argument.")
    print(f"Usage: python {os.path.basename(sys.argv[0])} <ttf-path>")
    sys.exit(1)

# Check input file.
ttf_path = sys.argv[1]
ttf_files = []
if os.path.isdir(ttf_path):
    for file_path in glob.glob(ttf_path + os.sep +"*.ttf"):
        ttf_files.append(file_path)

    if len(ttf_files) == 0:
        print("No TTF file in directory: " + ttf_path)
        exit(1)

    output_dir = ttf_path + os.sep + "output" + os.sep
else:
    if not os.path.isfile(ttf_path):
        print(f"Wrong argument: {ttf_path}")
        print("Please provide an input TTF file or directory as an argument.")
        sys.exit(1)

    ttf_files.append(ttf_path)
    output_dir = os.path.dirname(ttf_path) + os.sep + "output" + os.sep


# Make output directory.
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

# Clean input file.
for ttf_file in ttf_files:
    output_file = output_dir + os.path.basename(ttf_file)
    print(ttf_file + " -> " + output_file)
    clean_ttf(ttf_file, output_file)

print("\nFinished!")