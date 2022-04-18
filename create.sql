drop table if exists Item;
drop table if exists Seller;
drop table if exists Bidder;
drop table if exists Category;
drop table if exists Bid;
drop table if exists Auction;


create table Item (ItemID varChar(16), Name varChar(16), UserID varChar(16), Description varChar(64)  ); 
create table Seller ( UserID varChar(16), Rating int, Location varChar(16), Country varChar(16));
create table Bidder ( UserID varChar(16), Rating int, Location varChar(16), Country varChar(16));
create table Category ( itemID int, CategoryName varchar(32));
create table Bid ( ItemID int, UserID varChar(16), Time date, Amount float);
create table Auction ( ItemID int, Buy_Price float, Currently float, First_Bid float, Number_of_Bids int, Started date, Ended date );
