#functions for the rdrobust_search script

import os
import git
import numpy as np
import pandas as pd
import re
import datetime as dt

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
        time = repo['updated_on'])
        if URL in checked_URLs:
            index = checked_URLs.index(URL)
            old_time = checked_URLs_time[index]
            if parseTime(old_time) < parseTime(time):
                tuple_list.append((URL, time))
        else:
            tuple_list.append((URL, time))
    return tuple_list

def parseTime(s):
    
    """
    Input:
    
        s: a string representing a date and time in the form:
            <YYYY>-<MM>-<DD>T<hh>:<mm>:<ss>.<ssssss>+00:00
    
    Returns:
        
        t: a datetime object representing the date and time given by s
    """
    
    hyp1=s.find('-')
    hyp2=s.find('-',hyp1+1)
    Tpos=s.find('T')
    col1=s.find(':')
    col2=s.find(':',col1+1)
    plus=s.find('+')
    
    year=int(s[:hyp1])
    month=int(s[hyp1+1:hyp2])
    day=int(s[hyp2+1:Tpos])
    hour=int(s[Tpos+1:col1])
    minute=int(s[col1+1:col2])
    seconds=int(s[col2+1:plus])
    
    t=dt.datetime(year,month,day,hour,minute,seconds)
    
    return t

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

    repos={}
    
    #create and navigate to new directory repos
    try:
        os.mkdir('repos')
    except FileExistsError:
        pass

    current_dir=os.getcwd()

    os.chdir('repos')

    #add repos to folder named repos

    for url in URLs:
        print('cloning '+str(url))
        
        r=git.Repo.clone_from(url,os.getcwd()+'\\'+dirname)
        repos[doi]=r



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
