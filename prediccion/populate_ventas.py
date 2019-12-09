import openpyxl
import datetime
import matplotlib.pyplot as plt

from dateutil.relativedelta import relativedelta
from calendar import monthrange

from prediccion.models import RegistroVenta

from prediccion.func import populate_days, get_months, get_weeks

books_names = ['ventas_2015.xlsx', 'ventas_2016.xlsx', 'ventas_2017.xlsx', 'ventas_2018.xlsx', 'ventas_2019.xlsx']

def get_all_services(services):
    not_repeat = []
    for i in services:
        if not i in not_repeat:
            not_repeat.append(i)
    return not_repeat

def get_all_sales(array_books):
    all_dates_prices = []
    all_dates = []
    all_prices = []
    all_descriptions = []
    all_firms = []
    all_rucs = []

    for i in array_books:
        new_book = openpyxl.load_workbook(i, data_only=True)
        for j in new_book.sheetnames:
            sheet = new_book[j]

            for row in sheet.rows:
                if isinstance(row[2].value, datetime.datetime):
                    new_date = row[2].value                       
                    new_price = row[10].value
                    new_description = row[5].value
                    new_firm = row[3].value
                    new_ruc = row[4].value

                    all_dates_prices.append([new_date, new_price, new_description, new_firm, new_ruc])

    
    all_dates_prices.sort()

    for i in all_dates_prices:
        all_dates.append(i[0])
        all_prices.append(i[1])
        all_descriptions.append(i[2])
        all_firms.append(i[3])
        all_rucs.append(i[4])

    return all_dates, all_prices, all_descriptions, all_firms, all_rucs
    

def filter_for_service(all_data, value_filter, index_filter):
    filter_data = [[] for i in range(len(all_data))]
    for i in range(len(all_data[index_filter])):
        if all_data[index_filter][i]==value_filter:
            for j in range(len(filter_data)):
                filter_data[j].append(all_data[j][i])

    return filter_data

def populate_all_sales():
    date, price, description, firm, ruc = get_all_sales(books_names)
    
    all_services = get_all_services(description)

    data = [date, price, description, firm, ruc]

    for i in all_services:
        all_dates, all_prices, all_descriptions, all_firms, all_rucs = filter_for_service(data, i, 2)
        nn_dates, nn_prices, nn_descriptions, nn_firms, nn_rucs = populate_days(all_dates, all_prices, all_descriptions, all_firms, all_rucs)
        
        for j in range(len(nn_dates)):
            RegistroVenta.objects.create(fecha=nn_dates[j], precio=nn_prices[j], tipo=nn_descriptions[j], empresa=nn_firms[j], ruc=nn_rucs[j])

populate_all_sales()
