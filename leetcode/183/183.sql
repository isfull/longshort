## more efficiency
## group count select  n
select a.Name as Customers from Customers a left join Orders b on a.Id=b.CustomerId group by a.Id having count(b.CustomerId) = 0
## bad one
## n/2 * n/2
select Name as Customers from Customers where Id not in (select a.Id from Customers a join Orders b on a.Id = b.CustomerId)