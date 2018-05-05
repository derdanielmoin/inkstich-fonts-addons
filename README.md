# Inkscape extensions for inkstich fonts

In this git there are three extensions for inkscape to help using fonts in inkstich. The main idea
is to create each character as an own path for the font that is used once and save these pathes in
a defined format. After this create a new svg, write the text that you would stich, convert it to a
path and use this extension to replace all charachters. Then you only habe to do little corrections
for connecting script fonts.

This repository contains three extensions. Two for create the replacement files for the fonts and one
to actually do the replacement. There are in the extensions folder.

The add_prefix extension adds converts the label of an object in inkscape to the id and adds the given prefix
to the id. After this it deletes the label. If no label exists, it adds only the prefix.

The export_chars extension saves the selected chars and the created curves for satin stich or fill stich.
It depends on the font size and the name of the selected objects! 

The replace_chars extension finally replaces the selected text with the above created charachters.

The extensions are only tested under linux. If you want to use it with windows, you must at least replace the path
of the json file that saves the font data to a valid windows path. Then maybe it works also in windows.

## How to use the extensions

You will need the master version of inkscape, because there are some fixes in there that are needed
for the extensions. Copy (or symbolic link) the files in the "extensions" directory to inkscape-extension
directory. (~/.config/inkscape/extensions for linux). Then the extensions are located under extensions -> Inkstich fonts.
The idea to use this is the following:

For a fixed font and a fixed size (and style) do the following:

- Create a svg in inkscape and write all charachters in all combinations that the font replace with single curves.
- Convert the text to pathes and group each charachter in a single group
- Rename the group (with objects panel) to letter
- Use the "add prefix ..."-addon in extensions -> inkstich fonts menu to rename this groups to "small_..." or
"big_..." or other combinations needed.
- In each charachter group dublicate the path. The unchanched original path must be the most down path in the group.
This one is used internal in the addon to later replace the stich text with the abouve pathes. The other could
be used to to make the satin stich. Multiple pathes are allowed. For script fonts it is a good idea to
arrange them in writing order.
- next mark all letter groups and use "export chars..." in extensions -> inkstich fonts menu. this creates or adds to
a file that contains all the charachters. they are stored in a map with index: font name + size + name of the group.
if you run twice, same indices are replaced.
- Next you could create your stiching svg and write some text.
- Convert this text to pathes and use "replace chars..." from extensions -> inkstich fonts.
- make (hopefully little) changes that are nessesary and stich your text!

## Licences

The python code is Licenced under GPL. The example fonts are Licenced under OFL. Hopefully this is
a useful combination.
