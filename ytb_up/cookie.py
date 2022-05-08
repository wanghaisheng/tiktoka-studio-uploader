
# Darin McLain
# CS595 - Web Security - ODU - Spring 2021
# Assignment 3
# 
# Script to process header files and parse out cookie information
# Output results in table format to cookies.txt

import requests
import json
import os
import re

#https://stackoverflow.com/questions/32281041/converting-cookie-string-into-python-dict
def convertcookie2valid(cookie: str, parent_domain: str):
    items = cookie.split(';')
    SameSite = HttpOnly = Secure = Domain = Path = Expires = Comment = MaxAge = CookieName = CookieValue = Size = Sessionkey = Version = Priority = None
    CookieName = CookieValue = None
    idx = len(items) - 1
    while idx >= 0:
        item = items[idx].strip()
        idx -= 1
        if not item:
            continue
        SameSiteMatched = re.match(r'^SameSite(.*)?', item, re.I)
        HttpOnlyMatched = SameSiteMatched or re.match(r'^HttpOnly(.*)$', item, re.I)
        SecureMatched = HttpOnlyMatched or re.match(r'^Secure(.*)$', item, re.I)
        DomainMatched = SecureMatched or re.match(r'^Domain(.*)?', item, re.I)
        PathMatched = DomainMatched or re.match(r'^Path(.*)?', item, re.I)
        ExpiresMatched = PathMatched or re.match(r'^Expires(.*)?', item, re.I)
        CommentMatched = ExpiresMatched or re.match(r'^Comment(.*)?', item, re.I)
        MaxAgeMatched = ExpiresMatched or re.match(r'^Max-Age=(.*)?', item, re.I)
        VersionMatched = MaxAgeMatched or re.match(r'^Version=(.*)?', item, re.I)
        PriorityMatched = VersionMatched or re.match(r'^priority=(.*)?', item, re.I)
        matched = SameSiteMatched or HttpOnlyMatched or SecureMatched or DomainMatched or PathMatched or ExpiresMatched or CommentMatched or MaxAgeMatched or VersionMatched or PriorityMatched
        if matched:
            val = matched.groups(0)[0].lstrip('=')
            if matched == SameSiteMatched:
                SameSite = val if val.lower() in ['strict', 'lax', 'none'] else None
            elif matched == HttpOnlyMatched:
                HttpOnly = True
            elif matched == SecureMatched:
                Secure = True
            elif matched == DomainMatched:
                Domain = val
            elif matched == PathMatched:
                Path = val
            elif matched == PathMatched:
                Path = val
            elif matched == ExpiresMatched:
                Expires = val
            elif matched == CommentMatched:
                Comment = val
            elif matched == MaxAgeMatched:
                MaxAge = val
            elif matched == VersionMatched:
                Version = val
            elif matched == PriorityMatched:
                Priority = val
        else:
            CookieMatched = re.match(r'^(.[^=]*)=(.*)?', item, re.I)
            if CookieMatched:
                CookieName, CookieValue = CookieMatched.groups(0)

    Sessionkey = True if not Expires else False
    Size = (len(CookieName) if CookieName else 0) + (len(CookieValue) if CookieValue else 0)

    Domain = parent_domain if CookieName and not Domain else Domain
    Path = '/' if CookieName and not Path else Path
    Priority = 'Medium' if CookieName and not Priority else Priority.title() if Priority else 'Medium'

    Cookie = {
        CookieName: CookieValue,
        'Domain': Domain,
        'Path': Path,
        'Expires': Expires,
        'Comment': Comment,
        'MaxAge': MaxAge,
        'SameSite': SameSite,
        'HttpOnly': HttpOnly,
        'Secure': Secure,
        'Size': Size,
        'Sessionkey': Sessionkey,
        'Version': Version,
        'Priority': Priority
    }
    return Cookie if CookieName else None

# loop through all of the headers files
parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
headersDirectory = os.path.join(parentDirectory, "3", "assets", "headers")
assetsDirectory = os.path.join(parentDirectory, "3", "assets")
setCookie = "set-cookie:"
results = {}


for file in os.listdir(headersDirectory):
    cookies = redirects = httpOnly = secure = samesite = strict = lax = none = path = slash = 0 # reset counters
    statuscode = None

    with open(os.path.join(headersDirectory, file)) as headerfile:
        url = file[:-4] # get url from txt file, strip out .txt
        result = {}
        
        for line in headerfile.readlines():
            # Process cookies
            if setCookie in line.lower():
                cookies += 1 # count the cookie
                line = line[len(setCookie) + 1:] # strip out Set-Cookie: 
                cookie = Robotcookie(line, "") # create object out of cookie for easy calculations
                
                # check keys for stats
                if (cookie['HttpOnly']):
                    httpOnly += 1
                if (cookie['Secure']):
                    secure += 1
                
                if (cookie['SameSite'] != None):
                    samesite += 1

                    if (str(cookie['SameSite']).lower() == "strict"):
                        strict += 1
                    elif (str(cookie['SameSite']).lower() == "lax"):
                        lax += 1
                    else:
                        none += 1

                if (cookie['Path'] != None):
                    path += 1
                    if (cookie['Path'] != "/"):
                        slash += 1

            if (line.startswith("HTTP/")):
                if (statuscode != None):
                    redirects += 1
                statuscode = line.rstrip()

        result = {
            'Cookies': cookies,
            'StatusCode': statuscode,
            'Redirects': redirects,
            'HttpOnly': httpOnly,
            'Secure': secure,
            'SameSite': samesite,
            'Strict': strict,
            'Lax': lax,
            'None': none,
            'Path': path,
            'NotSlash': slash
        }

        results[url] = result

with open(os.path.join(assetsDirectory, "cookies.json"), "w") as outfile:  # https://www.geeksforgeeks.org/how-to-convert-python-dictionary-to-json/
    json.dump(results, outfile, separators=(',', ': '), indent=4)