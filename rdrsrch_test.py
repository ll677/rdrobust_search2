#test script for rdrsrch_fxns
import rdrsrch_fxns as rf
import shutil

def test_cloneRepos():

    #No good existing examples of AER repos

    #full journal names in URL; macro instead of mac or micro instead of mic
    DOIList=['10.1257/app.4.2.98',
             '10.1257/mac.20120257',
             '10.1257/mic.20110077',
             '10.1257/pol.20130407']

    #abbreviated journal names in URL
    # DOIList=['10.1257/app.20160056',
    #          '10.1257/mac.20140181',
    #          '10.1257/mic.20160125',
    #          '10.1257/pol.20140391'] #only one confirmed to contain rdrobust

    DOIList+=['10.1257/app.20160056',
             '10.1257/mac.20140181',
             '10.1257/mic.20160125',
             '10.1257/pol.20140391'] #only one confirmed to contain rdrobust

    output=rf.cloneRepos(DOIList)

    return output

# old test function doesn't work for our new URLs methond
def test_rdrobustOccurrences(repos):

    rdr_counts=rf.rdrobustOccurrences(repos)
    rf.series_to_csv(rdr_counts,'rdr_counts.csv')


#test function calls

# repos=test_cloneRepos()[0]
# test_rdrobustOccurrences(repos)

# shutil.rmtree('repos')
