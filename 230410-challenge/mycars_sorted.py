#!/usr/bin/env python3

import json
import locale
import mygmails
import reports


def load_data(filename):
    """Loads the contents of filename as a JSON file.
    """
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


def format_car(car):
    """Given a car dictionary, returns a nicely formatted name.
    """
    return "{} {} ({})".format(car["car_make"], car["car_model"], car["car_year"])


def process_data(data):
    """Analyzes the data, looking for maximums.
    Returns a list of lines that summarize the information.
    """
    locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
    max_revenue = {"revenue": 0}
    max_sales = {"total_sales": 0}
    years_count = {}
    for item in data:
        item_price = locale.atof(item["price"].strip("$"))
        # Calculate the revenue generated by model
        item_revenue = item["total_sales"] * item_price
        if item_revenue > max_revenue["revenue"]:
            item["revenue"] = item_revenue
            max_revenue = item
        # handle max sales
        if item["total_sales"] > max_sales["total_sales"]:
            max_sales = item
        # handle most popular car_year
        if item["car"]["car_year"] in years_count:
            years_count[item["car"]["car_year"]] = {"count": years_count[item["car"]["car_year"]]["count"]+1, "total_sales": years_count[item["car"]["car_year"]]["total_sales"]+item["total_sales"]}
        else:
            years_count[item["car"]["car_year"]] = {"count": 1, "total_sales": item["total_sales"]}
    popular_year = sorted(years_count.items(),key=lambda x: x[1]["count"], reverse=True)[0]
    summary = ["The {} generated the most revenue: ${}".format(format_car(max_revenue["car"]), max_revenue["revenue"]),
        "The {} had the most sales: {}".format(format_car(max_revenue["car"]), max_sales["total_sales"]),
        "The most popular year was {} with {} sales.".format(popular_year[0],popular_year[1]["total_sales"])]
    return summary


def cars_dict_to_table(car_data):
    """Turns the data in car_data into a list of lists.
    """
    table_data = [["ID", "Car", "Price", "Total Sales"]]
    for item in car_data:
        table_data.append([item["id"], format_car(item["car"]), item["price"], item["total_sales"]])
    return table_data


def cars_sort_dict(in_data):
    """Merge sort `in_data` by total sales and return a new list.
    """
    middle = len(in_data)//2
    left = in_data[:middle]
    right = in_data[middle:]
    if len(left) > 1:
        left = cars_sort_dict(left)
    if len(right) > 1:
        right = cars_sort_dict(right)

    def merge_list(A, B):
        result = []
        N = len(A)
        M = len(B)
        i = 0
        j = 0
        while i < N and j < M:
            if A[i]["total_sales"] <= B[j]["total_sales"]:
                result.append(A[i])
                i += 1
            else:
                result.append(B[j])
                j += 1
        result += A[i:] + B[j:]
        return result
    
    return merge_list(left, right)


def bars_chart_list(in_data):
    list_length = len(in_data)
    bars_chart_length = 0
    if list_length <= 1:
        text = "Lenth of the cars list for bars chart have to be more than zero"
        print(text)
        return text
    if list_length >= 11:
        bars_chart_length = 10
    else:
        bars_chart_length = list_length
    out_list = in_data[ list_length - bars_chart_length : ]
    return out_list


def main():
    """Processes the JSON data and generates a full report out of it.
    """
    data = load_data("car_sales.json")
    summary = process_data(data)
    print(summary)
    sorted_data = cars_sort_dict(data)
    table_data = cars_dict_to_table(sorted_data)
    # diagram = diagram_create(table_data)
    pdf_data = {}
    pdf_data['filename'] = 'mycars.pdf'
    pdf_data['title'] = "Sales summary for last month"
    pdf_data['summary'] = "<br/>".join(summary)
    pdf_data['table'] = table_data
    pdf_data['bars_chart'] = bars_chart_list(table_data)
    pdf_data['chart_legend'] = "Profit from the sale of 10 most popular models"
    pdf_data['chart_note'] = "(see 10 last lines of the table)"
    reports.generate(pdf_data)

    # sending the PDF report as an email attachment
    email_data = {}
    email_data['sender'] = "peregarien@gmail.com"
    email_data['receiver'] = "i0638464000@gmail.com"
    email_data['subject'] = "Sales Summary Challenge"
    email_data['body'] = "\n".join(summary)
    email_data['attachment_path'] = "mycars.pdf"

    # mygmails.mailservice(email_data)

if __name__ == "__main__":
    main()
