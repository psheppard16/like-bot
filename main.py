__author__ = 'Preston Sheppard'
from os import listdir
from os.path import isfile, join
import os
import requests
import pickle
from imgurAccount import ImgurAccount

def createAccount(name, clientId, clientSecret, extension=False):
    newAccount = None
    if extension:
        filePath = "accounts/" + name
    else:
        filePath = "accounts/" + name + ".txt"
    try:
        with open(filePath):
            raise Exception("An account with that name already exists")
    except IOError:
        newAccount = ImgurAccount(name, clientId, clientSecret)
        open(filePath, "a")
        with open(filePath, 'wb') as input:
            pickle.dump(newAccount, input, pickle.HIGHEST_PROTOCOL)
    if accountIsUnique(newAccount):
        return newAccount
    else:
        deleteAccount(newAccount.name)
        raise Exception("There is already an account registered to that user")

def accountIsUnique(accountToCheck):
    accounts = loadAllAccounts()
    for account in accounts:
        if accountToCheck.name != account.name:
            if accountToCheck.accountUsername == account.accountUsername:
                return False
    return True

def deleteAccount(name, extension=False):
    if extension:
        os.remove("accounts/" + name)
    else:
        os.remove("accounts/" + name + ".txt")

def loadAccount(name, extension=False):
    if extension:
        filePath = "accounts/" + name
    else:
        filePath = "accounts/" + name + ".txt"
    try:
        with open(filePath, 'rb') as file:
            return pickle.load(file)
    except IOError:
        raise Exception("An account with that name does not exists")

def deleteAllAccounts():
    accountDir = "accounts"
    accountFiles = [f for f in listdir(accountDir) if isfile(join(accountDir, f))]
    for fileName in accountFiles:
        os.remove(accountDir + "/" + fileName)

def loadAllAccounts():
    accounts = []
    accountDir = "accounts"
    accountFiles = [f for f in listdir(accountDir) if isfile(join(accountDir, f))]
    for fileName in accountFiles:
        accounts.append(loadAccount(fileName, extension=True))
    return accounts

def getSubmissions(accessToken, username, page=0):
    endPoint = "https://api.imgur.com/3/account/" + username + "/submissions/" + str(page)

    headers = {'Authorization': 'Bearer ' + accessToken}

    request = requests.get(endPoint, headers=headers)

    return request.json()['data']

def upvoteAllPosts(accessToken, username):
    submissions = getSubmissions(accessToken, username)
    accounts = loadAllAccounts()
    for submission in submissions:
        for account in accounts:
            account.upvotePost(submission['id'])

def upvoteMostRecentPost(accessToken, username):
    submissions = getSubmissions(accessToken, username)
    accounts = loadAllAccounts()
    for account in accounts:
        account.upvotePost(submissions[0]['id'])

clientId = "b41989483eb0563"
clientSecret = "9757b87faf30fb279e44ef24882bbdfd416cd4d0"
image = open('Testing.jpg', 'rb').read()


#add code here

# loads all accounts
accounts = loadAllAccounts()

# uploads a post
# account.uploadAndShare(image, "Test Name", "Test Title", "Test Description")

# runs method "somthing" for all accounts
for account in accounts:
    account.somthing

