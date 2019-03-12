# Intersection-wise accidents analysis
The script perform analysis on a dataset, grouping the data into **Intersections** and examining different features distributions. The script contains 2 main functions:
* `save_life` - Receives a dataframe and a column name and return a pivoted 2d table with each row containing an intersection's distribution of values of the column its name was given (intersections with small amount of accidents are removed). Several additional parameters can tune the results - return percentages instead of fractions, order results, etc.
* `calc_scores` - Wraps the function above and filter values of distributions which are "suprising". A suprising observation is concluded by performing a binomial test with P-value set by the overall distribution (summing all intersections values) and receving a near 0 probability. After filtering relevant values in the table, we replace the values with a more intuitive value which is the ration between the observed probability of a feature in an intersection and the probability of it in all dataset.

## TODO
* Pivot value - the whole analysis can be used on other pivot feature rather than **Intersections** if generalizing `non_urban_intersection_hebrew` value into a parameter
* Input - the input file and format are hardcoded
