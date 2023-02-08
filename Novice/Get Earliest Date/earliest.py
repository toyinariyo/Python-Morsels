def get_earliest(first_date, second_date):
    first_month, first_day, first_year = first_date.split("/")
    second_month, second_day, second_year = second_date.split("/")
    if (first_year, first_month, first_day) < (second_year, second_month, second_day):
        return first_date
    else:
        return second_date

      
