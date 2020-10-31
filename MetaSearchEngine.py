import json, sys
import urllib
import requests
from apiclient.discovery import build


if __name__ == '__main__':

    # ask user to enter a query
    query = raw_input('Enter your query: ')

    # ask for number of results for google
    gnum = raw_input('Enter the number of results you want from Google (Normal value is 10): ')

    print "---------------------------------------------------------------------"

    gtitles = []  # store google result titles
    glinks = []  # store google result links

    gsearch = str(query)  # convert to a string
    grequests = 1  # search query to engine once, if you want to get more than 10 results, increase value
    if int(gnum) > 10:  # if user wants more than 10 results, 1 page = 10 results
        grequests = int(gnum[:-1]) + 1  # then we have to increase to page more pages, example: if gnum = 15 then 1+1 = 2 grequests (2 pages = 20 results)

    # print(grequests, "this is no of request:")

    # Google Custom Search Engine ID
    gid = 'Your cse id'
    # Google Custom Search API Key
    gkey = 'your google id'

    # Create Service object
    service = build('customsearch', 'v1', developerKey=gkey)
    googleCSE = service.cse()

    counter = 1
    print "Top", gnum, "Results from Google"

    for i in range(grequests):  # for number of pages to get
        startpage = 1 + (i * 10)  # starting with page 1 results
        # Create request
        sendrequest = googleCSE.list(q=gsearch, num=10, start=startpage, cx=gid)
        # num = 10 means get 10 results, maximum value is 10
        # Get response
        gresponse = sendrequest.execute()
        # print response
        # Store response in json format
        gresult = json.dumps(gresponse, sort_keys=True, indent=2)
        # Change json format into python object
        gresult2 = json.loads(gresult)
        # print gresult2
        # print "Title:", gresult2["title"]
        # print "Link:", gresult2["link"]
        for i in range(len(gresult2['items'])):  # for every result in response
            if counter > int(gnum):  # keep only specified amount of results
                break
            title = gresult2['items'][i]['title']  # store title in variable
            print str(counter) + ") Title: " + title  # print result title

            # print type(title), "************type of the title which we are getting from the google: \n"
            counter = counter + 1
            # print "    Link:", gresult2['items'][i]['link']  # print result link
            gtitles.append(title.encode('utf-8'))  # str(title)) #store google result title in utf-8 encoding
            glinks.append(str(gresult2['items'][i]['link']))  # store google result link
    # print gtitles
    # print glinks

    for g_links in glinks:
        # print type(bing_links)
        # print "bing link ********************************** "
        print g_links

    # for bing_name in gtitles:
    #     print type(bing_name)
    #     print " bing name *************"
    #     print bing_name

    print "---------------------Google search part over------------------------------------------------"

    subscription_key = "your bing api key"
    assert subscription_key

    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"

    search_term = query

    import requests

    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}

    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    btitles = []  # store Bing result titles
    blinks = []  # store Bing result links

    for v in search_results["webPages"]["value"]:
        #     print("   url: ",  v["url"])
        #     print("   Name:",v["name"])
        #     print("   Snippet:", v["snippet"])

        name_bing = v["name"]
        link_bing = v["url"]

        btitles.append(name_bing)
        blinks.append(link_bing)

    

    print "******************************************************************"
    print "\n links from the bing search engine \n"
    count = 1

    for links_bing in blinks:
        print count, ")", links_bing
        count = count + 1

    # for title_bing in btitles:
    #     print "this is title", title_bing

    # =================================================================================================================

    # Rank Aggregation Algorithm: Borda Fuse

    ftitles = []  # store all titles
    flinks = []  # store all links
    fscores = []  # store all scores

    # gn = len(glinks) # total number of results of Google
    gn = int(gnum)  # number of results from Google specified by user
    bn = len(blinks)  # number of results from Bing specified by user

    print "No of Links fetched from the google: ", gn
    print "No of links fetched from the bing:", bn

    # calculate scores for Google results
    grank = gn  # keeps track of Google rank score for each result
    found = 0
    for i in range(gn):  # for every result in Google
        for j in range(bn):  # for every result in Bing
            # print "glinks[i]:", glinks[i]
            # print "blinks[j]:", blinks[j]
            if glinks[i] == blinks[j]:  # if google result is in bing result
                # keep Google result score
                ftitles.append(gtitles[i])  # store title
                flinks.append(glinks[i])  # store link
                # rank 1 is N points, rank 2 is N-1 points, rank 3 is N-2 points, etc...
                fscores.append(grank + (bn - j))  # google rank score + bing rank score
                found = 1
                break
        # if it is not in bing's results
        if found == 0:
            ftitles.append(gtitles[i])  # store title
            flinks.append(glinks[i])  # store link
            fscores.append(grank)  # google rank score
        grank = grank - 1
        found = 0

    # look for Bing results not in Google results and calculate scores
    brank = bn  # keeps track of Bing rank score for each result
    i = 0  # reset
    for i in range(bn):
        # for j in range(len(flinks)):
        # if blinks[i] != flinks[j]: #if Bing result not in final links (aka not in Google results)
        if blinks[i] not in flinks:  # if Bing result not in final links (aka not in Google results)
            # keep Bing reuslt score
            ftitles.append(btitles[i])  # store title
            flinks.append(blinks[i])  # store link
            fscores.append(brank)  # Bing rank score
        brank = brank - 1

    # ===========================================================================

    highest = 0
    pos = 0
    rank = 1  # counter
    num_of_unique_links = len(fscores)

    print "total no of unique links from both the search engines: ", num_of_unique_links

    print "\n Ranked Results of Google and Bing \n"
    for x in range(len(fscores)):  # for every score
        for y in range(len(fscores)):  # find highest score
            if fscores[y] > highest:
                highest = fscores[y]
                pos = y
        print str(rank) + ") Title: " + ftitles[pos]  # print title
        print "    Link:", flinks[pos], "\n"  # print link
        fscores[pos] = -1
        pos = 0  # reset
        highest = 0  # reset
        rank = rank + 1  # increase counter

