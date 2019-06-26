#A script using the functions from the rdrsrch_fxns.py module to output a table
#documenting usage of rdrobust in the do and R files of a certain set of DOIs

from rdrsrch_fxns import *
import getpass as gp
# DOIList=['10.1257/app.20160056',
#              '10.1257/mac.20140181',
#              '10.1257/mic.20160125',
#              '10.1257/pol.20140391'] #testlist

username=gp.getpass('Username:')
password=gp.getpass('Password:')
URLs=getURLs(username, password, 'aeaverification')
repos=cloneRepos(URLs)
new_counts=rdrobustOccurrences(repos)
update_rdr_counts(new_counts)
update_checked_URL(repos)
