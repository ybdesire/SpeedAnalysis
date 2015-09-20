from CalcDistance import calc_distance
from openpyxl import load_workbook, Workbook
from datetime import datetime
import math

AREA_DIST_THRESHOLD = 0.3 # 0.3KM
ZERO_SPEED_THRESHOLD = 10 #10KM/H. car stop speed cannot be real 0.
DIST_THRESHOLD = 0.3 # 0.3KM

class DataCalc:
	def __init__(self, file_path, sheet_name='vehicle_gps_log'):
		self.wb = load_workbook(file_path)
		self.ws = self.wb[sheet_name]
		self.column_length = 0
		
	def __get_column_length(self):	
		if(self.column_length == 0):
			self.column_length = self.ws.get_highest_row()
		return self.column_length
								
	def get_car_stop_point(self):#return the row number for those whose speed < ZERO_SPEED_THRESHOLD
		self.__get_column_length()
		speed_zero_index_list = []
		for i in range(self.column_length):
			if(i>2):
				current_gps_stat = self.ws['H' + str(i)].value
				pre_gps_stat = self.ws['H' + str(i-1)].value
				current_time = datetime.strptime(str(self.ws['I' + str(i)].value), '%Y-%m-%d %H:%M:%S')
				if(current_gps_stat!='V' and pre_gps_stat!='V' and current_time.year!=1999):
					current_speed = int(self.ws['F' + str(i)].value)
					if(current_speed<=ZERO_SPEED_THRESHOLD):
						speed_zero_index_list.append(i)
			elif(i==2):
				current_gps_stat = self.ws['H' + str(i)].value
				current_time = datetime.strptime(str(self.ws['I' + str(i)].value), '%Y-%m-%d %H:%M:%S')
				if(current_gps_stat!='V' and current_time.year!=1999):
					current_speed = int(self.ws['F' + str(i)].value)
					if(current_speed<=ZERO_SPEED_THRESHOLD):
						speed_zero_index_list.append(i)
		return speed_zero_index_list
		
	def get_car_stop_area(self, speed_zero_index_list):#return the car stop area row lists
		icount = 0
		car_stop_area = {}
		car_stop_list = []
		for i in range(len(speed_zero_index_list)):
			if(i<len(speed_zero_index_list)-1):
				lon1 = float(self.ws['D' + str(speed_zero_index_list[i])].value)
				lat1 = float(self.ws['E' + str(speed_zero_index_list[i])].value)
				lon2 = float(self.ws['D' + str(speed_zero_index_list[i+1])].value)
				lat2 = float(self.ws['E' + str(speed_zero_index_list[i+1])].value)
				dist = calc_distance(lon1, lat1, lon2, lat2)

				if(dist<AREA_DIST_THRESHOLD):
					car_stop_list.append(speed_zero_index_list[i])
				else:
					car_stop_list.append(speed_zero_index_list[i])
					car_stop_area[icount] = car_stop_list
					car_stop_list = []
					icount = icount + 1
		return car_stop_area
		
	def __is_valid_dist_interval(self, index_list):#if max distance bigger than 3km
		max_dist = 0
		for i in index_list:
			for j in index_list:
				lon1 = float(self.ws['D' + str(i)].value)
				lat1 = float(self.ws['E' + str(i)].value)
				lon2 = float(self.ws['D' + str(j)].value)
				lat2 = float(self.ws['E' + str(j)].value)
				dist = calc_distance(lon1, lat1, lon2, lat2)
				if(dist>max_dist):
					max_dist = dist
		if(max_dist>DIST_THRESHOLD):
			return False
		
		return True
		
	def get_valid_stop_area(self, car_stop_area):
		len_area_temp = len(car_stop_area)
		valid_stop_area_temp = car_stop_area
		invalid_key_list = []
		for key in valid_stop_area_temp:
			value = valid_stop_area_temp[key]
			zero_speed_exist = False
			for value_item in value:
				speed = int(self.ws['F' + str(value_item)].value)
				if(speed==0):
					zero_speed_exist = True
			if (not zero_speed_exist or len(value)==1 or not self.__is_valid_dist_interval(value)):
				invalid_key_list.append(key)
		#remove invalid stop area		
		for k in invalid_key_list:
			del(valid_stop_area_temp[k])
		#sort the key from 1 to n
		valid_stop_area = {}
		j = 0
		for i in range(len_area_temp):
			if i in valid_stop_area_temp:
				valid_stop_area[j] = valid_stop_area_temp[i]
				j = j+1
			
		return 	valid_stop_area

	def get_stop_lon_lat(self, valid_stop_area):
		stop_lon_lat = {}
		for i in range(len(valid_stop_area)):
			stop_index = valid_stop_area[i][0]
			lon = float(self.ws['D' + str(stop_index)].value)
			lat = float(self.ws['E' + str(stop_index)].value)
			stop_lon_lat[i] = [lon, lat]
		return stop_lon_lat

	def get_stop_start_time(self, valid_stop_area):
		stop_time = {}
		for i in range(len(valid_stop_area)):
			stop_index = valid_stop_area[i][0]
			str_time = str(self.ws['I' + str(stop_index)].value)
			stop_time[i] = str_time
			
		return stop_time
		
	def get_stop_end_time(self, valid_stop_area):
		stop_time = {}
		for i in range(len(valid_stop_area)):
			length = len(valid_stop_area[i])
			stop_index = valid_stop_area[i][length-1]
			str_time = str(self.ws['I' + str(stop_index)].value)
			stop_time[i] = str_time
			
		return stop_time
	
	def get_stop_time_interval(self, valid_stop_area):
		stop_interval_dict = {}
		for i in range(len(valid_stop_area)):
			length = len(valid_stop_area[i])
			start_index = valid_stop_area[i][0]
			end_index = valid_stop_area[i][length-1]
			start_time = datetime.strptime(str(self.ws['I' + str(start_index)].value), '%Y-%m-%d %H:%M:%S')
			end_time = datetime.strptime(str(self.ws['I' + str(end_index)].value), '%Y-%m-%d %H:%M:%S')
			stop_interval_dict[i] = (end_time-start_time).seconds/60
		return stop_interval_dict
	
	def get_driving_area(self, valid_stop_area):
		self.__get_column_length()
		driving_area = {}
		j = 0
		for i in range(len(valid_stop_area)+1):
			if(i==0):
				car_stop_start_index = valid_stop_area[i][0]
				if(car_stop_start_index>2):
					car_driving_start_index = 2
					car_driving_end_index = car_stop_start_index - 1
				else:
					continue
			elif(i==len(valid_stop_area)):
				length_pre = len(valid_stop_area[i-1])
				car_stop_end_index = valid_stop_area[i-1][length_pre-1]
				if(car_stop_end_index<self.column_length-1):
					car_driving_start_index = car_stop_end_index + 1
				else:
					car_driving_start_index = car_stop_end_index
				car_driving_end_index = self.column_length
			else:
				length_pre = len(valid_stop_area[i-1])
				car_driving_start_index = valid_stop_area[i-1][length_pre-1] + 1
				car_driving_end_index = valid_stop_area[i][0] - 1
			driving_area[j] = [car_driving_start_index, car_driving_end_index]
			j = j+1
		return driving_area
	
	def __is_valid_data(self, index):
		gps_stat = self.ws['H' + str(index)].value
		data_time = datetime.strptime(str(self.ws['I' + str(index)].value), '%Y-%m-%d %H:%M:%S')
		if(index>1 and gps_stat!='V' and data_time.year!=1999):
			return True
		else:
			return False

	def get_driving_ave_speed(self, driving_area):
		driving_area_ave_speed = {}
		for i in range(len(driving_area)):
			j = driving_area[i][0]
			speed_sum = 0
			count = 0
			while(j<=driving_area[i][1]):
				if(self.__is_valid_data(j)):
					speed_sum = speed_sum + int(self.ws['F' + str(j)].value)
					count = count + 1
				j = j+1
			driving_area_ave_speed[i] = speed_sum/count
		return driving_area_ave_speed
	
	def get_driving_time_stat(self, driving_area):
		driving_area_time = {}
		for i in range(len(driving_area)):
			length = len(driving_area[i])
			start_index = driving_area[i][0]
			end_index = driving_area[i][length-1]
			start_time = str(self.ws['I' + str(start_index)].value)			
			end_time = str(self.ws['I' + str(end_index)].value)
			interval = (datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')-datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')).seconds/60
			driving_area_time[i] = [start_time, end_time, interval]
		return driving_area_time
		
	def get_driving_lon_lat(self, driving_area):
		driving_lon_lat = {}
		for i in range(len(driving_area)):
			length = len(driving_area[i])
			start_index = driving_area[i][0]
			end_index = driving_area[i][length-1]
			lon_start = float(self.ws['D' + str(start_index)].value)
			lat_start = float(self.ws['E' + str(start_index)].value)
			lon_end = float(self.ws['D' + str(end_index)].value)
			lat_end = float(self.ws['E' + str(end_index)].value)
			driving_lon_lat[i] = [lon_start, lat_start, lon_end, lat_end]
		return driving_lon_lat
	
	def get_speed_variance(self, driving_area, center_value):
		speed_variance = {}
		for i in range(len(driving_area)):
			j = driving_area[i][0]
			speed_sum = 0
			count = 0
			while(j<=driving_area[i][1]):
				if(self.__is_valid_data(j)):
					sub_speed_center = int(self.ws['F' + str(j)].value) - center_value
					speed_sum = speed_sum + sub_speed_center*sub_speed_center
					count = count + 1
				j = j+1
			speed_variance[i] = math.sqrt(speed_sum/count)
		return speed_variance
