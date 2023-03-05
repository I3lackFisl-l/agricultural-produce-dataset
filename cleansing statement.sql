with a as(
	select year-543 year_no, plant, trim(region_province) region_province, convert(int,replace(month_no,'month_','')) month_no, produce_value
	from argriculture 
		unpivot(produce_value for month_no in (month_01, month_02, month_03, month_04, month_05, month_06, month_07, month_08, month_09, month_10, month_11, month_12)) as pvt
	--order by pvt.year, pvt.plant
)
--select *
--from a
--left join (
--	select provinceid, provincename from spatial_rain
--) s on s.ProvinceName = a.region_province
--where s.ProvinceID is null
insert into argriculture_produce_with_rain
select provinceid, provincename, minrain, maxrain, avgrain, year_no, month_no, date, plant, produce_value 
from spatial_rain s
inner join a on a.year_no = s.Year and a.month_no = s.Month and a.region_province = s.ProvinceName