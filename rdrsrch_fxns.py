#functions for the rdrobust_search script

import os
import git
import numpy as np
import pandas as pd
import glob
import re

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from bitbucket.client import Client
def getURLs(username, password, owner):
    """
    Returns a list of tuples of bitbuckets URLs and last_updated time that we
    want to clone. Also, generate a checked_URL.csv file that stores the URLs
    and last_updated time for each URL. If last_updated time of a URL is before
    the last modified time we got from bitbucket website, we append a tuple of
    URL and last_modified time of that URL, otherwise we will just skip this URL
    because we have already checked it before.

    Example: TODO
    """
    tuple_list = []
    df = pd.read_csv("checked_URL.csv")
    checked_URLs= list(df['URL'])
    checked_URLs_time = list(df['last_updated_time'])

    client = Client(str(username), str(password), str(owner))
    repos = client.get_repositories()['values']
    for repo in repos:
        links = repo['links']
        clone = links['clone']
        URL = clone[0]['href']
        time = repo['updated_on']
        if URL in checked_URLs:
            index = checked_URLs.index(URL)
            old_time = checked_URLs_time[index]
            if old_time < time:
                tuple = (URL, time)
                tuple_list.append(tuple)
        else:
            tuple = (URL, time)
            tuple_list.append(tuple)
    return tuple_list

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1pLxxyg01L-UkNpBWgP2xCRe7hIuUNw6e9BnVIqcO76c'
SAMPLE_RANGE_NAME = 'MASTER Summer 2018 forward!A:A'

def getDOIListGoogleSheet():
    """
    Get a List of DOIs from Replication_List spreadsheet.
    """
    DOIList = []
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values:
            # Print columns A, which correspond to indices 0.
            DOIList.append(row[0])
            # print('%s' % (row[0]))
    return DOIList[1:]



def getDOIList():
    """
    Return DOIList from excel file
    """
    excel = pd.ExcelFile("Replication_List.xlsx")
    excel = excel.parse("MASTER Summer 2018 forward")
    doilist = list(excel['DOI'])
    return doilist

def cloneRepos(DOIList):

    """
    Clones the repos corresponding to the DOIs in DOIlist into the a subdirectory
    named repos of the current working directory. Should require manual
    login once. Assumes that the repos have URLs in following format:

    https://bitbucket.org/aeaverification/<journal>-<DOI prefix>-<DOI suffix>.git

    NOTE: most AER URLs in bitbucket appear "non-standard"; convention used is that given in wiki

    Inputs:

        DOIList: list of strings representing DOIs to check

            NOTE: the DOIs MUST be in following format WITHOUT being
            headed by "doi:" :

            <prefix>/<suffix>

    Returns:

        repos: a dictionary indexing the elements of DOIlist to their repos

        badRepos: a Series of strings representing DOIs for which a repo could not be pulled
    """

    jnames={'app':'aej-applied','mac':'aej-macro','mic':'aej-micro',
              'pol':'aej-policy','aer':'aer'}

    repos={}

    badRepos=[]

    #create and navigate to new directory repos
    try:
        os.mkdir('repos')
    except FileExistsError:
        pass

    current_dir=os.getcwd()

    os.chdir('repos')

    #add repos to folder named repos

    for doi in DOIList:
        print('cloning'+str(doi))
        a=doi.index('/')
        b=doi.index('.',a)

        #get prefix, suffix
        pref=doi[:a]
        suff=doi[a+1:]

        #get journal
        key=doi[a+1:b]
        journal=jnames[key]

        dirname='%s-%s-%s' % (journal, pref, suff)

        URL='https://bitbucket.org/aeaverification/' + dirname + '.git'

        try:

            r=git.Repo.clone_from(URL,os.getcwd()+'\\'+dirname)
            repos[doi]=r

        except:

            try:

                journal='aej-'+key
                dirname='%s-%s-%s' % (journal, pref, suff)
                URL='https://bitbucket.org/aeaverification/' + dirname + '.git'
                r=git.Repo.clone_from(URL,os.getcwd()+'\\'+dirname)
                repos[doi]=r

            except:

                badRepos+=[doi]



    #navigate back to original directory

    os.chdir(current_dir)

    return (repos,pd.Series(badRepos))


def rdrobustOccurrences(repos):

    """
    Input:

        repos: a dictionary of repos indexed by their DOI strings

    Returns:

        rdr_counts: A Series with indices as the DOIs containing rdrobust,
            each indexing the number of occurrences of rdrobust in that DOI
    """

    # raise NotImplementedError
    DOIList = repos.keys()
    dic = {}
    for doi in DOIList:
        ct=0
        paths = getFilePaths(repos[doi].working_dir)
        for f in paths:
            file=open(f,'r', errors='ignore')
            text=file.read()
            file.close()
            ct+=count_rdrobust(text)
        if ct>0:
            dic[doi]=ct

    #     count = 0
    #     r = repos[doi]
    #     path = os.path.abspath(str(r))
    #     lst_do = glob.glob(str(path)+"/*.do")
    #     lst_R = glob.glob(str(path)+"/*.R")
    #     if len(lst_do)>0 or len(lst_R)>0:
    #         for do in lst_do:
    #
    #         count = len(lst_do) + len(lst_R)
    #         dic[doi] = count

    rdr_counts= pd.Series(dic)
    return rdr_counts

def getFilePaths(dir):

        """
        Input:

            dir: the path (as a string) to a directory to search

        Returns:

            paths: a list of do and R filepaths contained in dir and its
                subdirectories
        """

        dirtree=os.walk(dir)
        paths=[]
        for t in dirtree:
            for f in t[2]:
                if f[-3:]=='.do' or f[-2:]=='.R':
                    paths = paths + [os.path.join(t[0],f)]
        return paths

def count_rdrobust(text):

    """
    Input:

        text: string to parse

    Returns:

        count: occurrances of rdrobust in the text
    """

    count=sum(1 for i in re.finditer('rdrobust',text))
    return count

def series_to_csv(srs,filepath):
    """
    Input:
        srs: a Series with indices = doi strings and values = rdr_counts
        filepath: path of the series output
    Returns:
        None. Generate a csv file.
    """
    srs.to_csv(filepath)
