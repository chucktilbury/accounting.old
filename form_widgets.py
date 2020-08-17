import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror, showinfo, askyesno
from database import Database

class FormWidgetBase(tk.Frame):
    '''
    Common methods and data for form widgets.
    '''
    ctrl_width = 60
    label_width = 15
    padx = 0
    pady = 5

    def __init__(self, owner, **kw):
        super().__init__(owner, **kw)

        self.data = Database.get_instance()

        #self.padx = 5
        #self.pady = 5
        #self.label_width = 10
        #self.ctrl_width = 60
        self.text_height = 20
        # these are created for the widget.
        self.widget = None
        self.label = None
        self.row_id = -1

    def set_row_id(self, id):
        '''
        Set the current row ID so that the value can be seen in the database.
        '''
        self.row_id = id

    def getter(self):
        '''
        Read the value of the widget and save it to the database.
        '''
        pass

    def setter(self):
        '''
        Read the value from the database and place it into the widget.
        '''
        self.clear()
        pass

    def clear(self):
        '''
        Clear the value of the widget or reset it to the default value.
        '''
        pass

    def populate(self):
        '''
        This method populates widgets that have an ID as their data.
        '''
        pass


class FormTitle(FormWidgetBase):

    def __init__(self, owner, label, **kw):
        '''
        The title is a static object that does not have a corresponding table entry.

        owner = The frame to place the title into.
        label = Text of the title.
        **kw  = Passed to the widget.
        '''
        super().__init__(owner)

        self.label = label
        self.widget = tk.Label(self, text=self.label, font=("Helvetica", 14), **kw)
        self.widget.grid()

class FormEntry(FormWidgetBase):

    def __init__(self, owner, label, table, column, _type, **kw):
        '''
        An entry is a single line entry.

        owner  = The frame to place the title into.
        label  = The label to place in the widget.
        table  = The database table where the data exists.
        column = The database column where the data exists.
        _type  = Type of data in the database.
        *kw    = Passed to the Entry widget.
        '''
        super().__init__(owner)

        self._type = _type
        self.table = table
        self.column = column

        if not 'width' in kw:
            kw['width'] = self.ctrl_width

        self.label = tk.Label(self, text=label+':', width=self.label_width)
        self.label.grid(row=0, column=0, sticky='e', padx=self.padx, pady=self.pady)
        self.strvar = tk.StringVar(self)
        self.widget = tk.Entry(self, textvariable=self.strvar, **kw)
        self.widget.grid(row=0, column=1, sticky='w', padx=self.padx, pady=self.pady)

    def getter(self):
        value = self._type(self.strvar.get())
        self.data.set_single_value(self.table, self.column, self.row_id, value)

    def setter(self):
        state = self.widget.configure()['state']
        if state == 'readonly':
            self.widget.configure(state='normal')

        value = self.data.get_single_value(self.table, self.column, self.row_id)
        self.strvar.set(str(value))

        if state == 'readonly':
            self.widget.configure(state='readonly')

    def clear(self):
        '''
        Clear the value of the widget.
        '''
        state = self.widget.configure()['state']
        if state == 'readonly':
            self.widget.configure(state='normal')

        self.strvar.set('')

        if state == 'readonly':
            self.widget.configure(state='readonly')

class FormText(FormWidgetBase):

    def __init__(self, owner, label, table, column, **kw):
        '''
        A text widget is a multi-line entry that has scrollbars.

        owner  = The frame to place the title into.
        label  = The label to place in the widget.
        table  = The database table where the data exists.
        column = The database column where the data exists.
        **kw   = Passed to the Text widget.
        '''
        super().__init__(owner)

        self.table = table
        self.column = column
        self.label = tk.Label(self, text=label+':', width=self.label_width)

        if not 'width' in kw:
            kw['width'] = self.ctrl_width

        if not 'height' in kw:
            kw['height'] = self.text_height

        self.local_frame = tk.Frame(self, bd=1, relief=tk.RIDGE)
        self.widget = tk.Text(self.local_frame, wrap=tk.NONE, **kw)
        self.widget.insert(tk.END, '')
        self.widget.grid(row=0, column=0, sticky='nw')

        # see https://www.homeandlearn.uk/tkinter-scrollbars.html
        self.vsb = tk.Scrollbar(self.local_frame, orient=tk.VERTICAL)
        self.vsb.config(command=self.widget.yview)
        self.widget.config(yscrollcommand=self.vsb.set)
        self.vsb.grid(row=0, column=1, sticky='nse')

        self.hsb = tk.Scrollbar(self.local_frame, orient=tk.HORIZONTAL)
        self.hsb.config(command=self.widget.xview)
        self.widget.config(xscrollcommand=self.hsb.set)
        self.hsb.grid(row=1, column=0, sticky='wes')

        self.local_frame.grid(row=0, column=1, padx=self.padx, pady=self.pady, sticky='w')
        self.label.grid(row=0, column=0, padx=self.padx, pady=self.pady, sticky='e')

    def getter(self):
        value = self.widget.get(1.0, tk.END)
        self.data.set_single_value(self.table, self.column, self.row_id, value)

    def setter(self):
        value = self.data.get_single_value(self.table, self.column, self.row_id)
        self.widget.delete('1.0', tk.END)
        if not value is None:
            self.widget.insert(tk.END, str(value))

    def clear(self):
        self.widget.delete('1.0', tk.END)


class FormCombo(FormWidgetBase):
    '''
    A combo box is populated from another table and the form table has the ID of the current
    item indicated. The ID is what gets handled by the getter and setter.
    '''

    def __init__(self, owner, label, pop_table, pop_column, table, column, **kw):
        '''
        The name is displayed as the label and is also used to access the control
        when reading it or writing to it. Combo boxes use a different table to
        store their data in. This widgit automatically retrieves that data when
        it is displayed.

        owner      = The frame to place the title into.
        label      = The label to place in the widget.
        pop_table  = Table where the display data exists.
        pop_column = Column where the display data exists.
        table      = The database table where the data exists.
        column     = The database column where the data exists.
        **kw       = Passed to the Text widget.
        '''
        super().__init__(owner)

        self.pop_table = pop_table
        self.pop_column = pop_column
        self.table = table
        self.column = column

        self.label = tk.Label(self, text=label+':', width=self.label_width)
        self.label.grid(row=0, column=0)

        if not 'width' in kw:
            kw['width'] = self.ctrl_width

        self.widget = ttk.Combobox(self, state='readonly', **kw)
        self.widget.grid(row=0, column=1)
        self.populate()

    def getter(self):
        if self.row_id != -1:
            value = self.widget.current()+1
            self.data.set_single_value(self.table, self.column, self.row_id, value)

    def setter(self):
        if self.row_id != -1:
            value = self.data.get_single_value(self.table, self.column, self.row_id)
            self.widget.current(int(value)-1)
        self.populate()

    def clear(self):
        try:
            self.widget.current(0)
        except tk.TclError:
            pass # empty content is not an error

    def populate(self):
        self.widget['values'] = self.data.populate_list(self.pop_table, self.pop_column)

class FormDynamicLabel(FormWidgetBase):
    '''
    A dynamic label is one where the table has the actual data to be displayed.
    '''

    def __init__(self, owner, label, table, column, **kw):
        '''
        This widget only has a setter. The other overrides are irrelevant.

        owner      = The frame to place the title into.
        label      = The label to place in the widget.
        table      = The database table where the data exists.
        column     = The database column where the data exists.
        **kw       = Passed to the Text widget.
        '''
        super().__init__(owner)

        self.table = table
        self.column = column

        self.label = tk.Label(self, text=label+':', width=self.label_width)
        self.label.grid(row=0, column=0, sticky='e')

        if not 'width' in kw:
            kw['width'] = self.ctrl_width

        self.value = tk.StringVar(self)
        self.widget = tk.Label(self, textvariable=self.value, **kw)
        self.widget.grid(row=0, column=1, sticky='w')

    def setter(self):
        value = self.data.get_single_value(self.table, self.column, self.row_id)
        self.value.set(str(value))

class FormIndirectLabel(FormWidgetBase):
    '''
    An indirect label has an ID for the contents. The actual display content comes
    from another table and it pointed to by the ID.
    '''

    def __init__(self, owner, label, pop_table, pop_column, table, column, **kw):
        '''
        The table contains an ID where the actual display data is located.

        owner      = The frame to place the title into.
        label      = The label to place in the widget.
        pop_table  = Table where the display data exists.
        pop_column = Column where the display data exists.
        table      = The database table where the data exists.
        column     = The database column where the data exists.
        **kw       = Passed to the Text widget.
        '''
        super().__init__(owner)

        self.pop_table = pop_table
        self.pop_column = pop_column
        self.table = table
        self.column = column

        self.label = tk.Label(self, text=label+':', width=self.label_width)
        self.label.grid(row=0, column=0)

        if not 'width' in kw:
            kw['width'] = self.ctrl_width

        self.value = tk.StringVar(self)
        self.widget = tk.Label(self, textvariable=self.value, **kw)
        self.widget.grid(row=0, column=1)

    def getter(self):
        # This is the name
        value = self.value.get()
        # find the row ID where the name matches in the pop_table
        id = self.data.get_id_by_row(self.pop_table, self.pop_column, value)
        # set the value with the row_id
        self.data.set_single_value(self.table, self.column, self.row_id, id)

    def setter(self):
        # this is the ID
        id = self.data.get_single_value(self.table, self.column, self.row_id)
        # find the value with the row ID in the table
        value = self.data.get_single_value(self.pop_table, self.pop_column, id)
        # set the widget value
        self.value.set(str(value))

    def clear(self):
        self.value.set('')

