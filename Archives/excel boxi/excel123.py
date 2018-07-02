#! /usr/bin/env python
# coding=utf-8
import sys
import excel
import csc.csclxmls, path, fnmatch

# out = path.path('output.log')
pth = path.path('excelsettings.xml')
cc = csc.csclxmls.node(pth)
# open excel of raw data
f = excel.OpenExcel(cc('//item[@key="raw"]').text)
sh = f.data.sheet_by_name('RawData_Status Change')
# choose row headers
fields = sh.row_values(3)

# create dictionary to get cnd amount for each line
field_cat = [x.tag for x in cc('//categories/*')]
lfield_cat = [0] * len(field_cat)
count_cnd_dt = dict(zip(field_cat, lfield_cat))

count_l1_dt = {"SBO": 0, "DCO": 0, "SHELL": 0, "AAE": 0, "ONSEC": 0}
# a = ''
for y in range(4, sh.nrows):  #
    # dictionary key pairs of data
    value = sh.row_values(y)
    x = dict(zip(fields, value))
    ag = x['%s' % cc('//item[@key="Resolved"]').text]
    ag2 = x['%s' % cc('//item[@key="Responsible"]').text]
    ag3 = x['%s' % cc('//item[@key="TitleDesc"]').text]

    # crawl data
    try:
        # line below is searching if the xml contains the ag based on the data,
        # if yes , find it's key and update accordingly to the count_dt for CND
        sl = cc('//item[string()="%s"]' % ag)
        l1 = cc('//WI/item')

        if isinstance(sl, csc.csclxmls.nodelist):
            sl = sl[0]['key']
            x.update({'BOXI Crit': '%s' % sl})
        else:
            sl = sl['key']
            x.update({'BOXI Crit': '%s' % sl})
        count_cnd_dt[sl] += 1

        for y in l1:
            if x['BOXI Crit'] == "AAE":
                if y.text.lower() in ag3.lower() and y['key'] == x['BOXI Crit'] and y['group'] == ag:
                    count_l1_dt[y['key']] += 1
            elif y.text.lower() in ag3.lower() and y['key'] == x['BOXI Crit']:
                count_l1_dt[y['key']] += 1

    except:
        if ag is None:
            try:
                # repeat sequence for another header
                # sl = cc('//item[fmatch(string(),"%s")]' % ag2)
                sl = cc('//item[string()="%s"]' % ag2)
                l1 = cc('//WI/item')
                if isinstance(sl, csc.csclxmls.nodelist):
                    sl = sl[0]['key']
                    x.update({'BOXI Crit': '%s' % sl})
                else:
                    sl = sl['key']
                    x.update({'BOXI Crit': '%s' % sl})
                count_cnd_dt[sl] += 1

                for y in l1:
                    if x['BOXI Crit'] == "AAE":
                        if y.text.lower() in ag3.lower() and y['key'] == x['BOXI Crit'] and y['group'] == ag2:
                            count_l1_dt[y['key']] += 1
                    elif y.text.lower() in ag3.lower() and y['key'] == x['BOXI Crit']:
                        count_l1_dt[y['key']] += 1

            except:  # else , add those that are not included in OTHERS
                sl = 'OTHERS'
                count_cnd_dt[sl] += 1
                continue
# out.write_bytes(a)
print count_cnd_dt
print count_l1_dt


# if not (a):
#     a = ag + ' ' + ag2 + ' ' + sl
# else:
#     a = a + '\n' + ag + ' ' + ag2 + ' ' + sl




















# for data in var:
#    if x['INM Resolve Group Name'] in cc('//item[@key="%s"]' % str(data) ).text:
#        eval("data += 1")
# x.update({'department': data })
# if x['INM Resolve Group Name'] in cc('//item[@key="SBO"]').text:
#     SBO += 1
# elif x['INM Resolve Group Name'] in cc('//item[@key="DCO"]').text:
#     DCO += 1
# elif x['INM Resolve Group Name'] in cc('//item[@key="SHELL"]').text:
#     SHELL += 1
# elif x['INM Resolve Group Name'] in cc('//item[@key="ONSEC"]').text:
#     ONSEC += 1
# elif x['INM Resolve Group Name'] in cc('//item[@key="SAP"]').text:
#     SAP += 1
# elif x['INM Resolve Group Name'] in cc('//item[@key="AAE"]').text:
#     AAE += 1
# elif x['INM Resolve Group Name'] in cc('//item[@key="CCS"]').text:
#     CCS += 1
# else:
#     if x['INM Responsible Group Name'] in cc('//item[@key="SBO"]').text:
#         SBO += 1
#     elif x['INM Responsible Group Name'] in cc('//item[@key="DCO"]').text:
#         DCO += 1
#     elif x['INM Responsible Group Name'] in cc('//item[@key="SHELL"]').text:
#         SHELL += 1
#     elif x['INM Responsible Group Name'] in cc('//item[@key="ONSEC"]').text:
#         ONSEC += 1
#     elif x['INM Responsible Group Name'] in cc('//item[@key="SAP"]').text:
#         SAP += 1
#     elif x['INM Responsible Group Name'] in cc('//item[@key="AAE"]').text:
#         AAE += 1
#     elif x['INM Responsible Group Name'] in cc('//item[@key="CCS"]').text:
#         CCS += 1


# for x in exceldata:
