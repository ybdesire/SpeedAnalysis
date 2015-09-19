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
	print(valid_stop_area)
	
	
if __name__=='__main__':
	start = timeit.default_timer()
	main()
	stop = timeit.default_timer()
	print('------ running time: {0} s ------'.format(stop-start))	
	
