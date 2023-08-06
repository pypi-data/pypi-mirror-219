import os
import apsw
import requests

connection = apsw.Connection("database.sqlite")
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
    'accountid',
]
query_fields = ','.join(select_fields)
query = f'select {query_fields} from fxaccount where sca_axcompanycdsfilter=? and sca_sluttbruker=?'

cursor.execute(query, ['FXN', 1])
rows = cursor.fetchall()
print(f'Fant {len(rows)} accounts av type FXN hvor sca_sluttbruker=1')

cursor.execute(query, ['FXN', 0])
rows = cursor.fetchall()
print(f'Fant {len(rows)} accounts av type FXN hvor sca_sluttbruker=0')

query = f'select {query_fields} from fxaccount where sca_axcompanycdsfilter=? and not sca_organisationnumber is null'
cursor.execute(query, ['FXN'])
rows = cursor.fetchall()
print(f'Fant {len(rows)} accounts av type FXN hvor org.nr ikke er null')
ikke_i_bruk = []
for row in rows:
    # print(row)
    if row[0].startswith('Ikke bruk') or row[0].startswith('Ikke i bruk'):
        ikke_i_bruk.append(row)
print(f'Fant {len(ikke_i_bruk)} accounts av type FXN hvor navn starter med "Ikke i bruk"/"Ikke bruk"')

query = f'select {query_fields} from fxaccount where sca_axcompanycdsfilter=?'
cursor.execute(query, ['FXN'])
rows = cursor.fetchall()
print(f'Fant {len(rows)} accounts av type FXN')

# query = f'select {query_fields} from fxaccount where sca_axcompanycdsfilter=?'
# cursor.execute(query, ['FXN'])
# rows = cursor.fetchall()
# for row in rows:
# print(f'Fant {len(rows)} accounts av type FXN')

def get_account_link(accountid, accountname):
    return ''.join([
        f'<a target="_blank" href="https://flexituat.crm4.dynamics.com/main.aspx',
        f'?appid=d0b97346-c58c-4779-b85f-419ecf17e43a',
        f'&forceUCI=1&pagetype=entityrecord&etn=account&id={accountid}">{accountname}</a>'])

query = f'select {query_fields} from fxaccount where sca_axcompanycdsfilter=? and not sca_organisationnumber is null'
cursor.execute(query, ['FXN'])
rows = cursor.fetchall()
with open('account_orgnr.html', 'w') as f:
    f.write('<html><body>')
    for row in rows:
        accountname, orgnr, accountid, accountpostnr = row[0], row[1], row[7], row[2]
        if not orgnr.isdigit() or len(orgnr) != 9:
            print(accountname, orgnr, accountid)
            f.write(f'<h4>{get_account_link(accountid, accountname)}</h4>')
            f.write(f'<p>')
            f.write(f'Lagret org.nr: {orgnr}')
            orgnr_fixed = orgnr.replace(' ', '')
            if orgnr_fixed.isdigit() and len(orgnr_fixed) == 9:
                f.write(f' - Skulle det vært "{orgnr_fixed}"?')
                try:            
                    brreg_response = requests.get(f'https://data.brreg.no/enhetsregisteret/api/enheter/{orgnr_fixed}')
                    brreg_data = brreg_response.json()
                except:
                    print(brreg_response)
                    print(orgnr_fixed)
                    f.write(f'</p>')
                    continue
                try:
                    f.write(f'<br>Brreg sier:')
                    if 'slettedato' in brreg_data:
                        f.write(f'<br>Slettet: {brreg_data.get("slettedato")}')
                    if brreg_data.get('navn').lower() != accountname.lower():
                        f.write(f'<br>Ulikt navn hos brreg: "{brreg_data.get("navn")}"')
                    if brreg_data["forretningsadresse"]["postnummer"] != accountpostnr:
                        f.write(f'<br>Ulikt postnr hos brreg: "{brreg_data["forretningsadresse"]["postnummer"]}"')
                        f.write(f' - Flexit sier "{accountpostnr}"')
                except:
                    f.write(f'<br>Kunne ikke hente data fra brreg!')
            else:
                f.write(f' - Klarer ikke fikse: {orgnr}')
                if len(orgnr) < 9:
                    f.write(', det er ikke nok siffer!')
                else:
                    f.write(', det er for mange siffer!')
            f.write(f'</p>')
    f.write('</body></html>')
                
    
#print(f'Fant {len(ikke_i_bruk)} accounts av type FXN hvor navn starter med "Ikke i bruk"/"Ikke bruk"')


