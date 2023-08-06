
# ![Windows flag waving in the digital wind](https://raw.githubusercontent.com/npjg/microsoft-easter-eggs/main/examples/Windows%20Flag.gif) Microsoft Easter Eggs
This repository holds Python scripts to extract
the assets for Easter eggs from Microsoft products. Only extraction logic is provided; you must have access to the required original file(s) from the original Microsoft products.
For more information on the required file(s) for each easter egg, install the package from PyPI and run `MicrosoftEasterEggs -h`.

## Installation
Get it [on PyPI](https://pypi.org/project/MicrosoftEasterEggs/): ```pip3 install MicrosoftEasterEggs```

## Usage
If you install via `pip`, you can use the installed `MicrosoftEasterEggs` script, which includes subcommands for specific easter eggs:
```
MicrosoftEasterEggs windows31-credits ~/WINDOWS/SYSTEM/SHELL.DLL ~/Desktop
```

You can also use the code as a library and do your own export:
```{python}
from MicrosoftEasterEggs.windows31 import credits

windows31_credits = credits.Windows31Credits('/home/developer/WINDOWS/SYSTEM/SHELL.DLL')
windows31_credits.export('/home/developer')
```

## Current Support
* Windows 3.1
  * Credits (Program Manager)