from datetime import datetime
import csv

def time_to_decimal(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours + minutes / 60

def analyze_employee_data(file_path):
    employees = {} 
    output = {}
    consecutive_days_threshold = 7
    min_hours_between_shifts = 1
    max_hours_single_shift = 14
    max_hours_between_shifts = 10

    with open(file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            employee_name = row['Employee Name'] + ' - ' + row['File Number']
            shift_start = row['Time']
            shift_end = row['Time Out']

            if shift_end == '' or shift_start == '':
                continue
            shift_start_time = datetime.strptime(shift_start, '%m/%d/%Y %I:%M %p')
            shift_end_time = datetime.strptime(shift_end, '%m/%d/%Y %I:%M %p')

            timecard_hours_str = row['Timecard Hours (as Time)']
            shift_duration = time_to_decimal(timecard_hours_str)

            # Check for consecutive workdays
            if employee_name in employees:
                previous_shift_end = employees[employee_name][-1][1]
                if (shift_start_time - previous_shift_end).days == 1:
                    employees[employee_name].append((shift_start_time, shift_end_time, shift_duration))
                else:
                    employees[employee_name] = [(shift_start_time, shift_end_time, shift_duration)]
            else:
                employees[employee_name] = [(shift_start_time, shift_end_time, shift_duration)]

            # Check for shifts with less than 10 hours but greater than 1 hour between them
            if employees[employee_name]:
                last_shift_end = employees[employee_name][-1][1]
                hours_between_shifts = (last_shift_end - shift_start_time).total_seconds() / 3600
                
                if min_hours_between_shifts < hours_between_shifts < max_hours_between_shifts:
                    if 'shift_time_gap_between_threshold' in output:
                        if employee_name not in output['shift_time_gap_between_threshold']:
                            output['shift_time_gap_between_threshold'].append(employee_name)
                    else:
                        output['shift_time_gap_between_threshold'] = [employee_name]

            # Check for shifts longer than 14 hours
            if shift_duration > max_hours_single_shift:
                if 'shift_longer_than_threshold' in output:
                    if employee_name not in output['shift_longer_than_threshold']:
                            output['shift_longer_than_threshold'].append(employee_name)
                else:
                    output['shift_longer_than_threshold'] = [employee_name]

            # Check for employees who worked for 7 consecutive days
            if len(employees[employee_name]) == consecutive_days_threshold:
                if 'worked_consecutively_till_threshold' in output:
                    if employee_name not in output['worked_consecutively_till_threshold']:
                            output['worked_consecutively_till_threshold'].append(employee_name)
                else:
                    output['worked_consecutively_till_threshold'] = [employee_name]
        return output

if __name__ == "__main__":
    file_path = "Assignment_Timecard.csv"
    output = analyze_employee_data(file_path)
    if output is not None:
        for key, value in output.items():
            print('--------------------------------',key.replace("_"," ").upper(),'START','--------------------------------')
            print('\n'.join(value))
            print('--------------------------------',key.replace("_"," ").upper(), 'END','--------------------------------')
