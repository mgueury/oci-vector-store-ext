load data
infile 'support_owner.csv'
into table support_owner
fields terminated by "," optionally enclosed by '"'
( id, first_name, last_name, email, phone )
