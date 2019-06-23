#functions for the rdrobust_search script

import os
import git
import numpy as np
import pandas as pd
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
    Parameters:
        username: email address to login to bitbucket
        password: password to login to bit bitbucket
        owner: owner of bitucket repo, i.e. aeaverification in this case
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
            if old_time < time: #these are strings, not comparable values; needs correcting
                tuple_list.append((URL, time))
        else:
            tuple_list.append((URL, time))
    return tuple_list

def cloneRepos(URLs): #NEEDS UPDATING

    """
    Clones the repos corresponding to the links in URLs into the a subdirectory
    named repos of the current working directory. May require manual login.

    Inputs:

        URLs: list of tuples; 0 index is a URL of a repo to clone, 1 index is string date
            of its last update

    Returns:

        repos: a dictionary indexing the repos' URLs to a tuple of their repo object (0)
            and last update time (1)

        
    """
    
    raise NotImplementedError

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


def rdrobustOccurrences(repos): #NEEDS UPDATING

    """
    Input:

        repos: a dictionary indexing the repos' URLs to a tuple of their repo object (0)
            and last update time (1)

    Returns:

        new_counts: A pd.DataFrame (index are URLs, col 1 is DOI if extractable, col 2 is #
            of rdrobust occurrences)
    """

    raise NotImplementedError

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

def update_rdr_counts(new_counts):
    
    """
    Updates rdr_counts.csv in current working directory with info in new_counts. Includes
    entries for new repos and replaces entries for old repos which have been modified.
    
    Input:
    
        new_counts: A pd.DataFrame (index are URLs, col 1 is DOI if extractable, col 2 is #
            of rdrobust occurrences)
    
    """
    raise NotImplementedError
    
def update_checked_URL(repos)

    """
    Updates checked_URL.csv with the URLs and last modified date of repos examined in this
    run of the script.
    
    Input:
    
        repos: a dictionary indexing the repos' URLs to a tuple of their repo object (0)
            and last update time (1)

    """
    raise NotImplementedError