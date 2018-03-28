Chromagnon is a set of small tools dedicated to _Chrome_/_Chromium_ forensic.

## Tools
* [ChromagnonHistory](https://github.com/JRBANCEL/Chromagnon/wiki/ChromagnonHistory-=-chromagnonHistory.py) parses **Chrome History** file
* [ChromagnonCache](https://github.com/JRBANCEL/Chromagnon/wiki/ChromagnonCache-=-chromagnonCache.py) parses **Chrome Cache** files
* [ChromagnonVisitedLinks](https://github.com/JRBANCEL/Chromagnon/wiki/ChromagnonVisitedLinks-=-chromagnonVisitedLinks.py) can verify if urls are in **Chrome Visited Links** file
* [ChromagnonDownload](https://github.com/JRBANCEL/Chromagnon/wiki/ChromagnonDownload-=-chromagnonDownload.py) parses **Chrome Downloaded Files** database

## Requirements
* Python 2.7

## Remarks
* Most of the code is Endianness dependant and tested only on little endian hosts
* The code is alignment dependant. If Chrome was compiled with custom alignment flags, it probably won't work.

## Work In Progress
I am working on reverse engineering SSNS file format : [see this page](https://github.com/JRBANCEL/Chromagnon/wiki/Reverse-Engineering-SSNS-Format) for details.

## Tests
Following cases have been tested with success
* Chromagnon on FreeBSD 9.0 amd64 parsing file from Windows 7 64bits (Chrome 20)
* Chromagnon on FreeBSD 9.0 amd64 parsing file from Linux Mint 12 amd64 (Chrome 18)
* Chromagnon on FreeBSD 9.0 amd64 parsing file from FreeBSD 9.0 amd64 (Chrome 15)
* Chromagnon on Arch Linux x86_64 parsing file from Arch Linux x86_64 (Chrome 20)

Help is welcome to test Chromagnon on other plateforms.

## License
The code is released under **New BSD License** or **Modified BSD License**. See LICENSE file for details.
