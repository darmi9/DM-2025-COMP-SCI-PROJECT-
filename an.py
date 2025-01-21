import pandas as pd
import plotly.express as px
# Import the CSV file
df = pd.read_csv('updated-salaries-by-college-type.csv')
unique_types = df['School Type'].unique()
#print(unique_types)
# this is so I can see what school types there are and then make individual dataframes from them 
#this will make analysis easier.

engineering_df = df[df['School Type'] == 'Engineering']
party_df = df[df['School Type'] == 'Party']
liberal_arts_df = df[df['School Type'] == 'Liberal Arts']
ivy_league_df = df[df['School Type'] == 'Ivy League']
state_df = df[df['School Type'] == 'State']
#print(engineering_df)

median_salary_box = px.box(df, #box plot
             x='School Type', 
             y='Starting Median Salary',
             color='School Type',  # Different colors for each type
             title='Starting Median Salary by School Type',
             labels={'Starting Median Salary': 'Salary (USD)'},
             color_discrete_map={
                 'Engineering': '#003f5c',
                 'Ivy League': '#68aeba',
                 'Party': '#23627c',
                 'Liberal Arts': '#44879b',
                 'State': '#8fd6d9',})
median_salary_box.update_layout(template='plotly_dark')

# Loop through each school type DataFrame

#median_salary_box.write_html('median_salary_box.html')
#fig.show()
#fig2.show()
# I want to find the mean of all columns in all dataframes. Then bar chart them.
# I could use a try and except thing to tell if the column is a float or not.
def mean_df(df):
    mean_dict = {}
    for column in df.columns:
        try:
            mean_dict[column] = df[column].mean()
        except:
                pass
    return pd.DataFrame(mean_dict, index=[0])
engineering_mean = mean_df(engineering_df)# this worked!!!
party_mean = mean_df(party_df)
ivy_league_mean = mean_df(ivy_league_df)
state_mean = mean_df(state_df)
liberal_arts_mean = mean_df(liberal_arts_df)    
engineering_mean.index = ['Engineering']
party_mean.index = ['Party']
ivy_league_mean.index = ['Ivy League']
state_mean.index = ['State']
liberal_arts_mean.index = ['Liberal Arts']

bar_chart_df = pd.concat([engineering_mean, party_mean, ivy_league_mean, liberal_arts_mean, state_mean])
bar_chart_df.reset_index(inplace=True)
bar_chart_df.rename(columns={'index': 'School Type'}, inplace=True)

salary_data = px.bar(bar_chart_df,
             x= 'School Type',
             y=['Starting Median Salary',
                'Mid-Career Median Salary',
                'Mid-Career 10th Percentile Salary',
                'Mid-Career 25th Percentile Salary',
                'Mid-Career 75th Percentile Salary',
                'Mid-Career 90th Percentile Salary'], 
             title='Salaries by school type', 
             labels={'Starting Median Salary': 'Starting Median Salary'},
             barmode = 'group',
             color_discrete_map={
                 'Starting Median Salary': '#003f5c',
                 'Mid-Career Median Salary': '#68aeba',
                 'Mid-Career 10th Percentile Salary': '#23627c',
                 'Mid-Career 25th Percentile Salary': '#44879b',
                 'Mid-Career 75th Percentile Salary': '#8fd6d9',
                 'Mid-Career 90th Percentile Salary': '#bafff7'},
                )
salary_data.update_layout(template='plotly_dark')
# Show the chart
#salary_data.write_html('salary_data.html')

# I want to make a graph which shows the range of 10th percentile salaries vs 90th percentile salaries.
# I need a data frame which wouuld have the range and the school type.
# we already have average values in the bar chart data frame.
print(bar_chart_df)

# I need to find ranges.
# I can drop unnecesary columns.
bar_chart_df.drop(columns='Starting Median Salary', inplace=True)
bar_chart_df.drop(columns='Mid-Career Median Salary', inplace=True)
bar_chart_df.drop(columns='Mid-Career 25th Percentile Salary', inplace=True)
bar_chart_df.drop(columns='Mid-Career 75th Percentile Salary', inplace=True)
# I can just subtract the columns now.
bar_chart_df['Range'] = bar_chart_df['Mid-Career 90th Percentile Salary'] - bar_chart_df['Mid-Career 10th Percentile Salary']
print(bar_chart_df) # now I can drop the rest of the columns (apart from the ranges of course)
bar_chart_df.drop(columns='Mid-Career 10th Percentile Salary', inplace=True)
bar_chart_df.drop(columns='Mid-Career 90th Percentile Salary', inplace=True)
print(bar_chart_df)

ranges = px.bar(bar_chart_df, x='School Type', y='Range', title='Range of Salaries by School Type (From 90th percentile to 10th percentile)',
                color='School Type',  # Different colors for each type
                color_discrete_map={
                 'Engineering': '#003f5c',
                 'Ivy League': '#68aeba',
                 'Party': '#23627c',
                 'Liberal Arts': '#44879b', # these colours are the same as the ones from the other graphs, to keep the theme 
                 'State': '#8fd6d9',}) # the colours are in hexidecimal format.
ranges.update_layout(template='plotly_dark')
ranges.write_html('ranges.html')
