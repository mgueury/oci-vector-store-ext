load data
infile 'support_sr.csv'
into table support_sr
fields terminated by "," optionally enclosed by '"'
( id,
  customer_name,
  owner_id,
  subject,
  question CHAR(20000),
  answer,
  internal
)
