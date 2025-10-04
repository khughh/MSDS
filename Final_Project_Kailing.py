import csv
from tkinter import Tk, Canvas
import numpy as np
import math

#-------------------------------------------------------------------------
# Constants for visualization pixel values
#-------------------------------------------------------------------------
GUTTER = 60   # space around chart
MARGIN = 60   # space between bars
CHART_WIDTH = 1000
CHART_HEIGHT = 400
CANVAS_WIDTH = CHART_WIDTH + GUTTER * 3
CANVAS_HEIGHT = CHART_HEIGHT + GUTTER * 3
BAR_COUNT = 3  # show data per Mortgage Class and aggregated value

#-------------------------------------------------------------------------
# Safe type conversion functions
#-------------------------------------------------------------------------
def to_int(value : str, default_value = 0):
    '''
    Convert string to int safely.
    '''
    if value.strip() == '': return default_value  # missing value
    try:
        return int(value.strip())
    except:
        print('Bad integer value:', value)
        return default_value


def to_float(value : str, default_value = 0.0):
    '''
    Convert string to float safely.
    '''
    if value.strip() == '': return default_value  # missing value
    try:
        return float(value.strip())
    except:
        print('Bad float value:', value)
        return default_value


#-------------------------------------------------------------------------
# Functions to map data values to pixel dimensions
# FIXME: It would be better to auto-scale based on data values
#-------------------------------------------------------------------------
def mortgage_amt_to_height(mortgage_amt : float):
    '''
    Convert outstanding mortgage amount to pixel height on our graph
    '''
    return (mortgage_amt / 1000) * CHART_HEIGHT

def mthly_pmt_to_height(mthly_pmt : float):
    '''
    Convert monthly principal payment to pixel height
    '''
    return (mthly_pmt / 1000) * CHART_HEIGHT

def avg_int_rate_to_height(avg_int_rate : float):
    '''
    Convert avg_int_rate to pixel height
    '''
    return (avg_int_rate / 1000) * CHART_HEIGHT

#-------------------------------------------------------------------------
# Functions to draw bars in the visualization
#-------------------------------------------------------------------------
def draw_mortgage_amt_bar(canvas, x, width, mortgage_amt):
    height = mortgage_amt_to_height(mortgage_amt)
    y = CHART_HEIGHT + GUTTER - height
    canvas.create_rectangle(x, y, x + width, y + height, fill = 'pink')

def draw_mthly_pmt_bar(canvas, x, width, mthly_pmt):
    height = mthly_pmt_to_height(mthly_pmt)
    y = CHART_HEIGHT + GUTTER - height
    canvas.create_rectangle(x, y, x + width, y + height, fill = '#2299cc')

def draw_avg_int_rate_bar(canvas, x, width, avg_int_rate):
    height = avg_int_rate_to_height(avg_int_rate)
    y = CHART_HEIGHT + GUTTER - height
    canvas.create_rectangle(x, y, x + width, y + height, fill = 'green')


#-------------------------------------------------------------------------
def load_data_row(row):
    '''
    This function takes a line of the source CSV file as a list.
    It returns a dictionary with the keys as column names and the
    values as the actual data.
    '''
    AMMORT       = to_float(row[19])   # mortgage amount?
    REFI   = to_float(row[20].replace("'", ""))  # refinance?
    MORTCLASS = to_float(row[21].replace("'", "")) # mortgage class
    PMTONLY = to_float(row[24].replace("'", "")) # payment
    LOANTYPE = to_float(row[33].replace("'", ""))
    MISCPMT = to_float(row[34].replace("'", ""))  
    PMTFREQ = to_float(row[32].replace("'", ""))
    PMTAMT = to_float(row[35].replace("'", ""))
    INTRATE = to_float(row[36].replace("'", ""))
    
    return {
        'Mortgage_Amount' : AMMORT,
        '#_of_Refinances'  : REFI,
        'Mortgage_Class' : MORTCLASS,
        'Pmt_Only' : PMTONLY,
        'Pmt_Freq' : PMTFREQ,
        'Actual_Pmt_Amt' : PMTAMT,
        'Interest_Rate' : INTRATE
    }

#-------------------------------------------------------------------------
# Draw legend
#-------------------------------------------------------------------------
def draw_legend(canvas):
    canvas.create_rectangle(
        GUTTER + CHART_WIDTH - 300, GUTTER + MARGIN,
        GUTTER + CHART_WIDTH - 280, GUTTER + MARGIN + 20,
        fill = 'pink')
    canvas.create_text(
        GUTTER + CHART_WIDTH - 270, GUTTER + MARGIN,
        text = 'Outstanding Mortgage Amount per Mortgage Class', anchor = 'nw')

    canvas.create_rectangle(
        GUTTER + CHART_WIDTH - 300, GUTTER + MARGIN + 30,
        GUTTER + CHART_WIDTH - 280, GUTTER + MARGIN + 50,
        fill = '#2299cc')
    canvas.create_text(
        GUTTER + CHART_WIDTH - 270, GUTTER + MARGIN + 30,
        text = 'Monthly Payment per Mortgage Class', anchor = 'nw')

    canvas.create_rectangle(
        GUTTER + CHART_WIDTH - 300, GUTTER + MARGIN + 60,
        GUTTER + CHART_WIDTH - 280, GUTTER + MARGIN + 80,
        fill = 'green')
    canvas.create_text(
        GUTTER + CHART_WIDTH - 270, GUTTER + MARGIN + 60,
        text = 'Average Interest Rate per Mortgage Class', anchor = 'nw')

def draw_data_bars(canvas, mortgage_classes):
    x = GUTTER + MARGIN
    count = 0  # only include the highest emitting zip codes

    bar_width = ((CHART_WIDTH - MARGIN) / BAR_COUNT) - MARGIN

    print('sorted keys = ', sorted(mortgage_classes.keys()));
    # sorted by value descending instead of by key
    #for key in sorted(mortgage_classes, key=mortgage_classes.get, reverse = True):
    for key in sorted(mortgage_classes.keys()):
        if key != 0:

            bar_height = math.log10(max(mortgage_classes[key][0], 1)) * 100
            draw_mortgage_amt_bar(canvas, x, bar_width / 3, bar_height)
            val_comma = f'{round(mortgage_classes[key][0]):,}'
            canvas.create_text(x + bar_width / 6, CHART_HEIGHT - 80, text=chr(36)+val_comma, fill="black", font='Helvetica 8')
            x += bar_width / 3

            x_text = x;

            bar_height = math.log10(max(mortgage_classes[key][1], 1)) * 100
            draw_mthly_pmt_bar(canvas, x, bar_width / 3, bar_height)
            val_comma = f'{round(mortgage_classes[key][1]):,}'
            canvas.create_text(x + bar_width / 6, CHART_HEIGHT - 60, text=chr(36)+val_comma, fill="black", font='Helvetica 8')
            x += bar_width / 3

     #       canvas.create_text(x, CHART_HEIGHT + 44, text=key, fill="black", font='Helvetica 14')

            draw_avg_int_rate_bar(canvas, x, bar_width / 3, mortgage_classes[key][2])
            canvas.create_text(x + bar_width / 6, CHART_HEIGHT - 40, text=(round(mortgage_classes[key][2]/100, 2), '%'), fill="black", font='Helvetica 8')
            x += bar_width / 3

            # draw mortgage class
            canvas.create_text(x_text, CHART_HEIGHT + 80, text=key, fill="black", font='Helvetica 14')

            x += MARGIN

            count += 1
            if count >= BAR_COUNT: break


#-------------------------------------------------------------------------
# Open data file and create a list of data rows
#-------------------------------------------------------------------------

file = open('C:/lulu/Kailing/Python/mortgage.csv')
type(file)
#next(file)  # skip header row

data_reader = csv.reader(file)
header = []
header = next(data_reader)

dataset = [ ]
for row in data_reader:
    fields = load_data_row(row)
    dataset.append(fields)

mortgages_by_class = { }
row = 0
num_rows_by_class = np.array([0, 0, 0, 0, 0, 0])
for values in dataset:
    row += 1
#    print('row: ', row)
#    print('values: ', values);
    mort_class = values['Mortgage_Class']
    num_rows_by_class[int(mort_class)] += 1
#    print('mort_class: ', mort_class);

    #
    mortgage_amt = max(0, values['Mortgage_Amount'])
    pmt_only = values['Pmt_Only']
    pmt_amount = values['Actual_Pmt_Amt']
    pmt_freq = values['Pmt_Freq']
    int_rate = values['Interest_Rate']  
    monthly_pmt = np.multiply(np.array(pmt_only), np.array(pmt_freq))

    #scaling up the interest rate by 100 to make it visible on the chart
    int_rate = int_rate * 100

    # if we haven't seen this mortgage class yet, add it to the dictionary
    if mort_class not in mortgages_by_class:
        mortgages_by_class[mort_class] = [ 0.0, 0.0, 0.0 ]

    mortgage_amt += mortgages_by_class[mort_class][0]
    monthly_pmt += mortgages_by_class[mort_class][1]
    int_rate += mortgages_by_class[mort_class][2]
    
    mortgages_by_class[mort_class] = [ round(mortgage_amt, 2), round(monthly_pmt, 2), round(int_rate, 2) ]
class_keys = mortgages_by_class.keys();

for class_key in class_keys:
    num_this_class = num_rows_by_class[int(class_key)];
    mortgages_by_class[class_key][2] = round(mortgages_by_class[class_key][2] / num_this_class, 4)

print(mortgages_by_class)


#-------------------------------------------------------------------------
# Create Tkinter window
#-------------------------------------------------------------------------
gui = Tk()
gui.title('Mortgage Data by Mortgage Classes')

canvas = Canvas(gui, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background='#cccccc')
canvas.pack()

canvas.create_rectangle(
    GUTTER, GUTTER,
    GUTTER + CHART_WIDTH, GUTTER + CHART_HEIGHT,
    fill = 'white', outline = 'black')


#-------------------------------------------------------------------------
# Create visualization
#-------------------------------------------------------------------------
draw_data_bars(canvas, mortgages_by_class)
draw_legend(canvas)

canvas.mainloop()


    
#file.close()
