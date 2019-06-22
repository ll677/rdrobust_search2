# Instructions:
1. Installations:
    * install gitPython
    * in command line/terminal, call: pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

2. Git clone the rdrobust_search repository
3. Navigate to repository in command line/terminal, call python rdrobust_search.py
4. Outputs:
    1. rdr_counts.csv: column A contains DOIs of papers with code containing rdrobust, column B is number of appearance of rdrobust in the respective paper's code
    2. badRepos.csv: a list of DOIs for which a repo could not be cloned

# Files:
* rdrsrch_fxns.py: a module containing the functions necessary to run rdrobust_search
* rdrobust_search.py: a script to output the report on rdrobust's frequency
* rdrsrch_test.py: test script for rdrsrch_fxns.py


# OLD Script Outline
1. Get DOIList as list of strings
    1. Change replication_list spreadsheet on google sheets to public
    2. Query the doi column and store as python list using google sheets API (based on code from [here](https://developers.google.com/sheets/api/quickstart/python))
2. Pull the git repos
    1. Read list object of DOI strings; for each clone the repo into a subdirectory using gitPython
    2. Record DOIs that fail to clone in a pd.Series
2. Parse the code, count occurrences of rdrobust by DOI
    1. Generate accumulator pd.Series
    2. For each DOI, count number of rdrobust occurrences in do and R files; if nonzero, add to accumulator
3. Print/return report
    1. Export list of DOIs containing rdrobust and the frequency of rdrobust in the DOI as rdr_counts.csv
    2. Export list of DOIs which fail to clone in badRepos.csv