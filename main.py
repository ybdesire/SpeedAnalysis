import timeit
from DataCalc import DataCalc
from CalcDistance import calc_distance

def test():
	distance = calc_distance(121.306216, 31.353354, 121.185040, 31.405485)
	print(distance)#km
	
	
FILENAME = 'data-20150917.xlsx'
	
def main():
	data_calc_mgr = DataCalc(FILENAME, 'vehicle_gps_log')
	speed_zero_index_list = data_calc_mgr.get_car_stop_point()
	car_stop_area = data_calc_mgr.get_car_stop_area(speed_zero_index_list)
	valid_stop_area = data_calc_mgr.get_valid_stop_area(car_stop_area)
	
	stop_lon_lat = data_calc_mgr.get_stop_lon_lat(valid_stop_area)
	print('\ncar stop lon lat:')
	print_order_dict(stop_lon_lat)
	
	car_stop_start_time = data_calc_mgr.get_stop_start_time(valid_stop_area)
	print('\ncar stop start time:')
	print_order_dict(car_stop_start_time)
	
	car_stop_end_time  = data_calc_mgr.get_stop_end_time(valid_stop_area)
	print('\ncar stop end time:')
	print_order_dict(car_stop_end_time)
	
	car_stop_time_intervel = data_calc_mgr.get_stop_time_interval(valid_stop_area)
	print('\ncar stop time intervel:')
	print_order_dict(car_stop_time_intervel)
	
	car_driving_area = data_calc_mgr.get_driving_area(valid_stop_area)
	print('\ncar driving area:')
	print_order_dict(car_driving_area)
	
	driving_area_ave_speed = data_calc_mgr.get_driving_ave_speed(car_driving_area)
	print('\ncar driving average speed:')
	print_order_dict(driving_area_ave_speed)	
	
	car_driving_time_stat = data_calc_mgr.get_driving_time_stat(car_driving_area)
	print('\ncar driving start-time, end-time, intervel:')
	print_order_dict(car_driving_time_stat)	

	car_driving_lon_lat = data_calc_mgr.get_driving_lon_lat(car_driving_area)
	print('\ncar driving start-lon lat, end-lon lat')
	print_order_dict(car_driving_lon_lat)	

	speed_variance_70 = data_calc_mgr.get_speed_variance(car_driving_area, 70)
	speed_variance_75 = data_calc_mgr.get_speed_variance(car_driving_area, 75)
	speed_variance_80 = data_calc_mgr.get_speed_variance(car_driving_area, 80)
	speed_variance_85 = data_calc_mgr.get_speed_variance(car_driving_area, 85)
	speed_variance_90 = data_calc_mgr.get_speed_variance(car_driving_area, 90)
	speed_variance_95 = data_calc_mgr.get_speed_variance(car_driving_area, 95)
	
	

	
def print_order_dict(data):
	for i in range(len(data)):
		print(data[i])
	
if __name__=='__main__':
	start = timeit.default_timer()
	main()
	stop = timeit.default_timer()
	print('------ running time: {0} s ------'.format(stop-start))	
	
