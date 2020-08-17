import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror, askyesno
from database import Database


# see: https://effbot.org/tkinterbook/tkinter-dialog-windows.htm
class BaseDialog(tk.Toplevel):
    '''
    This class provides common services to simple data dialogs.
    '''

    def __init__(self, parent):

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        self.parent = parent

        self.result = None
        # get a copy of the data_store for the children

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        try:
            body.grid(padx=5, pady=5)

            self.buttonbox()

            self.grab_set()

            if not self.initial_focus:
                self.initial_focus = self

            self.protocol("WM_DELETE_WINDOW", self.cancel)

            self.initial_focus.focus_set()
            self.wait_window(self)
        except Exception:
            pass    # probably no records are available

    #
    # construction hooks
    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        return self

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        box.grid()

    #
    # standard button semantics
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks
    def validate(self):
        return True # override

    def apply(self):
        pass # override


class SelectItem(BaseDialog):
    '''
    Create a list of items called 'name' from a table and return the database
    ID of the item in item_id.
    '''

    def __init__(self, master, table, column, thing=None):

        self.table = table
        self.column = column
        if thing is None:
            self.thing = 'Item'
        else:
            self.thing = thing

        self.item_id = -1
        super().__init__(master)
        #self.wait_window(self)

    def body(self, master):
        self.title("Select %s"%(self.thing))
        self.data = Database.get_instance()

        padx = 6
        pady = 2

        frame = tk.Frame(master, bd=1, relief=tk.RIDGE)
        frame.grid(row=0, column=0, padx=4, pady=7)
        tk.Label(frame, text="Select %s"%(self.thing), font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2)

        ######################
        # Populate the combo boxes
        lst = self.data.populate_list(self.table, self.column)
        lst.sort()

        ######################
        # Show the boxes
        tk.Label(frame, text='Name:').grid(row=1, column=0)
        self.cbb = ttk.Combobox(frame, values=lst)
        self.cbb.grid(row=1, column=1, padx=padx, pady=pady)
        try:
            self.cbb.current(0)
        except tk.TclError:
            showerror("ERROR", "No records are available to select for this table.")
            self.cancel()

    def apply(self):
        ''' Populate the form with the selected data. '''
        id = self.data.get_id_by_name(self.table, self.column, self.cbb.get())
        self.item_id = id

class EditDialog(BaseDialog):

    def __init__(self, master, table, column, row_id, thing=None):

        self.row_id = row_id
        self.table = table
        self.column = column
        if thing is None:
            self.thing = 'Item'
        else:
            self.thing = thing

        super().__init__(master)
        #self.wait_window(self)

    def body(self, master):
        self.title("Edit %s"%(self.thing))
        self.data = Database.get_instance()

        padx = 6
        pady = 2

        frame = tk.Frame(master, bd=1, relief=tk.RIDGE)
        frame.grid(row=0, column=0, padx=4, pady=7)
        tk.Label(frame, text="Edit %s"%(self.thing), font=("Helvetica", 14)).grid(row=0, column=0)#, columnspan=2)

        # create the editor window
        self.widget = tk.Text(frame, wrap=tk.NONE, height=20, width=60)
        self.widget.insert(tk.END, '')
        self.widget.grid(row=1, column=0, sticky='nw')

        # see https://www.homeandlearn.uk/tkinter-scrollbars.html
        self.vsb = tk.Scrollbar(frame, orient=tk.VERTICAL)
        self.vsb.config(command=self.widget.yview)
        self.widget.config(yscrollcommand=self.vsb.set)
        self.vsb.grid(row=0, column=1, sticky='nse')

        self.hsb = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        self.hsb.config(command=self.widget.xview)
        self.widget.config(xscrollcommand=self.hsb.set)
        self.hsb.grid(row=1, column=0, sticky='wes')

        frame.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        value = self.data.get_single_value(self.table, self.column, self.row_id)
        self.widget.delete('1.0', tk.END)
        if not value is None:
            self.widget.insert(tk.END, str(value))

    def apply(self):
        '''
        Save the text to the database as a single item.
        '''
        if askyesno("Confirm", "are you sure you want to save this %s?"%(self.thing)):
            value = self.widget.get(1.0, tk.END)
            self.data.set_single_value(self.table, self.column, self.row_id, value)
            self.data.commit()


###############################################################################
# Does not use BaseDialog
class HelpDialog:

    help_text = """
    Shop Timer
    Chuck Tilbury (c) 2019

    This software is open source under the MIT and BSD licenses.

    -------------------------------------------
    General use.
    -------------------------------------------

    -------------------------------------------
    Saving a file
    -------------------------------------------

    -------------------------------------------
    Loading a file
    -------------------------------------------

    -------------------------------------------
    Reset to default settings
    -------------------------------------------

    """

    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.tx = tk.Text(self.top, height=25, width=80)
        self.sb = tk.Scrollbar(self.top)
        self.sb.pack(side=tk.RIGHT,fill=tk.Y)
        self.tx.pack(side=tk.LEFT)
        self.sb.config(command=self.tx.yview)
        self.tx.config(yscrollcommand=self.sb.set)
        self.tx.insert(tk.END, self.help_text)
        self.tx.config(state='disabled')

