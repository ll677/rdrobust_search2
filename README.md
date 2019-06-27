# TODO:
* Re-test after recent debug of functions and script

# Instructions:

1. Git clone the rdrobust_search2 repository
2. Navigate to repository in command line/terminal, call python rdrobust_search.py
3. Relevant data is output in rdr_counts.csv

# Files:
* rdrsrch_fxns.py: a module containing the functions necessary to run rdrobust_search
* rdrobust_search.py: a script to output the report on rdrobust's frequency
* rdrsrch_test.py: test script for rdrsrch_fxns.py
* rdr_counts.csv: column A contains URLs of papers with code containing rdrobust, column B is number of appearance of rdrobust in the respective paper's code, column C is DOIs if extractable from the repo
* checked_URL.csv: column A contains URL of checked repo, column B contains date of repo's last update

# Script Outline
1. Get list of URLs paired with last modified date
    1. Generate bitbucket client using user input username and password
    2. Get repository URLs from client
    3. Filter out URLs of repositories that have already been checked and haven't been updated since the last run of the script
2. Clone repos from URLs into a subdirectory
    1. pass on repo objects paired with last modified date
3. For each repo, parse its do and R files for rdrobust
    1. If rdrobust occurs at least once, record URL, number of rdrobust occurrences, and DOI if extractable
    2. Write outputs rdr_counts.csv and checked_URL.csv


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