
# coding: utf-8

# # Capstone Project 1: MuscleHub AB Test

# ## Step 1: Get started with SQL

# Like most businesses, Janet keeps her data in a SQL database.  Normally, you'd download the data from her database to a csv file, and then load it into a Jupyter Notebook using Pandas.
# 
# For this project, you'll have to access SQL in a slightly different way.  You'll be using a special Codecademy library that lets you type SQL queries directly into this Jupyter notebook.  You'll have pass each SQL query as an argument to a function called `sql_query`.  Each query will return a Pandas DataFrame.  Here's an example:

# In[9]:


# This import only needs to happen once, at the beginning of the notebook
from codecademySQL import sql_query


# In[ ]:





# In[2]:



# Here's an example of a query that just displays some data
sql_query('''
SELECT *
FROM visits
LIMIT 5
''')


# In[3]:


# Here's an example where we save the data to a DataFrame
df = sql_query('''
SELECT *
FROM applications
LIMIT 5
''')


# ## Step 2: Get your dataset

# Let's get started!
# 
# Janet of MuscleHub has a SQLite database, which contains several tables that will be helpful to you in this investigation:
# - `visits` contains information about potential gym customers who have visited MuscleHub
# - `fitness_tests` contains information about potential customers in "Group A", who were given a fitness test
# - `applications` contains information about any potential customers (both "Group A" and "Group B") who filled out an application.  Not everyone in `visits` will have filled out an application.
# - `purchases` contains information about customers who purchased a membership to MuscleHub.
# 
# Use the space below to examine each table.

# In[4]:


"""I used this SQL query to test the visit_date qualifiers"""

sql_query('''
SELECT *
FROM visits
WHERE visit_date >= '7-1-17' 
LIMIT 10
''')


# In[5]:


sql_query('''
SELECT *
FROM fitness_tests
LIMIT 10
''')


# In[6]:


sql_query('''
SELECT *
FROM applications
LIMIT 5
''')


# In[7]:


sql_query('''
SELECT *
FROM purchases
LIMIT 5
''')


# We'd like to download a giant DataFrame containing all of this data.  You'll need to write a query that does the following things:
# 
# 1. Not all visits in  `visits` occurred during the A/B test.  You'll only want to pull data where `visit_date` is on or after `7-1-17`.
# 
# 2. You'll want to perform a series of `LEFT JOIN` commands to combine the four tables that we care about.  You'll need to perform the joins on `first_name`, `last_name`, and `email`.  Pull the following columns:
# 
# 
# - `visits.first_name`
# - `visits.last_name`
# - `visits.gender`
# - `visits.email`
# - `visits.visit_date`
# - `fitness_tests.fitness_test_date`
# - `applications.application_date`
# - `purchases.purchase_date`
# 
# Save the result of this query to a variable called `df`.
# 
# Hint: your result should have 5004 rows.  Does it?

# In[30]:



"""
Define the data frame from a SQL statement.
Join the four tables together by first_name, last_name and
email address.
"""

df = sql_query('''
SELECT  visits.first_name,
        visits.last_name,
        visits.gender,
        visits.email,
        visits.visit_date,
        fitness_tests.fitness_test_date,
        applications.application_date,
        purchases.purchase_date
FROM visits 
LEFT JOIN fitness_tests 
    ON visits.first_name = fitness_tests.first_name 
    AND visits.last_name = fitness_tests.last_name 
    AND visits.email = fitness_tests.email
LEFT JOIN applications
    ON visits.first_name = applications.first_name
    AND visits.last_name = applications.last_name
    AND visits.email = applications.email
LEFT JOIN purchases
    ON visits.first_name = purchases.first_name
    AND visits.last_name = purchases.last_name
    AND visits.email = purchases.email
WHERE visits.visit_date >= '7-1-17'
''')

"""creates a variable to count the items in the data frame."""
count_df = df.count()

"""Print the dataframe items for auditing."""
print(count_df)


# ## Step 3: Investigate the A and B groups

# We have some data to work with! Import the following modules so that we can start doing analysis:
# - `import pandas as pd`
# - `from matplotlib import pyplot as plt`

# In[31]:


import pandas as pd

from matplotlib import pyplot as plt


# We're going to add some columns to `df` to help us with our analysis.
# 
# Start by adding a column called `ab_test_group`.  It should be `A` if `fitness_test_date` is not `None`, and `B` if `fitness_test_date` is `None`.

# In[32]:


"""
Defines a lambda expression that looks at fitness_test_date 
and determines if a member in the test groups are part of group 'A' or 'B'.
"""

df['ab_test_group'] = df['fitness_test_date'].apply(lambda x: 'A' if pd.notnull(x) else 'B')


# Let's do a quick sanity check that Janet split her visitors such that about half are in A and half are in B.
# 
# Start by using `groupby` to count how many users are in each `ab_test_group`.  Save the results to `ab_counts`.

# In[33]:


"""
Check for an even distribution of visitors by grouping
the number of visitors and getting a count for groups 'A' and 'B'.
"""

ab_counts = df.groupby('ab_test_group').first_name.count().reset_index()
print(ab_counts)


# We'll want to include this information in our presentation.  Let's create a pie cart using `plt.pie`.  Make sure to include:
# - Use `plt.axis('equal')` so that your pie chart looks nice
# - Add a legend labeling `A` and `B`
# - Use `autopct` to label the percentage of each group
# - Save your figure as `ab_test_pie_chart.png`

# In[34]:


"""
Determine the number for each of the ab_test_groups to use in a pie chart by
setting the labels and count values.
"""
pie_labels = ab_counts.ab_test_group.values
pie_counts = ab_counts.first_name.values

"""
Plot the pie chart utilizing the established values for counts and labels 
and establishing them as a percentage.
Add an equal distribution for better visualization and include a title and legend.
"""

plt.pie(pie_counts, labels = pie_labels, autopct = '%0.1f%%')
plt.axis('equal')
plt.title('Even Distribution Test')
plt.legend()

"""Save the image as a png to be used in future presentations"""

plt.savefig('ab_test_pie_chart.png',bbox_inches='tight',transparent = True)

plt.show()


# ## Step 4: Who picks up an application?

# Recall that the sign-up process for MuscleHub has several steps:
# 1. Take a fitness test with a personal trainer (only Group A)
# 2. Fill out an application for the gym
# 3. Send in their payment for their first month's membership
# 
# Let's examine how many people make it to Step 2, filling out an application.
# 
# Start by creating a new column in `df` called `is_application` which is `Application` if `application_date` is not `None` and `No Application`, otherwise.

# In[35]:


"""
Defines a lambda expression that looks at application_date 
and determines if a visitor in the test groups filled out an application
by looking at null values in the application_date field.
"""

df['is_application'] = df['application_date'].apply(lambda x: 'Application' if pd.notnull(x) else 'No Application')


# Now, using `groupby`, count how many people from Group A and Group B either do or don't pick up an application.  You'll want to group by `ab_test_group` and `is_application`.  Save this new DataFrame as `app_counts`

# In[36]:


"""
Count the number of visitors from each group who pick up an application
or do not pick up and application using groupby and count functions.
"""

app_counts = df.groupby(['ab_test_group','is_application']).first_name.count().reset_index()
print(app_counts)


# We're going to want to calculate the percent of people in each group who complete an application.  It's going to be much easier to do this if we pivot `app_counts` such that:
# - The `index` is `ab_test_group`
# - The `columns` are `is_application`
# Perform this pivot and save it to the variable `app_pivot`.  Remember to call `reset_index()` at the end of the pivot!

# In[37]:


"""
Create a pivot table to better visualize the number of visitors from 
groups 'A' and 'B' who did and did not pick up an application.
"""

app_pivot = app_counts.pivot(columns = 'is_application',
                             index = 'ab_test_group',
                             values = 'first_name')\
                      .reset_index()
    
print(app_pivot)


# Define a new column called `Total`, which is the sum of `Application` and `No Application`.

# In[38]:


"""
Add a new column to the applicant count pivot table that gives a total 
number of visitors for each test group.
"""

app_pivot['Total'] = app_pivot['Application'] + app_pivot['No Application']

print(app_pivot)


# Calculate another column called `Percent with Application`, which is equal to `Application` divided by `Total`.

# In[39]:


"""
Add a percentage column to the applicant count pivot table that gives a 
percentage of the total of visitors who picks up an application for 
each test group.
"""

app_pivot['Percent with Application'] = app_pivot['Application'] / app_pivot['Total']

print(app_pivot)


# It looks like more people from Group B turned in an application.  Why might that be?
# 
# We need to know if this difference is statistically significant.
# 
# Choose a hypothesis tests, import it from `scipy` and perform it.  Be sure to note the p-value.
# Is this result significant?

# In[56]:


"""Import the chi square test for data analysis."""

from scipy.stats import chi2_contingency

"""
Establish a contingency table to be used in the chi sqaure test.
Include the number of Applications and Non Applications 
from each group.
Perform the Chi Square test using chi2_contigency() from scipy.
"""
app_X = [[250, 2254],
         [325, 2175]]

chi2, apply_pval, dof, expected = chi2_contingency(app_X)

"""Print the Chi-Square Test Values"""
print("chi2", chi2)
print ("pval = ", apply_pval)
print ("dof = ", dof)
print ("expected values = ", expected)

"""
Create a quick function to determine if the p-value is significant
by comparing the value to 0.05.
"""

if apply_pval < 0.05:
    print 'This value is statiscally significant'
else:
    print 'This value is not statiscally significant'


# ## Step 4: Who purchases a membership?

# Of those who picked up an application, how many purchased a membership?
# 
# Let's begin by adding a column to `df` called `is_member` which is `Member` if `purchase_date` is not `None`, and `Not Member` otherwise.

# In[41]:


"""
Define a lambda expression to determine, out of the number of visitors
who picked up an application, who purchased a membership.
"""

df['is_member'] = df['purchase_date'].apply(lambda x: 'Member' if pd.notnull(x)                                             else 'Not Member')


# Now, let's create a DataFrame called `just_apps` the contains only people who picked up an application.

# In[42]:


"""Create a dataframe that contains on the visitors who picked up an application"""

just_apps = df[df['is_application'] == 'Application']


# Great! Now, let's do a `groupby` to find out how many people in `just_apps` are and aren't members from each group.  Follow the same process that we did in Step 4, including pivoting the data.  You should end up with a DataFrame that looks like this:
# 
# |is_member|ab_test_group|Member|Not Member|Total|Percent Purchase|
# |-|-|-|-|-|-|
# |0|A|?|?|?|?|
# |1|B|?|?|?|?|
# 
# Save your final DataFrame as `member_pivot`.

# In[43]:


"""
Using the information from the dataframe that contains only visitors 
that picked up an application, create a pivot table to better
visualize the number of members from each test group.
"""

member_counts = just_apps.groupby(['ab_test_group', 'is_member'])                         .first_name.count().reset_index()

member_pivot = member_counts.pivot(columns = 'is_member',
                                index = 'ab_test_group',
                                values = 'first_name')\
                            .reset_index()

"""
Add a new column to the member pivot table that creates a total of visitors 
who picked up an application for each test group.
"""

member_pivot['Total'] = member_pivot['Member'] + member_pivot['Not Member']

"""
Add a new column to the member pivot table that creates a percentage of visitors
who picked up an application and purchased a membership for each test group.
"""

member_pivot['Recent Purchase'] = member_pivot['Member'] / member_pivot['Total']

print(member_pivot)


# It looks like people who took the fitness test were more likely to purchase a membership **if** they picked up an application.  Why might that be?
# 
# Just like before, we need to know if this difference is statistically significant.  Choose a hypothesis tests, import it from `scipy` and perform it.  Be sure to note the p-value.
# Is this result significant?

# In[44]:


"""
Establish a contingency table to be used in the chi sqaure test.
Include the number of Members and Non Members
from each group of visitors who picked up an application.
Perform the Chi Square test using chi2_contigency() from scipy.
"""

mem_X = [[200, 50],
         [250, 75]]

chi2, member_pval, dof, expected = chi2_contingency(mem_X)

"""Print the Chi-Square Test Values"""
print("chi2", chi2)
print ("member_pval = ", member_pval)
print ("dof = ", dof)
print ("expected values = ", expected)

"""
Create a quick function to determine if the p-value is significant
by comparing the value to 0.05.
"""

if member_pval < 0.05:
    print 'This value is statiscally significant'
else:
    print 'This value is not statiscally significant'


# Previously, we looked at what percent of people **who picked up applications** purchased memberships.  What we really care about is what percentage of **all visitors** purchased memberships.  Return to `df` and do a `groupby` to find out how many people in `df` are and aren't members from each group.  Follow the same process that we did in Step 4, including pivoting the data.  You should end up with a DataFrame that looks like this:
# 
# |is_member|ab_test_group|Member|Not Member|Total|Percent Purchase|
# |-|-|-|-|-|-|
# |0|A|?|?|?|?|
# |1|B|?|?|?|?|
# 
# Save your final DataFrame as `final_member_pivot`.

# In[45]:


"""
Using the information from the main dataframe ,create a pivot table to 
better visualize the number of visitors from each test group who 
purchased a membership.
"""

final_member_counts = df.groupby(['ab_test_group', 'is_member'])                        .first_name.count().reset_index()
                 
final_member_pivot = final_member_counts.pivot(columns = 'is_member',
                                               index = 'ab_test_group',
                                               values = 'first_name')\
                                        .reset_index()

"""Add a new column to the final member pivot table that creates a total of visitors for each test group"""

final_member_pivot['Total'] = final_member_pivot['Member'] + final_member_pivot['Not Member']

"""
Add a new column to the final member pivot table that creates a percentage of visitors 
that purchased a membership for each test group
"""

final_member_pivot['Percent Purchase'] = final_member_pivot['Member'] / final_member_pivot['Total']

print(final_member_pivot)


# Previously, when we only considered people who had **already picked up an application**, we saw that there was no significant difference in membership between Group A and Group B.
# 
# Now, when we consider all people who **visit MuscleHub**, we see that there might be a significant different in memberships between Group A and Group B.  Perform a significance test and check.

# In[57]:


"""
Establish a contingency table to be used in the chi sqaure test.
Include the number of Members and Non Members from each group.
Perform the Chi Square test using chi2_contigency() from scipy.
"""

fin_X = [[200, 2304],
         [250, 2250]]

chi2, final_member_pval, dof, expected = chi2_contingency(fin_X)

"""Print the Chi-Square Test Values"""
print ("chi2 = ", chi2)  
print ("final_member_pval = ", final_member_pval)
print ("dof = ", dof)
print ("expected values = ", expected)

"""
Create a quick function to determine if the p-value is significant
by comparing the value to 0.05.
"""

if final_member_pval < 0.05:
    print 'This value is statiscally significant'
else:
    print 'This value is not statiscally significant'


# ## Step 5: Summarize the acquisition funel with a chart

# We'd like to make a bar chart for Janet that shows the difference between Group A (people who were given the fitness test) and Group B (people who were not given the fitness test) at each state of the process:
# - Percent of visitors who apply
# - Percent of applicants who purchase a membership
# - Percent of visitors who purchase a membership
# 
# Create one plot for **each** of the three sets of percentages that you calculated in `app_pivot`, `member_pivot` and `final_member_pivot`.  Each plot should:
# - Label the two bars as `Fitness Test` and `No Fitness Test`
# - Make sure that the y-axis ticks are expressed as percents (i.e., `5%`)
# - Have a title

# In[52]:


"""Create a visualization for the number of visitors who picked up an application"""

"""Plot a bar chart"""
ax = plt.subplot()
plt.bar(range(len(app_pivot)), app_pivot['Percent with Application'].values)

"""
Format the bar chart by utilizing the values in the application pivot table.
Add X and Y ticks to support and focus the visualization of data.
"""

ax.set_xticks(range(len(app_pivot)))
ax.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax.set_yticks([0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14])
ax.set_yticklabels(['0%', '2%', '4%', '6%', '8%', '10%', '12%', '14%'])

"""Add labels and a title to the bar chart."""
plt.title('Visitors Who Completed an Application')
plt.xlabel('Visitor Types')
plt.ylabel('Percent of Visitors Who Apply')

"""Save the image as a png to be used in future presentations"""
plt.savefig('percent_visitors_apply_chart.png', bbox_inches = 'tight')

plt.show()


# In[53]:


"""Create a visualization for the percent of applicants who purchased a membership"""

"plot a bar chart"
ax1 = plt.subplot()
plt.bar(range(len(member_pivot)), member_pivot['Recent Purchase'].values)

"""
Format the bar chart by utilizing the values in the application pivot table.
Add X and Y ticks to support and focus the visualization of data.
"""

ax1.set_xticks(range(len(member_pivot)))
ax1.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax1.set_yticks([0.0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00])
ax1.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])

"""Add labels and a title to the bar chart."""

plt.title('Applicants Who Purchased Membership')
plt.xlabel('Visitor Types')
plt.ylabel('Percent of Applicants Who Purchased Membership')

"""Save the image as a png to be used in future presentations"""
plt.savefig('percent_apply_purchase_chart.png', bbox_inches = 'tight')

plt.show()


# In[54]:


"""Create a visualization for the percent of visitors who purchase a membership"""

"""Plot a bar chart"""
ax2 = plt.subplot()
plt.bar(range(len(final_member_pivot)), final_member_pivot['Percent Purchase'].values)

"""
Format the bar chart by utilizing the values in the application pivot table.
Add X and Y ticks to support and focus the visualization of data.
"""

ax2.set_xticks(range(len(final_member_pivot)))
ax2.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax2.set_yticks([0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14])
ax2.set_yticklabels(['0%', '2%', '4%', '6%', '8%', '10%', '12%', '14%'])

"""Add labels and a title to the bar chart."""

plt.title('Visitors Who Purchased a Membership')
plt.xlabel('Visitor Types')
plt.ylabel('Percent of Visitors Who Purchased')

"""Save the image as a png to be used in future presentations"""

plt.savefig('percent_visitors_purchase_chart.png', bbox_inches = 'tight')

plt.show()

