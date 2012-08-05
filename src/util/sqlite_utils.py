def name_columns(rs):
    results = []
    for row in rs:
        named_row = {}
        for i, column in enumerate(row):
            named_row[rs.description[i][0]] = column
        results.append(named_row)
    return results

