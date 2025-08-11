from datetime import datetime, date, time

@staticmethod
def convert_to_db_datetime(date_time):
    dt_string = datetime.strptime(date_time, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    return dt_string

@staticmethod
def convert_from_db_datetime(date_time):
    dt_string = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M:%S')
    return dt_string

@staticmethod
def convert_from_db_date(date_time):
    dt_string = datetime.strptime(date_time, '%Y-%m-%d').strftime('%d/%m/%Y')
    return dt_string

@staticmethod
def db_datetime_to_date_only(date_time):
    dt_string = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
    return dt_string

@staticmethod
def uk_datetime():
    current_datetime = datetime.now()
    # convert to UK format dd/mm/YY H:M:S
    dt_string = current_datetime.strftime('%d/%m/%Y %H:%M:%S')
    return dt_string

@staticmethod
def uk_date():
    current_datetime = datetime.now()
    # convert to UK format dd/mm/YY
    dt_string = current_datetime.strftime("%d/%m/%Y")
    return dt_string

@staticmethod
def uk_datetime_filename():
    current_datetime = datetime.now()
    # Current date and time with hyphens (slashes not supported in filenames)
    dt_string = current_datetime.strftime("%d-%m-%Y %H%M%S")
    return dt_string

@staticmethod
def datetime_to_date(date_time):
    dt_string = date_time[0:11]
    return dt_string

