def read_excel(excel_file, col=5, row=5):
    import pandas

    file = pandas.read_excel(excel_file, usecols=[i for i in range(0, col)], header=None)
    file = file.fillna("")
    file_dict = dict(file.head(row))
    result = []
    for i in file_dict.keys():
        result.append([j for j in file_dict[i]])
    return result