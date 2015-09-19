import math
from math import radians, cos, sin, asin, sqrt



def calc_distance_cpp(org_lon, org_lat, dst_lon, dst_lat):
	NTU_2_M = 1.1112
	COS_5DEG = 0.9961947
	COS_15DEG = 0.96592583
	COS_25DEG = 0.90630779
	COS_35DEG = 0.81915204
	COS_45DEG = 0.70710678
	COS_55DEG = 0.57357644
	COS_65DEG = 0.42261826
	COS_75DEG = 0.25881905
	COS_85DEG = 0.087155743
	
	delta_lon = dst_lon - org_lon
	delta_lat = dst_lat - org_lat
	delta_lat = delta_lat*NTU_2_M

	lat = int(org_lat / 1000000)
	if( lat < 0 ):
		lat = -lat
		
	if(lat==0):
		delta_lon = (NTU_2_M * COS_5DEG)*delta_lon
	elif(lat==1):
		delta_lon = (NTU_2_M * COS_15DEG)*delta_lon
	elif(lat==2):
		delta_lon = (NTU_2_M * COS_25DEG)*delta_lon
	elif(lat==3):
		delta_lon = (NTU_2_M * COS_35DEG)*delta_lon
	elif(lat==4):
		delta_lon = (NTU_2_M * COS_45DEG)*delta_lon
	elif(lat==5):
		delta_lon = (NTU_2_M * COS_55DEG)*delta_lon
	elif(lat==6):
		delta_lon = (NTU_2_M * COS_65DEG)*delta_lon
	elif(lat==7):
		delta_lon = (NTU_2_M * COS_75DEG)*delta_lon
	elif(lat==8):
		delta_lon = (NTU_2_M * COS_85DEG)*delta_lon
	else:
		return DBL_MAX
	return math.sqrt(delta_lon * delta_lon + delta_lat * delta_lat)

#http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def calc_distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r
