# Elminage-Yami-no-Miko-to-Kamigami-no-Yubiwa-PS2-English-Patch
Attempt at making an English translation patch for Playstation 2 version of "Elminage: Priestess of Darkness and the Ring of the Gods".

## What is possible right now:
* Reinsertion of edited graphics.
* Translation of text stored in .CSV files and an ELF file.
* Translation of text stored in SCD.BIN is limited by lenght of original string x 2 (1 byte per ascii vs 2 bytes per shift-jis).

Currently looking into SCDXX.BIN files. As I uploaded the breakdown below, I've noticed a mistake with the edited "not working" file... Offset to the single not 0x2303 value is wrong. Changing it to correct 0xC5 lets me interact with the shade.

<img src="WIP/SCD.webp" width="1560" height="912"/>
