with A as (select count(ItemID) as countItem from Category group by ItemID) select count(countItem) from A where countItem = 4; 