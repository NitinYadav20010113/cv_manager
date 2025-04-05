from datetime import datetime
import logging
from datetime import datetime
from pytz import timezone
from dateutil.parser import parse
import re
from datetime import datetime
import datefinder
# Define the time zone for IST
IST = timezone('Asia/Kolkata')

def date_checker(date):
    current_date = datetime.now().date()
    if date!=None:
        date = datetime.strptime(date,"%Y-%m-%d").date()
        if date>current_date:
            return False
        return True
    else:
        return True
    
    
    

class ISTFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        # Convert to IST
        record_time = datetime.fromtimestamp(record.created, IST)
        if datefmt:
            return record_time.strftime(datefmt)
        else:
            # Default format
            return record_time.strftime('%Y-%m-%d %H:%M:%S')
        
# This function creates the logger for us
def logger_creater(type):
    logger_name = f"ISTLogger_{type}"  # Unique name for each logger
    logger = logging.getLogger(logger_name)
    # logger = logging.getLogger("ISTLogger")
    logger.setLevel(logging.DEBUG)

    # Console handler with IST timestamp formatter
    if type=="model_logger":
        console_handler = logging.FileHandler('model_logger.log')
    elif type=="insert_logger":
        console_handler = logging.FileHandler('insert_logger.log')
        
    formatter = ISTFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    return logger





# def reformat_date(date_string, output_format="%Y-%m-%d"):
#     try:

#         date=re.search('present|current|till',date_string.lower())
#         if date:
#             current_date = datetime.now()
#             formatted_date = current_date.strftime("%Y-%m-%d")
#             return formatted_date
#         # Parse the date from the string with default as None
#         date_obj = parse(date_string, default=None)
        
#         # If the day isn't explicitly provided, set it to the first of the month
#         if date_obj.day != 1:
#             date_obj = date_obj.replace(day=1)
        
#         # Format the parsed date into the desired format
#         formatted_date = date_obj.strftime(output_format)
#         return formatted_date
#     except ValueError:
#         # Handle the case where no date is found in the string
#         return None
    
    
    
    
# def new_reformer_date(date_string):
#     try:
#         matches = datefinder.find_dates(date_string)
#         dates = []
#         for match in matches:
#             # If the day is missing, set it to 1
#             if match.day == datetime.now().day:  # This means the day is not parsed correctly
#                 match = match.replace(day=1)
#             dates.append(match)
            
#         date=re.search('present|current|till',date_string.lower())
#         if date:
#             current_date = datetime.now()
#             formatted_date = current_date.strftime("%Y-%m-%d")
#             dates.append(formatted_date)
#         return dates

#     except:
#         return None
    
    


months_full = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12
}

months_abb = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12
}

def format_date(dates):
    dates=re.sub('([,.\'\’]|th|rd|from|since)',' ',dates.lower())
    dates=dates.strip()
    print('The date is',dates)
    check=re.split('\sto\s+',dates)
    if len(check)!=2:
        if dates.count('-')==1:
            dates=dates.split('-')
        elif dates.count('–')==1:
            dates=dates.split('–')
    else:
        dates=check
        
    output_dates=[]
    if len(dates)==2:
        for date in dates:
            day=None
            month=None
            year=None
            current_date=re.search('present|current|till|till now|till date',date.lower())
            if current_date:
                india_timezone = timezone("Asia/Kolkata")
                current_time_in_india = datetime.now(india_timezone)
                formatted_date = current_time_in_india.strftime("%Y-%m-%d")
                print('The date is',formatted_date)
                output_dates.append(formatted_date)
            else:
                date=date.strip()
                day= re.search(r"^\d{1,2}(?!\d)",date)
                if day:
                    date=date[day.end():]
                    day=day.group()
                    day=int(day)
                    if day>31 or day<1:
                        day=None
                    if day:
                        if day<10:
                            day=f'0{day}'
                        else:
                            day=str(day)
                month_pattern = r"\b(" + "|".join(list(months_full.keys())+list(months_abb.keys())) + r")\b"
                month_pattern=r"\b(\d{1,2}(?!\d)\b|"+month_pattern+")"

                # print('The month pattern is ',month_pattern)
                month_search=re.search(month_pattern,date)
                if month_search:
                    month=month_search.group()
                    if month in months_full:
                        month=months_full[month]
                    elif month in months_abb:
                        month=months_abb[month]
                    else:
                        month=int(month)
                    if month>12 or month<1:
                        month=None
                    else:
                        if month<10:
                            month=f'0{month}'
                        else:
                            month=str(month)
                        date=date[month_search.end():]
                
                year_search=re.search(r'\b(\d{2}|\d{4})\b',date)
                if year_search:
                    year=year_search.group()
                    if len(year)==2:
                        current_year = datetime.now().year
                        last_two_digits = current_year % 100
                        if int(year)>last_two_digits:
                            year=f'19{year}'
                        else:
                            year=f'20{year}'
                            
                
                if day and not month and not year:
                    year=day
                if day and not month:
                    month=day
                    day=None
                    
                if year is None:
                    output_dates.append(None)
                    continue
                if month is None:
                    if len(year)==4:
                        output_dates.append(f'{year}-01-01')
                        continue
                    if len(year)==2:
                        pass
                if day is None:
                    output_dates.append(f'{year}-{month}-01')
                    continue
                else:
                    output_dates.append(f'{year}-{month}-{day}')

                print('The day is ',day)
                print('The month is',month)
                print('The year is',year)
                
                

    return output_dates
