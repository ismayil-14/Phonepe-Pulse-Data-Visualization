create database phonepe;
use phonepe;

select State as "State" , sum(District_users) as "User Count" from map_user where Year = 2018 and Quarter = 4 group by State order by sum(District_users) desc limit 10;

select State, sum(Amount) as "Total Amount" from map_transaction  where Year = 2018 and Quarter = 1 group by State;

select * from agg_transaction;

select * from agg_user ;

select brand,sum(brand_count)  from agg_user group by brand ;

select * from map_transaction;

select * from  map_user ;

select sum(District_users) from map_user;

select * from  top_transaction_district ;

select* from top_transaction_pincode;

select * from  top_user_district ;

select State as "State" , sum(District_users) as "User Count" from map_user where Year = 2018 and Quarter = 4 group by State order by sum("User Count") desc limit 10;

select* from top_user_pincode;

create table agg_transaction(
  State varchar(50) ,
  Year int ,
  Quarter int,
  Transaction_type varchar(50) ,
  Transaction_count int ,
  Transaction_amount decimal(15) 
);

create table agg_user(
  State varchar(50) ,
  Year int ,
  Quarter int,
  Brand varchar(50),
  Brand_count int ,
  Brand_percentage float 
);
  
create table top_user_district(
  State varchar(50) ,
  Year int ,
  Quarter int,
  District_name varchar(50),
  District_users int
);

create table top_user_pincode(
  State varchar(50) ,
  Year int ,
  Quarter int,
  Pincode int,
  Pincode_users int
);

create table top_transaction_district(
  State varchar(50) ,
  Year int ,
  Quarter int,
  District_name varchar(50),
  District_amount float,
  District_count int
);

create table top_transaction_pincode(
  State varchar(50) ,
  Year int ,
  Quarter int,
  Pincode int,
  Pincode_amount float,
  Pincode_count int
);

create table map_transaction(
  State varchar(50) ,
  Year int ,
  Quarter int,
  District_name varchar(50),
  Amount float,
  Count int
);

create table map_user(
  State varchar(50) ,
  Year int ,
  Quarter int,
  District_name varchar(50),
  District_users int
  );
  
select State , sum(Amount) from map_transaction group by State order by sum(Amount) desc limit 10;

select District_name , sum(Amount) from map_transaction where Year = 2018 and Quarter = 1 and State = 'Kerala' group by District_name order by sum(Amount) desc limit 10;