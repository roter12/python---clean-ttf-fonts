
import sys
import glob
import os.path
from fontTools import ttLib
from fontTools.ttLib import TTFont
from fontTools.misc.transform import Transform
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen

# Comic font database.
db_s = {'.notdef' : 0.66650390625,'exclam' : 0.681640625,'quotedbl' : 0.24609375,'numbersign' : 0.66650390625,'dollar' : 0.83740234375,'percent' : 0.705078125,'ampersand' : 0.6943359375,'quotesingle' : 0.24609375,'parenleft' : 0.81689453125,'parenright' : 0.81689453125,'asterisk' : 0.2333984375,'plus' : 0.40625,'comma' : 0.25634765625,'hyphen' : 0.0732421875,'period' : 0.11865234375,'slash' : 0.81689453125,'zero' : 0.68408203125,'one' : 0.66748046875,'two' : 0.67529296875,'three' : 0.68408203125,'four' : 0.66845703125,'five' : 0.67724609375,'six' : 0.68408203125,'seven' : 0.68896484375,'eight' : 0.68408203125,'nine' : 0.68408203125,'colon' : 0.4306640625,'semicolon' : 0.56787109375,'less' : 0.5498046875,'equal' : 0.123046875,'greater' : 0.5498046875,'question' : 0.681640625,'at' : 0.69970703125,'A' : 0.66650390625,'B' : 0.66650390625,'C' : 0.7001953125,'D' : 0.66650390625,'E' : 0.66650390625,'F' : 0.66650390625,'G' : 0.7001953125,'H' : 0.66650390625,'I' : 0.66650390625,'J' : 0.80517578125,'K' : 0.66650390625,'L' : 0.66650390625,'M' : 0.66650390625,'N' : 0.66650390625,'O' : 0.69970703125,'P' : 0.66650390625,'Q' : 0.8017578125,'R' : 0.66650390625,'S' : 0.7001953125,'T' : 0.66650390625,'U' : 0.68310546875,'V' : 0.66650390625,'W' : 0.66650390625,'X' : 0.66650390625,'Y' : 0.66650390625,'Z' : 0.66650390625,'bracketleft' : 0.81689453125,'backslash' : 0.81689453125,'bracketright' : 0.81689453125,'asciicircum' : 0.41455078125,'underscore' : 0.0439453125,'grave' : 0.13330078125,'a' : 0.43115234375,'b' : 0.70703125,'c' : 0.43115234375,'d' : 0.7001953125,'e' : 0.43115234375,'f' : 0.6875,'g' : 0.60107421875,'h' : 0.68603515625,'i' : 0.68359375,'j' : 0.85693359375,'k' : 0.68603515625,'l' : 0.68603515625,'m' : 0.42236328125,'n' : 0.42333984375,'o' : 0.43115234375,'p' : 0.61572265625,'q' : 0.62109375,'r' : 0.42333984375,'s' : 0.43115234375,'t' : 0.55078125,'u' : 0.423828125,'v' : 0.4150390625,'w' : 0.4150390625,'x' : 0.4150390625,'y' : 0.59326171875,'z' : 0.4150390625,'braceleft' : 0.81689453125,'bar' : 0.98828125,'braceright' : 0.81689453125,'asciitilde' : 0.12060546875,'Adieresis' : 0.853515625,'Aring' : 0.88134765625,'Ccedilla' : 0.8984375,'Eacute' : 0.865234375,'Ntilde' : 0.85009765625,'Odieresis' : 0.8701171875,'Udieresis' : 0.8701171875,'aacute' : 0.63037109375,'agrave' : 0.63037109375,'acircumflex' : 0.64501953125,'adieresis' : 0.6142578125,'atilde' : 0.61572265625,'aring' : 0.64990234375,'ccedilla' : 0.61083984375,'eacute' : 0.63037109375,'egrave' : 0.63037109375,'ecircumflex' : 0.64501953125,'edieresis' : 0.6142578125,'iacute' : 0.62158203125,'igrave' : 0.62158203125,'icircumflex' : 0.63623046875,'idieresis' : 0.60546875,'ntilde' : 0.60693359375,'oacute' : 0.63037109375,'ograve' : 0.63037109375,'ocircumflex' : 0.64501953125,'odieresis' : 0.6142578125,'otilde' : 0.61572265625,'uacute' : 0.63037109375,'ugrave' : 0.63037109375,'ucircumflex' : 0.64501953125,'udieresis' : 0.6142578125,'dagger' : 0.80419921875,'degree' : 0.19921875,'cent' : 0.6044921875,'sterling' : 0.69970703125,'section' : 0.80224609375,'bullet' : 0.279296875,'paragraph' : 0.78466796875,'germandbls' : 0.6923828125,'registered' : 0.69970703125,'copyright' : 0.69970703125,'trademark' : 0.3798828125,'acute' : 0.13330078125,'dieresis' : 0.08642578125,'notequal' : 0.3427734375,'AE' : 0.66650390625,'Oslash' : 0.80029296875,'infinity' : 0.34423828125,'plusminus' : 0.48486328125,'lessequal' : 0.615234375,'greaterequal' : 0.615234375,'yen' : 0.66650390625,'mu' : 0.64697265625,'partialdiff' : 0.701171875,'summation' : 0.89990234375,'product' : 0.89990234375,'pi' : 0.4853515625,'integral' : 0.96435546875,'ordfeminine' : 0.34326171875,'ordmasculine' : 0.34326171875,'Omega' : 0.67724609375,'ae' : 0.43115234375,'oslash' : 0.546875,'questiondown' : 0.681640625,'exclamdown' : 0.681640625,'logicalnot' : 0.2666015625,'radical' : 0.8232421875,'florin' : 0.88037109375,'approxequal' : 0.2763671875,'Delta' : 0.6826171875,'guillemotleft' : 0.2841796875,'guillemotright' : 0.2841796875,'ellipsis' : 0.11865234375,'Agrave' : 0.865234375,'Atilde' : 0.85009765625,'Otilde' : 0.86669921875,'OE' : 0.6748046875,'oe' : 0.43115234375,'endash' : 0.0732421875,'emdash' : 0.0732421875,'quotedblleft' : 0.255859375,'quotedblright' : 0.25634765625,'quoteleft' : 0.255859375,'quoteright' : 0.25634765625,'divide' : 0.3486328125,'lozenge' : 0.71875,'ydieresis' : 0.78369140625,'Ydieresis' : 0.853515625,'fraction' : 0.66650390625,'Euro' : 0.68359375,'guilsinglleft' : 0.2841796875,'guilsinglright' : 0.2841796875,'fi' : 0.6875,'fl' : 0.6875,'daggerdbl' : 0.8125,'periodcentered' : 0.16552734375,'quotesinglbase' : 0.25634765625,'quotedblbase' : 0.25634765625,'perthousand' : 0.705078125,'Acircumflex' : 0.86328125,'Ecircumflex' : 0.86328125,'Aacute' : 0.865234375,'Edieresis' : 0.853515625,'Egrave' : 0.865234375,'Iacute' : 0.865234375,'Icircumflex' : 0.86328125,'Idieresis' : 0.853515625,'Igrave' : 0.865234375,'Oacute' : 0.8818359375,'Ocircumflex' : 0.8798828125,'apple' : 0.71923828125,'Ograve' : 0.8818359375,'Uacute' : 0.8818359375,'Ucircumflex' : 0.8798828125,'Ugrave' : 0.8818359375,'dotlessi' : 0.42333984375,'circumflex' : 0.13720703125,'tilde' : 0.09375,'macron' : 0.0458984375,'breve' : 0.1201171875,'dotaccent' : 0.0859375,'ring' : 0.15966796875,'cedilla' : 0.1884765625,'hungarumlaut' : 0.13330078125,'ogonek' : 0.12646484375,'caron' : 0.13720703125,'Scaron' : 0.88037109375,'scaron' : 0.6318359375,'brokenbar' : 0.8330078125,'Eth' : 0.66650390625,'eth' : 0.689453125,'Yacute' : 0.865234375,'yacute' : 0.7998046875,'Thorn' : 0.66650390625,'thorn' : 0.8720703125,'multiply' : 0.3701171875,'onesuperior' : 0.400390625,'twosuperior' : 0.4052734375,'threesuperior' : 0.41064453125,'onehalf' : 0.6669921875,'onequarter' : 0.6669921875,'threequarters' : 0.671875,'.notdef#3' : 0.095703125,'.notdef#4' : 0.1201171875,'.notdef#5' : 0.1201171875,'.notdef#6' : 0.1240234375,'.notdef#7' : 0.09375,'.notdef#8' : 0.095703125,'.notdef#9' : 0.1201171875,'.notdef#10' : 0.1201171875,'.notdef#11' : 0.1240234375,'.notdef#12' : 0.095703125,'.notdef#13' : 0.1201171875,'.notdef#14' : 0.1201171875,'.notdef#15' : 0.1240234375,'.notdef#16' : 0.09375,'.notdef#17' : 0.095703125,'.notdef#18' : 0.1201171875,'.notdef#19' : 0.1201171875,'.notdef#20' : 0.1240234375,'.notdef#21' : 0.09375,'.notdef#22' : 0.1240234375,'.notdef#23' : 0.095703125,'.notdef#24' : 0.1201171875,'.notdef#25' : 0.1201171875,'.notdef#26' : 0.1240234375,'.notdef#27' : 0.095703125,'.notdef#28' : 0.08642578125,'currency' : 0.4208984375}
db_o = {'.notdef' : 0.25,'exclam' : 0.24169921875,'quotedbl' : 0.67919921875,'numbersign' : 0.25,'dollar' : 0.15771484375,'percent' : 0.15673828125,'ampersand' : 0.2333984375,'quotesingle' : 0.67919921875,'parenleft' : 0.1298828125,'parenright' : 0.1298828125,'asterisk' : 0.69189453125,'plus' : 0.37353515625,'comma' : 0.1044921875,'hyphen' : 0.42529296875,'period' : 0.24169921875,'slash' : 0.1298828125,'zero' : 0.2412109375,'one' : 0.25,'two' : 0.25,'three' : 0.2412109375,'four' : 0.25,'five' : 0.2412109375,'six' : 0.2412109375,'seven' : 0.2412109375,'eight' : 0.2412109375,'nine' : 0.2412109375,'colon' : 0.24169921875,'semicolon' : 0.1044921875,'less' : 0.31396484375,'equal' : 0.51513671875,'greater' : 0.31396484375,'question' : 0.24169921875,'at' : 0.2333984375,'A' : 0.25,'B' : 0.25,'C' : 0.2333984375,'D' : 0.25,'E' : 0.25,'F' : 0.25,'G' : 0.2333984375,'H' : 0.25,'I' : 0.25,'J' : 0.111328125,'K' : 0.25,'L' : 0.25,'M' : 0.25,'N' : 0.25,'O' : 0.2333984375,'P' : 0.25,'Q' : 0.13134765625,'R' : 0.25,'S' : 0.23291015625,'T' : 0.25,'U' : 0.2333984375,'V' : 0.25,'W' : 0.25,'X' : 0.25,'Y' : 0.25,'Z' : 0.25,'bracketleft' : 0.1298828125,'backslash' : 0.1298828125,'bracketright' : 0.1298828125,'asciicircum' : 0.53564453125,'underscore' : 0.1181640625,'grave' : 0.73828125,'a' : 0.2412109375,'b' : 0.22900390625,'c' : 0.2412109375,'d' : 0.234375,'e' : 0.2412109375,'f' : 0.25,'g' : 0.0712890625,'h' : 0.25,'i' : 0.25,'j' : 0.07666015625,'k' : 0.25,'l' : 0.25,'m' : 0.25,'n' : 0.25,'o' : 0.2412109375,'p' : 0.0634765625,'q' : 0.0634765625,'r' : 0.25,'s' : 0.2412109375,'t' : 0.2412109375,'u' : 0.2412109375,'v' : 0.25,'w' : 0.25,'x' : 0.25,'y' : 0.07177734375,'z' : 0.25,'braceleft' : 0.1298828125,'bar' : 0.005859375,'braceright' : 0.1298828125,'asciitilde' : 0.86279296875,'Adieresis' : 0.25,'Aring' : 0.25,'Ccedilla' : 0.03515625,'Eacute' : 0.25,'Ntilde' : 0.25,'Odieresis' : 0.2333984375,'Udieresis' : 0.2333984375,'aacute' : 0.2412109375,'agrave' : 0.2412109375,'acircumflex' : 0.2412109375,'adieresis' : 0.2412109375,'atilde' : 0.2412109375,'aring' : 0.2412109375,'ccedilla' : 0.0615234375,'eacute' : 0.2412109375,'egrave' : 0.2412109375,'ecircumflex' : 0.2412109375,'edieresis' : 0.2412109375,'iacute' : 0.25,'igrave' : 0.25,'icircumflex' : 0.25,'idieresis' : 0.25,'ntilde' : 0.25,'oacute' : 0.2412109375,'ograve' : 0.2412109375,'ocircumflex' : 0.2412109375,'odieresis' : 0.2412109375,'otilde' : 0.2412109375,'uacute' : 0.2412109375,'ugrave' : 0.2412109375,'ucircumflex' : 0.2412109375,'udieresis' : 0.2412109375,'dagger' : 0.12109375,'degree' : 0.72607421875,'cent' : 0.244140625,'sterling' : 0.2333984375,'section' : 0.123046875,'bullet' : 0.4501953125,'paragraph' : 0.1318359375,'germandbls' : 0.2412109375,'registered' : 0.2333984375,'copyright' : 0.2333984375,'trademark' : 0.53662109375,'acute' : 0.73828125,'dieresis' : 0.76904296875,'notequal' : 0.4052734375,'AE' : 0.25,'Oslash' : 0.18310546875,'infinity' : 0.41162109375,'plusminus' : 0.294921875,'lessequal' : 0.25,'greaterequal' : 0.25,'yen' : 0.25,'mu' : 0.060546875,'partialdiff' : 0.23583984375,'summation' : 0.0166015625,'product' : 0.0166015625,'pi' : 0.23193359375,'integral' : -0.01318359375,'ordfeminine' : 0.58154296875,'ordmasculine' : 0.58154296875,'Omega' : 0.25,'ae' : 0.2412109375,'oslash' : 0.18994140625,'questiondown' : -0.00927734375,'exclamdown' : -0.00927734375,'logicalnot' : 0.25,'radical' : 0.25,'florin' : 0.10986328125,'approxequal' : 0.43603515625,'Delta' : 0.25,'guillemotleft' : 0.31787109375,'guillemotright' : 0.31787109375,'ellipsis' : 0.24169921875,'Agrave' : 0.25,'Atilde' : 0.25,'Otilde' : 0.2333984375,'OE' : 0.24609375,'oe' : 0.2412109375,'endash' : 0.42529296875,'emdash' : 0.42529296875,'quotedblleft' : 0.67724609375,'quotedblright' : 0.67724609375,'quoteleft' : 0.67724609375,'quoteright' : 0.67724609375,'divide' : 0.40234375,'lozenge' : 0.22412109375,'ydieresis' : 0.07177734375,'Ydieresis' : 0.25,'fraction' : 0.25,'Euro' : 0.2412109375,'guilsinglleft' : 0.31787109375,'guilsinglright' : 0.31787109375,'fi' : 0.25,'fl' : 0.25,'daggerdbl' : 0.11279296875,'periodcentered' : 0.5107421875,'quotesinglbase' : 0.1044921875,'quotedblbase' : 0.1044921875,'perthousand' : 0.15673828125,'Acircumflex' : 0.25,'Ecircumflex' : 0.25,'Aacute' : 0.25,'Edieresis' : 0.25,'Egrave' : 0.25,'Iacute' : 0.25,'Icircumflex' : 0.25,'Idieresis' : 0.25,'Igrave' : 0.25,'Oacute' : 0.2333984375,'Ocircumflex' : 0.2333984375,'apple' : 0.22216796875,'Ograve' : 0.2333984375,'Uacute' : 0.2333984375,'Ucircumflex' : 0.2333984375,'Ugrave' : 0.2333984375,'dotlessi' : 0.25,'circumflex' : 0.7490234375,'tilde' : 0.76318359375,'macron' : 0.78955078125,'breve' : 0.75537109375,'dotaccent' : 0.76953125,'ring' : 0.7314453125,'cedilla' : 0.0615234375,'hungarumlaut' : 0.73828125,'ogonek' : 0.12353515625,'caron' : 0.73583984375,'Scaron' : 0.23291015625,'scaron' : 0.2412109375,'brokenbar' : 0.08349609375,'Eth' : 0.25,'eth' : 0.2412109375,'Yacute' : 0.25,'yacute' : 0.07177734375,'Thorn' : 0.25,'thorn' : 0.0634765625,'multiply' : 0.3916015625,'onesuperior' : 0.5166015625,'twosuperior' : 0.5166015625,'threesuperior' : 0.51123046875,'onehalf' : 0.25,'onequarter' : 0.25,'threequarters' : 0.25,'.notdef#3' : 1.0078125,'.notdef#4' : 0.9951171875,'.notdef#5' : 0.9951171875,'.notdef#6' : 0.9892578125,'.notdef#7' : 1.00634765625,'.notdef#8' : 1.0078125,'.notdef#9' : 0.9951171875,'.notdef#10' : 0.9951171875,'.notdef#11' : 0.9892578125,'.notdef#12' : 1.0078125,'.notdef#13' : 0.9951171875,'.notdef#14' : 0.9951171875,'.notdef#15' : 0.9892578125,'.notdef#16' : 1.00634765625,'.notdef#17' : 1.0078125,'.notdef#18' : 0.9951171875,'.notdef#19' : 0.9951171875,'.notdef#20' : 0.9892578125,'.notdef#21' : 1.00634765625,'.notdef#22' : 0.9892578125,'.notdef#23' : 1.0078125,'.notdef#24' : 0.9951171875,'.notdef#25' : 0.9951171875,'.notdef#26' : 0.9892578125,'.notdef#27' : 1.0078125,'.notdef#28' : 0.76904296875,'currency' : 0.36181640625}

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