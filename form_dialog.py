'''
This module implements generic forms (see forms.py and form_widgets.py) within
a dialog.
'''

import tkinter as tk
import tkinter.ttk as ttk
#from tkinter.messagebox import showerror, showinfo, askyesno
from database import Database
#from form_widgets import *
#from forms import DialogForm
#from dialogs import *
from logger import *

@class_wrapper
class FormDialog(tk.Toplevel):
    '''
    A form dialog is a stand-alone mini-application that is self-contained and does
    not interact with the rest of the program except through the database.
    '''

    def __init__(self, owner, **kw):

        super().__init__(owner)
        self.transient(parent)

        self.logger.set_level(Logger.DEBUG)

        self.owner = owner
        self.logger.set_level(Logger.DEBUG)
        self.outer_frame = tk.Frame(self)
        self.frame = tk.Frame(self.outer_frame)
        self.frame.grid(row=0, column=0)
        tk.Button(self.outer_frame, text="Dismiss", width=15, command=_dismiss_cb).grid(row=1, column=0)
        self.hide()

    @func_wrapper
    def show(self):
        '''
        Display the dialog, after it has been created.
        '''
        self.update()
        self.deiconify()
        self.load_form()

    @func_wrapper
    def hide(self):
        '''
        Hide the dialog. This is for the external interface.
        '''
        self.withdraw()

    @func_wrapper
    def get_frame(self):
        '''
        Return the frame to place the form into.
        '''
        return self.frame

    @func_wrapper
    def destroy(self):
        '''
        Override the base class to prevent the dialog from being destroyed when the
        close button is pressed in the system menu.
        '''
        self.hide()

    @func_wrapper
    def _dismiss_cb(self):
        '''
        Hide the dialog without destroying it.
        '''
        self.hide()

    def load_form(self):
        '''
        Load the form from the database. This must be overridden.
        '''
        raise Exception("load_form() in FormDialog must have override.")

    def save_form(self):
        '''
        Save the form to the database.  This must be overridden.
        '''
