# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 20:16:04 2019

@author: George, Amit, Tal, Gili
"""
#%%
import pandas as pd
import scipy

def save_life(df, col_name, to_sort=False, order=None, is_pct=True):
    # remove accidents not on intersections
    a = df.dropna(subset=['non_urban_intersection_hebrew'])
    a["non_urban_intersection_hebrew"] = a["non_urban_intersection_hebrew"].apply(lambda x: x.replace("מחלף", "צומת"))
    a["accident_type_hebrew"] = a["accident_type_hebrew"].apply(lambda x: x.replace(" אל ", " ב"))
    # remove duplicate entries for the same accident_id
    a = a.groupby('provider_and_id')['non_urban_intersection_hebrew', col_name].first()
    no_dup = a
    # count for each intersection how many intersections each year
    b = a.groupby(['non_urban_intersection_hebrew', col_name]).size().reset_index().rename(columns={0: 'count'})
    # pivot. making 2d table with each intersection name and year as rows and columns
    c = b.pivot('non_urban_intersection_hebrew', col_name, 'count')
    # years with no accidents are nans here, change the
    c.fillna(0, inplace=True)
    # add total number of accident for each intersection
    c['total'] = c.sum(axis=1)
    # sort it
    c.sort_values('total', inplace=True, ascending=False)
    
    for col in c:
        if col != "total":
            if is_pct:
                c[col] = c[col] / c["total"] *100
    
    if to_sort:
        cols = []
        for col in c:
            #if c[col].max() > 0.05:
            cols.append((col, (c[col]*c['total']).mean()))
        cols = sorted(cols, key=lambda x: x[1])
        cols = [x[0] for x in cols]
    else:
        cols = c.columns
    c = c[c.total > 49].copy()
    c = c[cols].copy()
    if order is not None:
        c = c[order]
    return c, no_dup

#%%
def calc_scores(df, col_name):
    vec, no_dup = save_life(df, col_name, is_pct=False)
    dist = no_dup.groupby(col_name)["non_urban_intersection_hebrew"].count() / no_dup.groupby(col_name)["non_urban_intersection_hebrew"].count().sum()

    res = []
    res1 = []
    for idx, x in vec.iterrows():
        cur = {"name": idx}
        cur1 = {"name": idx}
        for c in vec:
            if c != "total":
                cur[c] = scipy.stats.binom_test(x[c], x["total"], dist[c], 
                   alternative='greater')
                if cur[c] < 0.01:
                    cur1[c] = (x[c] / x["total"]) / dist[c]
                else:
                    cur1[c] = None
        res.append(cur)
        res1.append(cur1)
    return pd.DataFrame(res1)


df = pd.read_csv(r'anyway_tables_csv_updated/involved_markers_hebrew.csv')
h = {x: "late_night" for x in [23, 0, 1, 2, 3, 4]}
h.update({x: "morning" for x in [5, 6, 7, 8, 9, 10, 11, 12]})
h.update({x: "noon" for x in [13, 14, 15, 16]})
h.update({x: "evening" for x in [17, 18, 19, 20, 21, 22]})
df["stage"] = df.accident_hour.apply(lambda x: h[x])

accident_type = calc_scores(df, "accident_type_hebrew")
stage = calc_scores(df, "stage")
vehicle_type_hebrew = calc_scores(df, "vehicle_type_hebrew")
age_group_hebrew = calc_scores(df, "age_group_hebrew")
severity = calc_scores(df, "accident_severity_hebrew")

