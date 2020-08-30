from forms import Form
from logger import *


#
# TODO: A customer cannot be deleted if a committed sale exists. If a customer is
#       deleted, then all uncommitted sales are also deleted.
#
#       Show total committed and uncommitted sales for customer.
#
@class_wrapper
class CustomersForm(Form):

    def __init__(self, notebook):
        super().__init__(notebook, notebook.get_tab_index('Customers'), 'Customer')

        self.add_title('Edit Customers Form')

        self.add_dynamic_label('Date', 'date_created', 1)
        self.add_spacer(1)
        self.add_entry('Name', 'name', 2, str)
        self.add_entry('Address1', 'address1', 2, str)
        self.add_entry('Address2', 'address2', 2, str)

        self.add_entry('City', 'city', 1, str)
        self.add_entry('State', 'state', 1, str)

        self.add_entry('Zip Code', 'zip', 1, str)
        self.add_combo('Country', 'country_ID', 1, 'Country', 'name')

        self.add_entry('Email', 'email_address', 1, str)
        self.add_combo('Email Status', 'email_status_ID', 1, 'EmailStatus', 'name')

        self.add_entry('Phone', 'phone_number', 1, str)
        self.add_combo('Phone Status', 'phone_status_ID', 1, 'PhoneStatus', 'name')

        self.add_entry('Web Site', 'web_site', 1, str)
        self.add_combo('Class', 'class_ID', 1, 'ContactClass', 'name')

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

#
# TODO: A vendor cannot be deleted if a committed purchase exists. If a vendor is
#       deleted, then all uncommitted purchases are also deleted.
#
#       Associate a vendor with an account. When a purchase is made, then that
#       account is debit when the purchase is committed.
#
#       Show total committed and uncommitted purchases for vendor
#
@class_wrapper
class VendorsForm(Form):

    def __init__(self, notebook):
        super().__init__(notebook, notebook.get_tab_index('Vendors'), 'Vendor')

        self.add_title('Edit Vendors Form')

        self.add_dynamic_label('Date', 'date_created', 1)
        self.add_spacer(1)
        self.add_entry('Name', 'name', 2, str)
        self.add_entry('Contact', 'contact_name', 2, str)
        self.add_entry('Description', 'description', 2, str)

        self.add_entry('Email', 'email_address', 1, str)
        self.add_combo('Email Status', 'email_status_ID', 1, 'EmailStatus', 'name')

        self.add_entry('Phone', 'phone_number', 1, str)
        self.add_combo('Phone Status', 'phone_status_ID', 1, 'PhoneStatus', 'name')

        self.add_entry('Web Site', 'web_site', 1, str)
        self.add_combo('Class', 'type_ID', 1, 'ContactClass', 'name')

        self.add_std_button('Prev')
        self.add_std_button('Next')
        self.add_button_spacer()
        self.add_std_button('Select', 'name')
        self.add_std_button('Clear')
        self.add_std_button('Save')
        self.add_std_button('Delete')
        self.add_button_spacer()
        self.add_edit_button('Edit Notes', 'notes', 'Notes')

#
# TODO: Modify these forms so that a new sale can be entered and committed sales
#       cannot be modified. (sales and products)
#
#       Need to select sales based on customer name and pull up all sales associated
#       a customer for selections.
#
#       Find a way to prevent duplicate sales from being imported.
#
#       Make product widget simpler. This form only displays the products. Products
#       for this sale are edited in a different dialog that is activated by a button.
#       If the sale is committed, then the button is disabled.
#
#       Sales and purchases need to show if they have been committed. When the commit
#       button is pressed, then the accounts are debited.
#
@class_wrapper
class sSalesForm(Form):

    def __init__(self, notebook):
        super().__init__(notebook, notebook.get_tab_index('Sales'), 'SaleRecord')

        self.add_title('Sales Setup Form')
        self.add_indirect_label('Customer', 'customer_ID', 1, 'Customer', 'name')
        self.add_spacer(1)
        self.add_dynamic_label('Gross', 'gross', 1)
        self.add_spacer(1)
        self.add_dynamic_label('Fees', 'fees', 1)
        self.add_spacer(1)
        self.add_dynamic_label('Shipping', 'shipping', 1)
        self.add_spacer(1)
        self.add_combo('Status', 'status_ID', 1, 'SaleStatus', 'name')
        self.add_spacer(1)
        #self.add_products_widget()

        self.add_std_button('Prev')
        self.add_std_button('Next')
        self.add_button_spacer()
        self.add_std_button('Save')
        self.add_std_button('Delete')
        #self.add_commit_btn()
        self.add_button_spacer()
        self.add_edit_button('Edit Notes', 'notes', 'Notes')

@class_wrapper
class sPurchaseForm(Form):

    def __init__(self, notebook):
        super().__init__(notebook, notebook.get_tab_index('Purchases'), 'PurchaseRecord')

        self.add_title('Purchase Setup Form')
        self.add_indirect_label('Vendor', 'vendor_ID', 1, 'Vendor', 'name')
        self.add_spacer(1)
        self.add_dynamic_label('Gross', 'gross', 1)
        self.add_spacer(1)
        self.add_dynamic_label('Tax', 'tax', 1)
        self.add_spacer(1)
        self.add_dynamic_label('Shipping', 'shipping', 1)
        self.add_spacer(1)
        self.add_combo('Purchase Type', 'type_ID', 1, 'PurchaseType', 'name')
        self.add_spacer(1)
        self.add_combo('Purchase Status', 'status_ID', 1, 'PurchaseStatus', 'name')
        self.add_spacer(1)

        self.add_std_button('Prev')
        self.add_std_button('Next')
        self.add_button_spacer()
        self.add_std_button('Save')
        self.add_std_button('Delete')
        #self.add_commit_btn()
        self.add_button_spacer()
        self.add_edit_button('Edit Notes', 'notes', 'Notes')
