import os
import sys
import apsw
import requests
from dev.dev_setup import load_dev_environment
from fxpyD365api import GenericWrapper

load_dev_environment()

connection = apsw.Connection("companydb.sqlite")
cursor = connection.cursor()

query_fields = ','.join([
    'name',
    'sca_organisationnumber',
    'emailaddress1',
    'address1_postalcode',
    'address1_city',
    '_parentaccountid_value',
    'sca_sluttbruker',
    'sca_axcompanycdsfilter',
    'accountid',
    'statuscode',
    '_sca_salesperson_value',
    '_sca_axcompanychainid_value',
])

systemuser_api = GenericWrapper('systemusers')

def get_salesperson(salespersonid):
    cursor.execute('select internalemailaddress from fxsalesperson where systemuserid=?', (salespersonid,))
    if len(cursor.fetchall()) == 0:
        try:
            userdata = systemuser_api.retrieve(salespersonid).json()
            user = {
                'systemuserid': salespersonid,
                'fullname': userdata['fullname'],
                'internalemailaddress': userdata['internalemailaddress'],
            }
            insert_sql = 'insert into fxsalesperson values(:systemuserid, :fullname, :internalemailaddress)'
            cursor.execute(insert_sql, user)
            return userdata['internalemailaddress']
        except:
            print(f'Could not insert or retrieve user {salespersonid}')
            return None
    cursor.execute('select internalemailaddress from fxsalesperson where systemuserid=?', (salespersonid,))
    rows = cursor.fetchall()
    return rows[0][0]

chain_api = GenericWrapper('sca_axcompanychains')

def get_chain(chainid):
    cursor.execute('select sca_name from fxchain where sca_axcompanychainid=?', (chainid,))
    if len(cursor.fetchall()) == 0:
        chaindata = chain_api.retrieve(chainid).json()
        data = {
            'sca_axcompanychainid': chainid,
            'sca_name': chaindata['sca_name'],
        }
        insert_sql = 'insert into fxchain values(:sca_axcompanychainid, :sca_name)'
        cursor.execute(insert_sql, data)
        return data['sca_name']
    cursor.execute('select sca_name from fxchain where sca_axcompanychainid=?', (chainid,))
    rows = cursor.fetchall()
    return rows[0][0]

def get_account_link(accountid, accountname):
    return ''.join([
        f'<a target="_blank" href="https://flexituat.crm4.dynamics.com/main.aspx',
        f'?appid=d0b97346-c58c-4779-b85f-419ecf17e43a',
        f'&forceUCI=1&pagetype=entityrecord&etn=account&id={accountid}">{accountname}</a>'])

# START MIDLERTIDIG
query = f'select {query_fields} from fxaccount'
cursor.execute(query)
rows = cursor.fetchall()

orgnr_list = []
orgnr_dict = {}
incorrect_orgnr = {}
missing_orgnr_count = 0
deactivated_companies_count = 0
for row in rows:
    salesperson = None
    chain = None
    name, orgnr, email, postnr, city, parentid, sluttbruker, axcmpfilter, accountid, statuscode, salesrep, chainid = row
    if salesrep:
        salesperson = get_salesperson(salesrep)
    if chainid:
        chain = get_chain(chainid)
    if int(statuscode) == 2:
        deactivated_companies_count += 1
        continue
    if orgnr:
        orgnr_fixed = orgnr.replace(' ', '')
        orgnr_list.append(orgnr_fixed)
        if not orgnr_fixed.isdigit() or len(orgnr_fixed) != 9:
            incorrect_orgnr[accountid] = (name, orgnr)
        else:
            if orgnr_fixed not in orgnr_dict:
                orgnr_dict[orgnr_fixed] = []
            orgnr_dict[orgnr_fixed].append((name, orgnr, email, postnr, city, salesperson, chain))
    else:
        missing_orgnr_count += 1

print(f'Missing org.nr: {missing_orgnr_count}')
print(f'Org.nr list: {len(orgnr_list)}')
print(f'Org.nr unique: {len(orgnr_dict)}')
print(f'Error in org.nr: {len(incorrect_orgnr)}')
for k, v in incorrect_orgnr.items():
    print(k, v)
for k, v in orgnr_dict.items():
    if len(v) > 1:
        print(k, len(v))
        for l in v:
            name, orgnr, email, postnr, city, salesperson, chain = l
            print(salesperson, name, orgnr, email or 'NO_EMAIL', postnr, city, salesperson, chain or 'NO_CHAIN')
        print('-')


sys.exit()
# END MIDLERTIDIG





query = f'select {query_fields} from fxaccount where sca_axcompanycdsfilter=? and not sca_organisationnumber is null'
cursor.execute(query, ['FXN'])
rows = cursor.fetchall()

with open('account_orgnr.html', 'w') as f:
    f.write('<html><body><h1>Accounts med feil i orgnr</h1>')
    f.write('<p><em>... samt sammenlignet navn og postnr hos BRREG</em></p>')
    for row in rows:
        accountname, orgnr, accountid, accountpostnr, accountcity = row[0], row[1], row[7], row[2], row[3]
        if not orgnr.isdigit() or len(orgnr) != 9:
            print(accountname, orgnr, accountid)
            f.write(f'<h4>{get_account_link(accountid, accountname)}</h4>')
            f.write(f'<p>')
            f.write(f'Lagret org.nr: {orgnr}')
            orgnr_fixed = orgnr.replace(' ', '')
            if orgnr_fixed.isdigit() and len(orgnr_fixed) == 9:
                f.write(f' - Skulle det vært "{orgnr_fixed}"? <a href="">Endre</a>')
                try:            
                    brreg_response = requests.get(f'https://data.brreg.no/enhetsregisteret/api/enheter/{orgnr_fixed}')
                    brreg_data = brreg_response.json()
                except:
                    print(brreg_response)
                    print(orgnr_fixed)
                    f.write(f'</p><hr>')
                    continue
                try:
                    f.write(f'<br>Brreg sier:')
                    if 'slettedato' in brreg_data:
                        f.write(f'<br>Slettet: {brreg_data.get("slettedato")} <a href="">Deaktiver i D365</a>')
                    else:
                        if brreg_data['konkurs']:
                            f.write(f'<br>KONKURS! <a href="">Deaktiver i D365</a>')
                        if brreg_data['underAvvikling']:
                            f.write(f'<br>underAvvikling!')
                        if brreg_data['underTvangsavviklingEllerTvangsopplosning']:
                            f.write(f'<br>underTvangsavviklingEllerTvangsopplosning!')
                        if brreg_data.get('navn').lower() != accountname.lower():
                            f.write(f'<br>Ulikt navn hos brreg: "{brreg_data.get("navn")}"<a href="">Endre</a>')
                        if brreg_data["forretningsadresse"]["postnummer"] != accountpostnr:
                            f.write(f'<br>Postnr brreg: "{brreg_data["forretningsadresse"]["postnummer"]}"')
                            f.write(f', i D365: "{accountpostnr}" <a href="">Endre</a>')
                        if brreg_data["forretningsadresse"]["poststed"].lower() != accountcity.lower():
                            f.write(f'<br>Poststed brreg: "{brreg_data["forretningsadresse"]["poststed"]}"')
                            f.write(f', i D365: "{accountcity}" <a href="">Endre</a>')
                except Exception as err:
                    print(f'BRREG DATA ERROR: {err}')
                    f.write(f'<br>Kunne ikke hente data fra brreg!')
            else:
                f.write(f' - Klarer ikke fikse: {orgnr}')
                if len(orgnr) < 9:
                    f.write(', det er ikke nok siffer!')
                else:
                    f.write(', det er for mange siffer!')
            f.write(f'</p><hr>')
    f.write('</body></html>')
                
    
#print(f'Fant {len(ikke_i_bruk)} accounts av type FXN hvor navn starter med "Ikke i bruk"/"Ikke bruk"')


