import os
import apsw
import requests

connection = apsw.Connection("companydb.sqlite")
cursor = connection.cursor()

sql_create_table_brreg_cols = [    
    'brreg_orgnr',
    'brreg_name',
    'brreg_konkurs',
    'brreg_underAvvikling',
    'brreg_underTvangsavviklingEllerTvangsopplosning',
    'brreg_postnummer',
    'brreg_poststed',
    'brreg_adresse',
]

select_fields = [
    'name',
    'sca_organisationnumber',
    'address1_postalcode',
    'address1_city',
    '_parentaccountid_value',
    'sca_sluttbruker',
    'sca_axcompanycdsfilter',
    '_sca_axcustomergroup_value',
    'accountid',
]
query_fields = ','.join(select_fields)
query = f'select {query_fields} from fxaccount where sca_axcompanycdsfilter=?'

cursor.execute(query, ['FXN'])
rows = cursor.fetchall()
fxn_not_set = 0
for row in rows:
    sca_axcompanycdsfilter = row[6]
    print(sca_axcompanycdsfilter)
    if not sca_axcompanycdsfilter == 'FXN':
        fxn_not_set += 1
print(f'Fant {fxn_not_set} accounts hvor _sca_axcustomergroup_value=NBE men sca_axcompanycdsfilter er ikke FXN')

