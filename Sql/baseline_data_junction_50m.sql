SELECT
osm_israel."Geometry"
,osm_israel."OSM_name"
,osm_israel.lu_type
,osm_israel.osm_tags

,ST_X(ST_PointOnSurface("Geometry")) as long
,ST_Y(ST_PointOnSurface("Geometry")) as lat

,markers.id

FROM 		osm_israel 
INNER JOIN 	markers
			ON (osm_israel.osm_tags LIKE '%junction%' AND ST_distance(ST_setSRID(osm_israel."Geometry",4326)::geography,markers.geom::geography) < 50)
where 		created between date '2015-01-01' and date '2018-01-01'
		and markers."locationAccuracy" = 1
