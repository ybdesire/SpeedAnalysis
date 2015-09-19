from CalcDistance import calc_distance
from openpyxl import load_workbook, Workbook
from datetime import datetime

DIST_THRESHOLD = 3 # 3KM
ZERO_SPEED_THRESHOLD = 10 #10KM/H. car stop speed cannot be real 0.

class DataCalc:
	def __init__(self, file_path, sheet_name='vehicle_gps_log'):
		self.wb = load_workbook(file_path)
		self.ws = self.wb[sheet_name]
		self.column_length = 0
		
	def __get_column_length(self):	
		if(self.column_length == 0):
			self.column_length = self.ws.get_highest_row()
		return self.column_length
	
	def go_through_all_gps_data_and_get_length_src(self):
		self.__get_column_length()
		for i in range(self.column_length):
			if(i>2):
				current_gps_stat = self.ws['H' + str(i)].value
				pre_gps_stat = self.ws['H' + str(i-1)].value
				if(current_gps_stat!='V' and pre_gps_stat!='V'):
					current_lon = float(self.ws['D' + str(i)].value)
					current_lat = float(self.ws['E' + str(i)].value)				
					pre_lon = float(self.ws['D' + str(i-1)].value)
					pre_lat = float(self.ws['E' + str(i-1)].value)
					dist = calc_distance(pre_lon, pre_lat, current_lon, current_lat)
					if(dist>3):
						print('{0}: {1}'.format(i, dist))
						
	def go_through_all_gps_data_and_get_length_result(self):
		self.__get_column_length()
		for i in range(self.column_length):
			if(i>2):
				current_gps_stat = self.ws['D' + str(i)].value
				pre_gps_stat = self.ws['D' + str(i-1)].value
				if(current_gps_stat!='V' and pre_gps_stat!='V'):
					current_lon = float(self.ws['A' + str(i)].value)
					current_lat = float(self.ws['B' + str(i)].value)				
					pre_lon = float(self.ws['A' + str(i-1)].value)
					pre_lat = float(self.ws['B' + str(i-1)].value)
					dist = calc_distance(pre_lon, pre_lat, current_lon, current_lat)
					if(dist>3):
						print('{0}: {1}'.format(i, dist))
						
	def filter_invalid_data_and_create_file(self, result_file_path):
		self.__get_column_length()
		result_wb = Workbook()
		result_ws = result_wb.active
		j=1
		for i in range(self.column_length+1):
			if(i>0):
				if(i==1):
					result_ws['A'+str(j)] = self.ws['D' + str(i)].value
					result_ws['B'+str(j)] = self.ws['E' + str(i)].value
					result_ws['C'+str(j)] = self.ws['F' + str(i)].value
					result_ws['D'+str(j)] = self.ws['H' + str(i)].value
					result_ws['E'+str(j)] = self.ws['I' + str(i)].value
				elif(i>1):
					current_gps_stat = self.ws['H' + str(i)].value
					current_time = datetime.strptime(str(self.ws['I' + str(i)].value), '%Y-%m-%d %H:%M:%S')
					if(current_time.year==1999 or current_gps_stat=='V'):
						continue
					else:
						result_ws['A'+str(j)] = self.ws['D' + str(i)].value
						result_ws['B'+str(j)] = self.ws['E' + str(i)].value
						result_ws['C'+str(j)] = self.ws['F' + str(i)].value
						result_ws['D'+str(j)] = self.ws['H' + str(i)].value
						result_ws['E'+str(j)] = self.ws['I' + str(i)].value
				j = j + 1
		result_wb.save(result_file_path)
		
	def get_car_stop_point(self):
		self.__get_column_length();
		speed_zero_index_list = []
		for i in range(self.column_length):
			if(i>2):
				current_gps_stat = self.ws['H' + str(i)].value
				pre_gps_stat = self.ws['H' + str(i-1)].value
				if(current_gps_stat!='V' and pre_gps_stat!='V'):
					current_speed = int(self.ws['F' + str(i)].value)
					if(current_speed<=ZERO_SPEED_THRESHOLD):
						speed_zero_index_list.append(i)
		return speed_zero_index_list
		
	def get_car_stop_area(self, speed_zero_index_list):
		icount = 0
		car_stop_area = {}
		car_stop_list = []
		for i in range(len(speed_zero_index_list)):
			if(i<len(speed_zero_index_list)-1):
				if(abs(speed_zero_index_list[i]-speed_zero_index_list[i+1])==1):#continues points can be a possible area
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
		valid_stop_area = car_stop_area
		invalid_key_list = []
		for key in valid_stop_area:
			value = valid_stop_area[key]
			zero_speed_exist = False
			for value_item in value:
				speed = int(self.ws['F' + str(value_item)].value)
				if(speed==0):
					zero_speed_exist = True
			if (not zero_speed_exist or len(value)==1 or not self.__is_valid_dist_interval(value)):
				invalid_key_list.append(key)
		#remove invalid stop area		
		for k in invalid_key_list:
			del(valid_stop_area[k])
		return 	valid_stop_area