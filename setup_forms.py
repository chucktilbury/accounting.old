from forms import Form
from logger import *

@class_wrapper
class BusinessForm(Form):
    '''
    Create the form for the Business tab under Setup.
    '''

    def __init__(self, notebook):
        super().__init__(notebook, notebook.get_tab_index('Business'), 'Business')

        self.add_title('Business Setup Form')
        self.add_entry('Name', 'name', 2, str)
        self.add_entry('Address1', 'address1', 2, str)
        self.add_entry('Address2', 'address2', 2, str)

        self.add_entry('City', 'city', 1, str)
        self.add_entry('State', 'state', 1, str)

        self.add_entry('Zip Code', 'zip', 1, str)
        self.add_entry('Country', 'country', 1, str)

        self.add_entry('Email', 'email_address', 1, str)
        self.add_entry('Phone', 'phone_number', 1, str)

        self.add_entry('Web Site', 'web_site', 2, str)
        self.add_entry('Description', 'description', 2, str)

        self.add_std_button('Save')
        self.add_button_spacer()
        self.add_edit_button('Edit Terms', 'terms', 'Terms')
        self.add_edit_button('Edit Returns', 'returns', 'Returns')
        self.add_edit_button('Edit Warranty', 'warranty', 'Warranty')

@class_wrapper
class AccountsForm(Form):

    def __init__(self, notebook):
        super().__init__(notebook, notebook.get_tab_index('Accounts'), 'Account')

        self.add_title('Accounts Setup Form')
        self.add_entry('Name', 'name', 1, str)
        self.add_entry('Number', 'number', 1, str)
        self.add_combo('Type', 'type_ID', 1, 'AccountTypes', 'name')
        self.add_entry('Total', 'total', 1, float)
        self.add_entry('Description', 'description', 2, str)

        self.add_std_button('Prev')
        self.add_std_button('Next')
        self.add_button_spacer()
        self.add_std_button('Select', 'name')
        self.add_std_button('Clear')
        self.add_std_button('Save')
        self.add_std_button('Delete')
        self.add_button_spacer()
        self.add_edit_button('Edit Notes', 'notes', 'Notes')

@class_wrapper
class InventoryForm(Form):

    def __init__(self, notebook):
        super().__init__(notebook, notebook.get_tab_index('Inventory'), 'InventoryItem')

        self.add_title('Inventory Setup Form')
        self.add_entry('Name', 'name', 2, str)
        self.add_entry('Stock Num', 'stock_num', 1, int)
        self.add_entry('Stock', 'num_stock', 1, int)
        self.add_entry('Retail', 'retail', 1, float)
        self.add_entry('Wholesale', 'wholesale', 1, float)
        self.add_entry('Description', 'description', 2, str)

        self.add_std_button('Prev')
        self.add_std_button('Next')
        self.add_button_spacer()
        self.add_std_button('Select', 'name')
        self.add_std_button('Clear')
        self.add_std_button('Save')
        self.add_std_button('Delete')
        self.add_button_spacer()
        self.add_edit_button('Edit Notes', 'notes', 'Notes')

