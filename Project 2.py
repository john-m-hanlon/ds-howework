from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pylab as pl
import numpy as np
import scipy.stats as stats

df_raw = pd.read_csv('admissions.csv')
df_raw.head()

print('How many observations are there in our dataset?')
print('There are 400 total observaions in our dataset')
print('------------------------------------------------')

print('Create a summary table')
print('Summary table of Admissions, GRE, GPA, and undergraduate school prestige')
print(df_raw.describe())
print('------------------------------------------------')


print('Why would GRE have a larger STD than GPA?')
print('GRE has a larger STD than GPA due to the range of the values. The GRE range is 580, whereas the GPA range is 1.74. A single STD unit from the GRE mean is much larger than a single STD unit from the GPA mean.')
print('------------------------------------------------')


print('Question 4. Drop data points with missing data')
df = df_raw[:].dropna()
print(df.describe())
print('------------------------------------------------')

print('Question 5. Confirm that you dropped the correct data. How can you tell?')
print('You can tell that all the NAN data has been dropped by reviewing the count data. The data was previously not uniform across the different columns. Following the execution of dropna(), we now see that the total count for each variable is the same, meaning all the NAN figures have been dropped.')
print('------------------------------------------------')

print('Question 6. Create box plots for GRE and GPA')

plt.title('GRE Box Plot')
plt.boxplot(df['gre'])
#plt.show()

plt.title('GPA Box Plot')
plt.boxplot(df['gpa'])
#plt.show()
print('------------------------------------------------')

print('Question 7. What do these plots show?')
print('These plots show: median, interquartile range, max / min, outliers')
print('------------------------------------------------')

print('Question 8. Describe each distribution')
print(df.describe())
for i in df:
	print('The distribution of the variable',i,'is:',df[i].skew())
	print('The kurtosis of the variable',i,'is:',df[i].kurt())
	print('')

df.plot(kind='density', xlim=(-5,5))
#plt.show()

print('------------------------------------------------')

print('Question 9. If our model had an assumption of a normal distribution would we meet that requirement?')
print('No, by looking at the skewness, kurtosis, and the graphical representation, we can see that the dataset is not normalized, thus any insights from the analysis may not be able to be reproduced in another study')
print('------------------------------------------------')


print('Question 10. Does this distribution need correction? If so, why? How?')
print('There are two ways to correct the dataset and obtain a normalized dataset. We can either reduce the STD or increase the sample size. Reducing the STD would entail a dataset that is closer to the mean. Additionally, to increase the sampe size we would need a dataset larger than 397 observations to analyze.')
print('------------------------------------------------')

print('Question 11. Which of our variables are potentially colinear')
print(df.corr())
print('Two potentially colinear pairings would be a positive correlation between GRE and GPA and a negative correlation between undergrade presitge and graduate school admission')
print('------------------------------------------------')

print('Question 12. What did you find')
print('There was not any relationship that was particularlly strong. There may be additional variables that we are not considering or we need to increase the sample size')
print('------------------------------------------------')

print('Question 13. Write an analysis plan for exploring the association between grad school admissions rates and prestige of undergraduate schools.')
print("When exploring the relationship between graduate school admissions and the prestige of the applicant's undergraduate institution, first look to clean the data ensure each variable maps accordingly and there are no NAN values. Once the data has been cleaned, determine each variable's distribution and kurtosis. Analyzing datasets that are not normal may yield inaccurate results. To account for a non-normal distribution, run additional tests which permissible to analyze a non-normally distributed dataset. Once these tests have been run, look at the strength of the association between the two variables in scope (admission and undergrad prestige). If there is a strong relationship and the results are statistically significant we should be able to assert that undergrad prestige is a predictor for graduate school admissions. If there is a weak relationship and/or the analysis is not statistically significant, re-examine the variables and looks to see if there may be any additional factors affecting the covariate, such as how is prestige determined and categorized.")
print('------------------------------------------------')

print('Question 14. What is your hypothesis')
print('My hypothesis is that the longer an individual is out of undergradate school, and the longer they are at the same company the more likely they will be to be admitted')
print('------------------------------------------------')




print('Bonus/Advanced')
print('1. Bonus: Explore alternatives to dropping obervations with missing data')
print('2. Bonus: Log transform the skewed data')
print('3. Advanced: Impute missing data')

	