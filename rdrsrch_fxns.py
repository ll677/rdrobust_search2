#functions for the rdrobust_search script

import os
import git
# import numpy as np
import pandas as pd
import re
import datetime as dt
# import json
# import requests

from bitbucket.client import Client

##### SCRIPT FUNCTIONS #####

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
        
    Returns:
    
        URLs: dict; URLs of repos to clone index tuples, 0 index is string date
            of last update, 1 index is string name of repo
    """
    URLs={}
    df = pd.read_csv("checked_URL.csv")
    checked_URLs= list(df['URL'])
    checked_URLs_time = list(df['last_updated_time'])
    client = Client(str(username), str(password), str(owner))
    # repos = client.get_repositories()['values']
    
    # alt soln. here: https://thepythoncoding.blogspot.com/2019/06/python-script-to-clone-all-repositories.html?fbclid=IwAR0a-cI-EI9cA1cgQGkiXCY9R6-5SrJq_NItKurEQ59eSVnzGCVpmKtWs7g
    
    # compile repo list
    pg=1
    d=[0]
    repos=[]
    while len(d)>0:
        d=client.get_repositories(params={'pagelen':100,'page':pg})['values']
        repos=repos+d
        pg+=1
    
    #get URLs
    for repo in repos:
        links = repo['links']
        clone = links['clone']
        URL = clone[0]['href']
        upd = repo['updated_on'])
        name = repo['name']
        if URL in checked_URLs:
            index = checked_URLs.index(URL)
            old_upd = checked_URLs_time[index]
            if parseTime(old_time) < parseTime(upd):
                URLs[URL]=(upd,name)
        else:
            URLs[URL]=(upd,name)
    return URLs


def cloneRepos(URLs): 

    """
    Clones the repos corresponding to the links in URLs into the a subdirectory
    named repos of the current working directory. May require manual login.

    Inputs:

        URLs: dict; URLs of repos to clone index tuples, 0 index is string date
            of last update, 1 index is string name of repo

    Returns:

        repos: a dictionary indexing the repos' URLs to a tuple of their repo object (0),
            last update time (1), and DOI if present (2) ('' if not present)

        
    """
    
    repos={}
    
    #create and navigate to new directory repos
    try:
        os.mkdir('repos')
    except FileExistsError:
        pass

    current_dir=os.getcwd()

    os.chdir('repos')

    #add repos to folder named repos

    for url in URLs.keys():
        print('cloning '+str(url))
        upd=URLs[url][0]
        name=URLs[url][1]
        r=git.Repo.clone_from(url,os.getcwd()+'\\'+name)
        
        #Try to get DOI
        DOI=''
        suffSt=name.find('10.1257-')+8
        suffEnd=0
        if suffLoc-8 >= 0:
            for t in ['/','-','.git']:
                SuffEnd=min(suffEnd,name.find(t,suffSt))
            DOI='10.1257/'+name[suffSt,suffEnd]
        repos[url]=(r,upd,DOI)

    #navigate back to original directory

    os.chdir(current_dir)

    return repos


def rdrobustOccurrences(repos): 

    """
    Input:

        repos: a dictionary indexing the repos' URLs to a tuple of their repo object (0),
            last update time (1), and DOI if present (2) ('' if not present)

    Returns:

        new_counts: A pd.DataFrame (index are URLs, col 1 is DOI if extractable, col 2 is #
            of rdrobust occurrences)
    """

    new_counts=pd.DataFrame(index=pd.core.indexes.base.Index([],name='URL'),
                            columns=['DOI','rdr_counts'])
    URLs=repos.keys()
    for url in URLs:
        ct=0
        paths = getFilePaths(repos[url][0].working_dir)
        for f in paths:
            file=open(f,'r', errors='ignore')
            text=file.read()
            file.close()
            ct+=count_rdrobust(text)
        if ct>0:
            new_counts.at[url]={'DOI':repos[url][2],'rdr_counts':ct}
            
    return new_counts

def update_rdr_counts(new_counts):
    
    """
    Updates rdr_counts.csv in current working directory with info in new_counts. Includes
    entries for new repos and replaces entries for old repos which have been modified.
    
    Input:
    
        new_counts: A pd.DataFrame (index are URLs, col 1 is DOI if extractable, col 2 is #
            of rdrobust occurrences)
    
    """
    old_counts=pd.read_csv('rdr_counts.csv',index_col='URL')
    old_counts.update(new_counts[new_counts.index.isin(old_counts.index)])
    rdr_counts=old_counts.append(new_counts[~new_counts.index.isin(old_counts.index)])
    rdr_counts.to_csv('rdr_counts.csv')
    
    
def update_checked_URL(repos):

    """
    Updates checked_URL.csv with the URLs and last modified date of repos examined in this
    run of the script.
    
    Input:
    
        repos: a dictionary indexing the repos' URLs to a tuple of their repo object (0),
            last update time (1), and DOI if present (2) ('' if not present)
    """
    checked_URL=pd.read_csv('checked_URL.csv',index_col='URL')
    for url in repos.keys():
        checked_URL.at[url]={'last_updated_time':repos[url][1]}
    checked_URL.to_csv('checked_URL.csv')


##### HELPER FUNCTIONS #####

# getURLs helpers

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

# rdrobustOccurrences helpers

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
