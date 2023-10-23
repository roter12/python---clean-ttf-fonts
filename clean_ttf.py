
import sys
import glob
import os.path
from fontTools import ttLib
from fontTools.ttLib import TTFont
from fontTools.misc.transform import Transform
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen

# Comic font database.
db_s = {
    'zero' : 0.68408203125, 
    'one' : 0.66748046875, 
    'two' : 0.67529296875, 
    'three' : 0.68408203125, 
    'four' : 0.66845703125, 
    'five' : 0.67724609375, 
    'six' : 0.68408203125, 
    'seven' : 0.68896484375, 
    'eight' : 0.68408203125, 
    'nine' : 0.68408203125, 
    'A' : 0.66650390625, 
    'B' : 0.66650390625, 
    'C' : 0.7001953125, 
    'D' : 0.66650390625, 
    'E' : 0.66650390625, 
    'F' : 0.66650390625, 
    'G' : 0.7001953125, 
    'H' : 0.66650390625, 
    'I' : 0.66650390625, 
    'J' : 0.80517578125, 
    'K' : 0.66650390625, 
    'L' : 0.66650390625, 
    'M' : 0.66650390625, 
    'N' : 0.66650390625, 
    'O' : 0.69970703125, 
    'P' : 0.66650390625, 
    'Q' : 0.8017578125, 
    'R' : 0.66650390625, 
    'S' : 0.7001953125, 
    'T' : 0.66650390625, 
    'U' : 0.68310546875, 
    'V' : 0.66650390625, 
    'W' : 0.66650390625, 
    'X' : 0.66650390625, 
    'Y' : 0.66650390625, 
    'Z' : 0.66650390625, 
    'a' : 0.43115234375, 
    'b' : 0.70703125, 
    'c' : 0.43115234375, 
    'd' : 0.7001953125, 
    'e' : 0.43115234375, 
    'f' : 0.6875, 
    'g' : 0.60107421875, 
    'h' : 0.68603515625, 
    'i' : 0.68359375, 
    'j' : 0.85693359375, 
    'k' : 0.68603515625, 
    'l' : 0.68603515625, 
    'm' : 0.42236328125, 
    'n' : 0.42333984375, 
    'o' : 0.43115234375, 
    'p' : 0.61572265625, 
    'q' : 0.62109375, 
    'r' : 0.42333984375, 
    's' : 0.43115234375, 
    't' : 0.55078125, 
    'u' : 0.423828125, 
    'v' : 0.4150390625, 
    'w' : 0.4150390625, 
    'x' : 0.4150390625, 
    'y' : 0.59326171875, 
    'z' : 0.4150390625
}
db_o = {
    'zero' : 0.2412109375, 
    'one' : 0.25, 
    'two' : 0.25, 
    'three' : 0.2412109375, 
    'four' : 0.25, 
    'five' : 0.2412109375, 
    'six' : 0.2412109375, 
    'seven' : 0.2412109375, 
    'eight' : 0.2412109375, 
    'nine' : 0.2412109375, 
    'A' : 0.25, 
    'B' : 0.25, 
    'C' : 0.2333984375, 
    'D' : 0.25, 
    'E' : 0.25, 
    'F' : 0.25, 
    'G' : 0.2333984375, 
    'H' : 0.25, 
    'I' : 0.25, 
    'J' : 0.111328125, 
    'K' : 0.25, 
    'L' : 0.25, 
    'M' : 0.25, 
    'N' : 0.25, 
    'O' : 0.2333984375, 
    'P' : 0.25, 
    'Q' : 0.13134765625, 
    'R' : 0.25, 
    'S' : 0.23291015625, 
    'T' : 0.25, 
    'U' : 0.2333984375, 
    'V' : 0.25, 
    'W' : 0.25, 
    'X' : 0.25, 
    'Y' : 0.25, 
    'Z' : 0.25, 
    'a' : 0.2412109375, 
    'b' : 0.22900390625, 
    'c' : 0.2412109375, 
    'd' : 0.234375, 
    'e' : 0.2412109375, 
    'f' : 0.25, 
    'g' : 0.0712890625, 
    'h' : 0.25, 
    'i' : 0.25, 
    'j' : 0.07666015625, 
    'k' : 0.25, 
    'l' : 0.25, 
    'm' : 0.25, 
    'n' : 0.25, 
    'o' : 0.2412109375, 
    'p' : 0.0634765625, 
    'q' : 0.0634765625, 
    'r' : 0.25, 
    's' : 0.2412109375, 
    't' : 0.2412109375, 
    'u' : 0.2412109375, 
    'v' : 0.25, 
    'w' : 0.25, 
    'x' : 0.25, 
    'y' : 0.07177734375, 
    'z' : 0.25
}

# Clean font.
def clean_ttf(input_file, output_file, not_scaling = False, not_align = False):
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
        if not_align == True or not hasattr(glyph, 'yMin'):
            yOffset = 0
        else:
            if glyph_name not in db_o:
                yOffset = 0
            else:
                yOffset = db_o[glyph_name] * (hhea_table.ascent - hhea_table.descent) - glyph.yMin + hhea_table.descent
        
        # Calculate yZoom
        if not_scaling == True or glyph_name not in db_s:
            yZoom = 1
        else:
            yZoom = (hhea_table.ascent - hhea_table.descent) * db_s[glyph_name] * 0.8 / (glyph.yMax - glyph.yMin)

        transformPen = TransformPen(glyphPen, Transform().translate(0, yOffset).scale(1, yZoom))
        glyph.draw(transformPen, font['glyf'])
        font['glyf'][glyph_name] = glyphPen.glyph()

    # Save
    font.save(output_file)
    # font.saveXML(f"{output_file}.xml")

# Check arguments.
if len(sys.argv) < 2:
    print("Please provide an input TTF file or directory as an argument.")
    print("If you want only align, not scaling, add '-a' option.")
    print("If you want only scaling, not align, add '-s' option.")
    print(f"Usage: python {os.path.basename(sys.argv[0])} [-a/-s] <ttf-path>")
    sys.exit(1)

# Check input file.
not_scaling = False
not_align = False
if len(sys.argv) == 3:
    ttf_path = sys.argv[2]
    not_scaling = True if sys.argv[1] == "-a" else False
    not_align = True if sys.argv[1] == "-s" else False
else:
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
    output_file = output_file.replace(".ttf", "_out.ttf")
    print(ttf_file + " -> " + output_file)
    clean_ttf(ttf_file, output_file, not_scaling, not_align)

print("\nFinished!")