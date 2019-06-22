#A script using the functions from the rdrsrch_fxns.py module to output a table
#documenting usage of rdrobust in the do and R files of a certain set of DOIs

import rdrsrch_fxns as rf

# DOIList=['10.1257/app.20160056',
#              '10.1257/mac.20140181',
#              '10.1257/mic.20160125',
#              '10.1257/pol.20140391'] #testlist

DOIList=rf.getDOIListGoogleSheet()
# DOIList=rf.getDOIList()
#print(DOIList)
temp=rf.cloneRepos(DOIList)
repos=temp[0]
badRepos=temp[1]
rdr_counts=rf.rdrobustOccurrences(repos)
rf.series_to_csv(rdr_counts,'rdr_counts.csv')
rf.series_to_csv(badRepos,'badRepos.csv')
