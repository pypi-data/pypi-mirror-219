import apsw
from dev.dev_setup import load_dev_environment
from fxpyD365api import Account
from dev.account_utils import account_fields, account_brreg_fields

load_dev_environment()

"""
https://flexituat.crm4.dynamics.com/api/data/v9.0/accounts?
$select=name,sca_axcompanycdsfilter,sca_organisationnumber,_sca_axcustomergroup_value&
$filter=_sca_axcustomergroup_value%20eq%203ec49c86-ae0c-ea11-a811-000d3a228591&$top=50
"""


class CompanyAccountNorway(Account):
    
    def get_company_account_norway_page(self, page):
        select_str = ','.join(account_fields)
        filter_str = '_sca_axcustomergroup_value eq 3ec49c86-ae0c-ea11-a811-000d3a228591'
        return self.get_page(page=page, select=select_str, request_filter=filter_str)


connection = apsw.Connection("companydb.sqlite")
cursor = connection.cursor()

table_cols = account_fields + account_brreg_fields
try:
    sql_create_table = (f'create table fxaccount({",".join(table_cols)})')
    cursor.execute(sql_create_table)
except apsw.SQLError:
    pass # table probably exists
try:
    sql_create_table = 'create table fxsalesperson(systemuserid, fullname, internalemailaddress)'
    cursor.execute(sql_create_table)
except apsw.SQLError:
    pass # table probably exists
try:
    sql_create_table = 'create table fxchain(sca_axcompanychainid, sca_name)'
    cursor.execute(sql_create_table)
except apsw.SQLError:
    pass # table probably exists


def account_already_in_db(accountid):
    cursor.execute('select * from fxaccount where accountid=?', (accountid,))
    return bool(len(cursor.fetchall()))

account_insert_format_str = ', :'.join(table_cols)
account_insert_sql = f'insert into fxaccount values(:{account_insert_format_str})'

current_page = 1
next_page_exists = True
company_account_api = CompanyAccountNorway(page_size=500)
while next_page_exists:
    account_data = company_account_api.get_company_account_norway_page(page=current_page)
    print(f'STARTING WITH PAGE {current_page}')
    for account in account_data['value']:
        accountid = account.get('accountid')
        if not account_already_in_db(accountid):
            cursor.execute(account_insert_sql, account)
            print(f'Inserted: {accountid} - {account.get("name")}')
        else:
            print(f'Already in db: {accountid} - {account.get("name")}')
    print(f'DONE WITH PAGE {current_page}')
    current_page += 1
    if not company_account_api.has_next_page:
        next_page_exists = False


