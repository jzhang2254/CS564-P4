
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

# helper methods return completed row for .dat file
def strquote(quote):
    return "\"" + quote.replace("\"", "\"\"") + "\""

def itemRow(item, keys):
    if 'ItemID' not in keys:
        itemID = "NULL"
    else:
        itemID = item['ItemID']
    if 'UserID' not in item['Seller'].keys(): # seller
        userID = "NULL"
    else:
        userID = item['Seller']['UserID']
    if 'Name' not in keys:
        Name = "NULL"
    else:
        Name = strquote(item['Name'])
    if 'Description' not in keys or item['Description'] == None:
        Description = "NULL"
    else:
        Description = strquote(item['Description'])
    
    row = itemID +'|'+ userID+"|"+Name+"|"+Description+"\n"
    return row

def categoryRow(item, keys):
    rows = []
    if 'ItemID' not in keys:
        itemID = ""
    else:
        itemID = item['ItemID']
    if item['Category'] != None:
        for cat in item['Category']:
            rows.append(itemID+"|"+strquote(cat))
    return rows

def User(item, keys):
    users = []
    # seller info
    if 'Seller' not in keys:
        return "NULL" #fix !!!!!!!!!!!!!!!!!!!!!!!!!!!
    else:
        userID = item['Seller']['UserID']
    if 'Rating' not in item['Seller'].keys():
        rating = "NULL"
    else:
        rating = item['Seller']['Rating'] # cast to int????
    if 'Location' not in keys:
        location = "NULL"
    else:
        location = strquote(item['Location'])
    if 'Country' not in keys:
        country = "NULL"
    else:
        country = strquote(item['Country'])
    seller = userID+"|"+ rating+"|"+location+"|"+country+"\n"
    users.append(seller)
    
    # buyer info  
    if item.get('Bids') != None :
        for bid in item['Bids']:
            bidder2, rating2, location2, country2 ='NULL'
            
            bidder2 = bid["Bid"]["Bidder"]["UserID"]
            # print(bidder2)
            if 'Rating' not in bid.keys():
                rating2 = bid["Bid"]["Bidder"]["Rating"]
            if 'Location' in bid.keys():
                location2 = strquote(bid["Bid"]["Bidder"]["Location"])
            else:
                location2 = 'NULL'
            if 'Country' in bid.keys():
                country2 = strquote(bid["Bid"]["Bidder"]["Country"])
            else:
                country2 = 'NULL'
            buyer = bidder2+"|"+rating2+"|"+location2+"|"+country2+"\n"
            users.append(buyer)
    return users
    
def Bid(item, keys):
    if 'ItemID' not in keys:
        itemID = "" # error 
    else:
        itemID = item['ItemID']
    if 'Seller' in keys:
        userID = item['Seller']['UserID']
    elif 'UserID' not in item['Seller'].keys():
        if item['Bid'] != None:
            for bid in item['Bids']:
                userID = bid['Bid']['Bidder']['UserID']
        else:
            userID = None
        
    if item['Bids'] == None:
        time = 'NULL'
        amount = 0.00
    else:
        for bid in item['Bids']:
            time = transformDttm(bid['Bid']['Time'])
            amount = transformDollar(bid['Bid']['Amount'])
    return itemID+"|"+userID+"|"+time+"|"+str(amount)+"\n"
    
def Auction(item, keys):
    if 'ItemID' not in keys:
        itemID = ""
    else:
        itemID = item['ItemID']
    if 'Currently' not in keys:
        currently = "0.00"
    else:
        currently = transformDollar(item['Currently'])
    if 'Buy_Price' not in keys:
        buy_price = transformDollar(None)
        if buy_price == None:
            buy_price = "NULL"
    else:
        buy_price = transformDollar(item['Buy_Price'])
    if 'First_Bid' not in keys:
        first_bid = transformDollar(None)
        if first_bid == None:
            first_bid == "NULL"
    else:
        first_bid = transformDollar(item['First_Bid'])
    if 'Number_of_Bids' not in keys:
        numBids = "0"
    else:
        numBids = item['Number_of_Bids']
    if 'Started' not in keys:
        started = "NULL"
    else:
        started = transformDttm(item['Started'])
    if 'Ends' not in keys:
        ended = "NULL"
    else:
        ended = transformDttm(item['Ends'])

    return itemID+"|"+buy_price+"|"+first_bid+"|"+currently+"|"+numBids+"|"+started+"|"+ended+"\n"

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    itemSchema = open('Item.dat', mode='a+')
    catSchema = open('Category.dat', mode='a+')
    perSchema = open('Person.dat', mode='a+')
    bidSchema = open('Bid.dat', mode='a+')
    aucSchema = open('Auction.dat', mode='a+')
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json fil
        # print("file: ", json_file)
        count = 0
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            keys = item.keys()
            items = itemRow(item, keys)
            itemSchema.write(items)
            cat_row = categoryRow(item, keys)
            for c in cat_row:
                c = c+"\n"
                catSchema.write(c)
            person = User(item, keys) 
            for p in person:
                perSchema.write(p)
            bid = Bid(item, keys)
            bidSchema.write(bid)
            auction = Auction(item, keys)
            aucSchema.write(auction)
            count += 1
        # print(count)
            # print('item: ', item_row)
            # print(item)
            # break
            # print('category: ', cat_row)
            # print('person: ', person)
            # print("bid: ", bid)
            # print('auction: ', auction)

            # print()

            # if count == 2:
            #     break
            

        
        # print(itemSchema)
    f.close()
    itemSchema.close()
    itemSchema.close()
    catSchema.close()
    perSchema.close()
    bidSchema.close()
    aucSchema.close()
    # print("total_files: ", total_files)
    

    

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
