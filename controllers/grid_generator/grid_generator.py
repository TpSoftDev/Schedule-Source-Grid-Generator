# This file is responsible for generating time grids for a new hires class schedule
# The programatic equivilant to manually highlighting a students grid on paper
# Generates a new time table in the project directory

#We nee
import datetime

from openpyxl import load_workbook
from datetime import time

from openpyxl.styles import PatternFill
import os
import sys
from controllers.grid_generator.helper_classes.availability_parser import parse_availability

from openpyxl import load_workbook
from controllers.grid_generator.helper_classes.availability_parser import parse_availability

FINAL_HOUR_IN_GRID = 22
NUM_INTERVALS_PER_HOUR = 6


def fill_in_day(ws, dayId, availableRanges):
    # Sunday (ID = 1) starts at row 3 (1 + 2) = 3
    rowNum = dayId + 2
    colNum = 2
    color = 'FFFF00'

    for hour in range(6, FINAL_HOUR_IN_GRID):
        minute = 5
        while(minute <= 60):
            #Flag for if we are on hour 60, hour minutes get reset so we must break the loop
            edge_case_found = 0

            #When at the last minute of hour h, we treat it as hour=h+1, minute = 0
            if minute == 60:
                minute = 0
                newHour = hour + 1
                currentTime = datetime.time(hour=newHour, minute=minute)
                edge_case_found = 1

            else:
                currentTime = datetime.time(hour=hour, minute=minute)

            if (not is_available(currentTime, availableRanges)):
                fill_in_cell(ws, rowNum, colNum, color)

            if (edge_case_found == 1):
                print("FOUND EDGE CASE")
                break

            minute += 5
            colNum += 1


#TODO Document
def is_available(currentTime, availableRanges):
    print()
    for range in availableRanges:
        if currentTime < range["end_time"] and currentTime > range["start_time"]:
            return True

    return False

#TODO document
def fill_in_cell(ws, row, col, color):
    # Create a PatternFill object with the given color (in hexadecimal format)
    fill_color = PatternFill(start_color=color, end_color=color, fill_type="solid")

    # Use the row and column to get the cell and apply the fill color
    ws.cell(row=row, column=col).fill = fill_color




def main():

    wb = load_workbook("Timetable template.xlsx")
    ws = wb.active

    avail = parse_availability("170601496")
    monday = avail[1]
    print(monday)
    fill_in_day(ws, 2, monday["DayRanges"])

    wb.save("Timetable template.xlsx")




# Run the main program when gridGenerator is executed
if __name__ == "__main__":
    main()