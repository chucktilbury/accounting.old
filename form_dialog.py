'''
This module implements generic forms (see forms.py and form_widgets.py) within
a dialog.
'''

import tkinter as tk
import tkinter.ttk as ttk
#from tkinter.messagebox import showerror, showinfo, askyesno
from database import Database
from form_widgets import *
#from dialogs import *
from logger import *

@class_wrapper
class FormDialog(tk.Toplevel):
    '''
    A form dialog is a stand-alone mini-application that is self-contained and does
    not interact with the rest of the program except through the database.
    '''

    def __init__(self, owner, table, **kw):

        super().__init__(owner)
        self.transient(parent)

        self.logger.set_level(Logger.DEBUG)
        #self.data = Database.get_instance()

