#!/usr/bin/env python3
import sys

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo, askyesno
from tkinter.filedialog import askopenfilename
from database import Database

from notebook import Notebook
from setup_forms import *
from main_forms import *
from dialogs import HelpDialog
from importer import ImportPayPal

class MainFrame(object):
    '''
    Main entry point of program.
    '''
    def __init__(self):
        self.master = tk.Tk()
        self.master.geometry('950x500')
        #self.master.resizable(0, 0)
        self.master.wm_title("Accounting")

        self.data = Database.get_instance()

        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self._do_open)
        filemenu.add_separator()
        filemenu.add_command(label="Import PayPal", command=self._do_import)
        filemenu.add_separator()
        filemenu.add_command(label="Backup Database", command=self._do_backup)
        filemenu.add_command(label="Restore Database", command=self._do_restore)
        filemenu.add_command(label="Clear Database", command=self._do_clear)
        filemenu.add_separator()
        # TODO: Add backup/restore for customers and vendors.
        filemenu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # TODO: Add reports on menu. (see notes.txt)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help", command=self._do_help)
        helpmenu.add_command(label="About", command=self._do_about)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.master.config(menu=menubar)

        # TODO: Show balance/P&L sheet on home tab.
        nb1 = Notebook(self.master, ['Home', 'Customers', 'Vendors', 'Sales', 'Purchases', 'Setup'])
        CustomersForm(nb1)
        VendorsForm(nb1)
        nb1.show_tab(0)

        nb2 = Notebook(nb1.get_frame(nb1.get_tab_index('Setup')), ['Business', 'Accounts', 'Inventory'])
        BusinessForm(nb2)
        AccountsForm(nb2)
        InventoryForm(nb2)
        nb2.show_tab(0)

    def main(self):
        self.master.mainloop()

    def _do_import(self):
        fname = askopenfilename(initialdir = '.', title = "Select file",filetypes = (("CSV files","*.CSV *.csv"),("all files","*")))
        if type(fname) is type(''):
            imp = ImportPayPal(fname)
            imp.import_all()

    def _do_help(self):
        HelpDialog(self.master)

    def _do_about(self):
        showinfo('About', 'Accounting (c) 2018-2020')

    def _do_backup(self):
        if askyesno("Backup Database?", "are you sure you want to back up the database as it is?"):
            print('back it up')

    def _do_restore(self):
        if askyesno("Restore Database?", "are you sure you want to restore the database?"):
            print('restore from backup')

    def _do_clear(self):
        if askyesno("Clear Database?", "are you sure you want to destroy the database?"):
            print('destroy it')

    def _do_open(self):
        if askyesno("Open Database?", "do you want to open a different database file? (this change will not be persistent)"):
            print('open it')



if __name__ == "__main__":
    MainFrame().main()
