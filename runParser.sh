#!/bin/bash
python skeleton_parser.py ../ebay_data/items-*.json
sort -u Item.dat > Item_uniq.dat
sort -u Person.dat > Person_uniq.dat
sort -u Bid.dat > Bid_uniq.dat
sort -u Category.dat > Category_uniq.dat
sort -u Auction.dat > Auction_uniq.dat
sqlite3 E_Bay < create.sql
sqlite3 E_Bay < load.txt