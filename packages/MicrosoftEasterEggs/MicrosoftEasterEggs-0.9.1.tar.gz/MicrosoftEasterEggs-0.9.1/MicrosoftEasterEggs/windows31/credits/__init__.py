
import os 
import json

import jsons
import nefile
from nefile.resource_table import ResourceType

from .resources import text
from .resources import flag
from .resources import emcees

## Models the credits screen in the Windows 3.1 Program Manager.
## @param[in] windows_31_shell_dll_filepath - The filepath to SHELL.DLL, which contains the easter egg.
##            Must contain the following resources:
##              - RT_BITMAP, 9997 (Windows flag)
##              - RT_BITMAP, 9998 (Emcees)
##              - RT_RCDATA, 9999 (Encrypted credits text)
class Windows31Credits:
    def __init__(self, windows_31_shell_dll_filepath):
        self.shell_dll = nefile.NE(windows_31_shell_dll_filepath)

    def export(self, export_folder_path):
        # The Windows flag animation.
        windows_flag_animation_filepath = os.path.join(export_folder_path, 'Windows Flag.gif')
        self.windows_flag_animation.save_as_animated_gif(windows_flag_animation_filepath)
        # The credit backgrounds (with emcees).
        for emcee in self.emcees:
            emcee_image_filepath = os.path.join(export_folder_path, f'{emcee.name}.bmp')
            emcee.image.save(emcee_image_filepath)
        # The decrypted and parsed credit text.
        credits_filepath = os.path.join(export_folder_path, 'credits.json')
        with open(credits_filepath, 'w') as credits_file:
            json.dump(self.credits_text, credits_file)

    ## Recreates the Windows flag animation.
    ## Can save as an animated GIF with the proper framerate, or 
    ## the individual images can be accessed.
    @property
    def windows_flag_animation(self):
        return flag.Windows31FlagAnimation(self.shell_dll)

    ## Recreates each of the 4 emcees that can present the Windows 3.1 credits:
    ##  - Steve Ballmer
    ##  - Bill Gates
    ##  - Brad Silverberg (bradsi)
    ##  - T-Bear
    @property
    def emcees(self):
        return emcees.Windows31CreditEmcees(self.shell_dll).emcees

    ## Decrypts and parses the text of the Windows 3.1 credits.
    ## @return A list of lists of the credits data.
    @property
    def credits_text(self):
        credits_text = text.Windows31CreditsText(self.shell_dll)
        return jsons.dump(credits_text)
