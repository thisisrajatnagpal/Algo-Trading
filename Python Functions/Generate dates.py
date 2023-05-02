def gen_dates(first_date, days):
    duration = dt.timedelta(days)
    from_date = dt.datetime.strptime(first_date, '%d-%m-%Y')
    #print(from_date.strftime("%A"))
    store = []
    for d in range(duration.days + 1):
        day = from_date + dt.timedelta(days=d)
        store.append(day)
    return store
