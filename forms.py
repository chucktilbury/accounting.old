
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror, showinfo, askyesno
from database import Database
from form_widgets import *
from form_dialog import *
from dialogs import *
from logger import *

#
# TODO: Add a validation such that required fields are not blank, numbers are numbers, etc.
#

@class_wrapper
class Form(tk.Frame):
    '''
    Create a form widget that has all of the controls and infrastructure to
    control it. All of these forms are imbedded in a notebook tab.
    '''

    #def __init__(self, notebook, index, table, scrolling=False, **kw):
    def __init__(self, owner, table, scrolling=False, **kw):
        '''
        Create a form and provide infrastructiore to add and service different kinds of
        widgets in the form.

        notebook    =   The notebook that owns this form.
        index       =   The index of the notebook tab that owns this form.
        table       =   Database table where most of the items in the form can be found.
        *kw         =   Named arguments passed to the frame of the form.
        '''
        #super().__init__(notebook.get_frame(index))#, **kw)
        #notebook.frame_list[index]['show_cb'] = self.load_form
        super().__init__(owner)

        self.scrolling = scrolling

        # create the button frame and place it
        self.btn_frame = tk.Frame(self)
        self.btn_frame.grid(row=0, column=0, sticky='se')

        # create the widget frame and place it
        if self.scrolling:
            cframe = tk.LabelFrame(self)#, width=kw['width'], height=kw['height'])
            cframe.grid(row=0, column=1, sticky='nw')
            self.canvas = tk.Canvas(cframe, **kw)
            self.canvas.grid(row=0, column=0)

            vscollbar = tk.Scrollbar(cframe, orient='vertical', command=self.canvas.yview)
            vscollbar.grid(row=0, column=1, sticky='nsw')

            self.canvas.configure(yscrollcommand=vscollbar.set)
            self.canvas.configure(yscrollincrement='20')

            self.ctl_frame = tk.LabelFrame(self.canvas)

            self.canvas.create_window((0,0), window=self.ctl_frame, anchor='nw')
            self.canvas.focus_set()
        else:
            self.ctl_frame = tk.LabelFrame(self)
            self.ctl_frame.grid(row=0, column=1, sticky='nw')

        # get the database interface
        self.data = Database.get_instance()
        self.table = table
        self.edit_class = None

        # Layout management.
        self.row = 0    # current row to place a widget into
        self.col = 0    # current column to place a widget into
        # This is the width of the actual control, not the control + label.
        self.column_width = 35
        # This is a stupid fudge factor placed in an attribute so it can be changed
        # from the outside of the class. If the columns don't line up then alter this
        # variable until the do.
        self.column_fudge = 9

        # These parameters can be set for each form.
        # self.padx = 5   # widget pad
        # self.pady = 5   # widget pad
        self.columns = 2    # number of columns to reserve for this form
        self.btn_row = 0    # current row to place a button into
        self.btn_padx = 5   # button pad
        self.btn_pady = 5   # button pad
        self.btn_width = 10 # size of a button
        self.text_height = 20   # height of a text entry control

        # row list management
        if not table is None:
            self.row_list = self.data.get_id_list(self.table)
            self.row_index = 0
        else:
            self.row_list = None
            self.row_index = 0

        # controls management
        self.ctl_list = []
        self.grid()

    @func_wrapper
    def add_title(self, text):
        '''
        Add a static label to the form.

        text = Text of the label.
        '''
        ctrl = FormTitle(self.ctl_frame, text)
        ctrl.grid(row=self.row, column=self.col, columnspan=self.columns)
        self.row += 1
        self.ctl_list.append(ctrl)

    @func_wrapper
    def add_entry(self, label, column, cols, _type, **kw):
        '''
        Add an entry control to the form. The value from this control is cast
        to the _type when it is written to the database.

        label   =   Label for the control.
        column  =   Column to get the data from.
        cols    =   Number of form columns that this control will span.
        _type   =   Type of the data in the database.
        **kw    =   Named args passed to the control.
        '''
        ctrl = FormEntry(self.ctl_frame, label, self.table, column, _type, width=self._get_width(cols), **kw)
        self._grid(ctrl, cols)
        self.ctl_list.append(ctrl)

    @func_wrapper
    def add_combo(self, label, column, cols, pop_tab, pop_col, **kw):
        '''
        Add a combo box entry to the form. The values for the combo box are located
        in a table other than the one indicated in this object. The table/column in
        this object has the ID from the remote table.

        label   =   Label for the control.
        column  =   Column to get the data from.
        cols    =   Number of form columns that this control will span.
        pop_tab =   Database table where the values for the combo box are located.
        pop_col =   Database column where the values for the combo box are located.
        **kw    =   Named args passed to the control.
        '''
        ctrl = FormCombo(self.ctl_frame, label, pop_tab, pop_col, self.table, column, width=self._get_width(cols), **kw)
        self._grid(ctrl, cols)
        self.ctl_list.append(ctrl)


    @func_wrapper
    def add_text(self, label, column, cols, **kw):
        '''
        Add a multi-line text control to the form.

        label   =   Label for the control.
        column  =   Column to get the data from.
        cols    =   Number of form columns that this control will span.
        **kw    =   Named args passed to the control.
        '''
        ctrl = FormText(self.ctl_frame, label, self.table, column, width=self._get_width(cols), **kw)
        self._grid(ctrl, cols)
        self.ctl_list.append(ctrl)

    @func_wrapper
    def add_indirect_label(self, label, column, cols, pop_tab, pop_col, **kw):
        '''
        Add a dynamic label to the form. The database column for this control contains
        a numeric ID that points to a row in another table.

        label   =   Label for the control.
        column  =   Column to get the data from.
        cols    =   Number of form columns that this control will span.
        pop_tab =   Database table where the display value is located.
        pop_col =   Database column where the display value is located.
        **kw    =   Named args passed to the control
        '''
        ctrl = FormIndirectLabel(self.ctl_frame, label, pop_tab, pop_col, self.table, column, width=self._get_width(cols), **kw)
        self._grid(ctrl, cols)
        self.ctl_list.append(ctrl)

    @func_wrapper
    def add_dynamic_label(self, label, column, cols, **kw):
        '''
        Add a label where the form table has the actual data to display.

        label   =   Label for the control.
        column  =   Column to get the data from.
        cols    =   Number of form columns that this control will span.
        **kw    =   Named args passed to the control
        '''
        ctrl = FormDynamicLabel(self.ctl_frame, label, self.table, column, width=self._get_width(cols), **kw)
        self._grid(ctrl, cols)
        self.ctl_list.append(ctrl)

    @func_wrapper
    def add_spacer(self, cols):
        '''
        This adds an invisible spacer into the control frame.
        '''
        frame = tk.Frame(self.ctl_frame)
        self._grid(frame, cols)

    @func_wrapper
    def add_std_button(self, name, column=None, command=None, **kw):
        '''
        Add a button control to the button panel of the form.

        name    =   Text that appears on the button
        command =   Optional button callback. "Standard" buttons use the default callbacks.
        **kw    =   Named args passed to the control
        '''

        if command is None:
            if name == "Next":
                command = self._next_button
            elif name == "Prev":
                command = self._prev_button
            elif name == "Clear":
                command = self._new_button
            elif name == "Save":
                command = self._save_button
            elif name == "Delete":
                command = self._delete_button
            elif name == "Edit":
                command = lambda x=self.row_list[self.row_index]: self._edit_button(x)
            elif name == "Select":
                if column is None:
                    raise Exception("Select button requires a column to be specified.")
                command = lambda c=column: self._select_button(c)
            else:
                raise Exception("Cannot add button. Unknown name and no command to exec.")

        ctrl = tk.Button(self.btn_frame, text=name, command=command, width=self.btn_width, **kw)
        ctrl.grid(row=self.btn_row, column=0, sticky='nw')
        self.btn_row += 1

    @func_wrapper
    def set_edit_class(self, cls):
        '''
        Set the class to create when the edit button is pressed. This must be called when there
        is an "Edit" button created.
        '''
        self.edit_class = cls

    @func_wrapper
    def add_edit_button(self, name, column, thing, **kw):
        '''
        This button spawns a text dialog for editing text information.

        name    =   Text for the button
        column  =   Column in the database where the data is located.
        **kw    =   Args passed to the button constructor
        '''
        if len(self.row_list) == 0:
            index = 0
        else:
            index = self.row_list[self.row_index]

        ctrl = tk.Button(self.btn_frame, text=name,
                        command=lambda t=self.table,
                                        c=column,
                                        r=index,
                                        l=thing: self._edit_btn_command(t, c, r, l),
                        width=self.btn_width, **kw)
        ctrl.grid(row=self.btn_row, column=0, sticky='nw')
        self.btn_row += 1

    @func_wrapper
    def add_button_spacer(self):
        '''
        This adds an invisible spacer into the button frame.
        '''
        frame = tk.Frame(self.btn_frame)
        frame.grid(row=self.btn_row, column=0, sticky='nw', pady=5)
        self.btn_row += 1

    @func_wrapper
    def load_form(self):
        '''
        Load the form from the database.
        '''
        if len(self.row_list) == 0:
            showinfo('Records', 'There are no records for this form to display.')
            return

        for item in self.ctl_list:
            item.set_row_id(self.row_list[self.row_index])
            item.setter()

        if self.scrolling:
            geom = self._get_geometry(self.ctl_frame)
            self.canvas.configure(scrollregion=(0, 0, geom['width'], geom['height']))

    @func_wrapper
    def save_form(self):
        '''
        Save the form to the database.
        TODO: Handle "new" forms.
        '''
        for item in self.ctl_list:
            item.set_row_id(self.row_list[self.row_index])
            item.getter()

        self.data.commit()

    @func_wrapper
    def _get_geometry(self, wid):
        '''
        Get the size and location of a widget.
        '''
        wid.update()
        return {'width':wid.winfo_width(), 'height':wid.winfo_height(),
                'hoffset':wid.winfo_x(), 'voffset':wid.winfo_y(),
                'name':wid.winfo_name()}

    @func_wrapper
    def _get_width(self, cols):
        '''
        Calculate the actual width of the actual control, minus any padding and
        the label.
        '''
        actual = self.column_width * cols
        if cols < self.columns:
            actual -= self.column_fudge     # This is a stupid fudge factor.
        return actual

    @func_wrapper
    def _grid(self, ctrl, cols):
        '''
        Insert the control into the form grid according to the number of columns it
        will absorb.
        '''
        if cols == self.columns:
            ctrl.grid(row=self.row, column=self.col, columnspan=self.columns)
            self.row += 1
            self.col = 0
        else:
            if self.col >= self.columns-1:
                ctrl.grid(row=self.row, column=self.col, columnspan=cols)
                self.col = 0
                self.row += 1
            else:
                ctrl.grid(row=self.row, column=self.col, columnspan=cols)
                self.col += 1

    @func_wrapper
    def _edit_btn_command(self, table, column, row_id, thing):
        '''
        Display the dialog, then fill in the data from the database. React to
        the "save" or "cancel" buttons.
        '''
        EditDialog(self, table, column, row_id, thing)

    @func_wrapper
    def _next_button(self):
        if not self.row_list is None:
            self.row_index += 1
            if self.row_index > len(self.row_list)-1:
                self.row_index = len(self.row_list)-1
                showinfo('Last Record', 'This is the last record.')
            else:
                self.load_form()

    @func_wrapper
    def _prev_button(self):
        if not self.row_list is None:
            self.row_index -= 1
            if self.row_index < 0:
                self.row_index = 0
                showinfo('First Record', 'This is the first record.')
            else:
                self.load_form()

    @func_wrapper
    def _select_button(self, column):
        if not self.row_list is None:
            item = SelectItem(self, self.table, column)
            if item.item_id > 0:
                self.row_index = self.row_list.index(item.item_id)
                self.load_form()

    @func_wrapper
    def _new_button(self):
        for item in self.ctl_list:
            item.clear()

    @func_wrapper
    def _save_button(self):
        if askyesno('Save record?', 'Are you sure you want to save this?'):
            self.save_form()

    @func_wrapper
    def _delete_button(self):
        if askyesno('Delete record?', 'Are you sure you want to delete this?'):
            self.data.delete_row(self.table, self.row_list[self.row_index])
            self.data.commit()

            self.row_list = self.data.get_id_list(self.table)
            if self.row_index > len(self.row_list):
                self.row_index -= 1
            self.load_form()

    @func_wrapper
    def _edit_button(self, row_id):
        if self.edit_class is None:
            showerror("Error", "There is no edit class set for the edit button")
        else:
            self.edit_class(self, row_id, self.table)

@class_wrapper
class NotebookForm(Form):

    def __init__(self, notebook, index, table, scrolling=False, **kw):

        super().__init__(notebook.get_frame(index), table, scrolling, **kw)
        notebook.frame_list[index]['show_cb'] = self.load_form

@class_wrapper
class DialogForm(Form):

    def __init__(self, owner, row_id, table, scrolling=False, **kw):

        super().__init__(owner, table, scrolling, **kw)
        self.form_dialog = FormDialog(owner)
        self.form_dialog.load_form = self.load_form
        self.form_dialog.save_form = self.save_form
        self.row_id = row_id
