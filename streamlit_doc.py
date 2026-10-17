import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='startup anyalysis') 

df = pd.read_csv('cleared_data_strmlt')
df['date'] = pd.to_datetime(df['date'], errors='coerce')

clear_df = pd.read_csv('cleared_data_strmlt')
clear_df['date'] = pd.to_datetime(clear_df['date'])
clear_df['year'] = clear_df['date'].dt.year
clear_df['month'] = clear_df['date'].dt.month
clear_df['investment'] = clear_df['investment'].replace({
    # Seed Funding
    'Seed Round': 'Seed Funding',
    'Seed': 'Seed Funding',
    'Seed funding': 'Seed Funding',
    'Seed Funding Round': 'Seed Funding',

    # Pre-Series A
    'Pre-series A': 'Pre-Series A',
    'pre-series A': 'Pre-Series A',
    'pre-Series A': 'Pre-Series A',
    'Pre Series A': 'Pre-Series A',

    # Angel Funding
    'Angel': 'Angel Funding',
    'Angel Round': 'Angel Funding',

    # Seed + Angel Funding
    'Seed/ Angel Funding': 'Seed + Angel Funding',
    'Seed / Angel Funding': 'Seed + Angel Funding',
    'Seed/Angel Funding': 'Seed + Angel Funding',
    'Seed / Angle Funding': 'Seed + Angel Funding',
    'Angel / Seed Funding': 'Seed + Angel Funding',

    # Venture Capital
    'Venture': 'Venture Capital',
    'Venture Round': 'Venture Capital',
    'Venture - Series Unknown': 'Venture Capital',

    # Private Equity
    'Private Equity Round': 'Private Equity',
    'PrivateEquity': 'Private Equity',

    # Debt Funding
    'Debt-Funding': 'Debt Funding',

    # Equity Funding
    'Equity Based Funding': 'Equity Funding'
})

# startup anaylysis 

def load_startup_anaylysis(selected_startup,df):
    startup_df = df[df['startup'] == selected_startup]
    
    # company deatails 

    st.subheader('Company Profile')
    industry = startup_df['verticle'].dropna()
    subindustry = startup_df['SubVertical'].dropna()
    location = startup_df['city'].dropna()

    industry = industry.iloc[0] if not industry.empty else 'Not Available'
    subindustry = subindustry.iloc[0] if not subindustry.empty else 'Not Available'
    location = location.iloc[0] if not location.empty else 'Not Available'

    st.header(selected_startup)

    col1, col2, col3 = st.columns(3)

    col1.markdown('**Industry**')
    col1.write(industry)

    col2.markdown('**Subindustry**')
    col2.write(subindustry)

    col3.markdown('**Location**')
    col3.write(location)



    # Funding Summary
    st.subheader('Funding Summary')

    total_funding = startup_df['amount'].sum()
    total_rounds = startup_df['investment'].count()
    avg_funding = startup_df['amount'].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric('Total Funding', f'₹{total_funding:.2f} Cr')
    col2.metric('Funding Rounds', total_rounds)
    col3.metric('Average Funding', f'₹{avg_funding:.2f} Cr')


    # funding history
    st.subheader('Funding History')

    funding_history = startup_df[['investment', 'investors', 'date', 'amount']].copy()
    funding_history['date'] = pd.to_datetime(funding_history['date'], errors='coerce')
    funding_history = funding_history.sort_values('date', ascending=True, na_position='last')
    st.dataframe(funding_history, hide_index=True)


    # similar startup 
    st.subheader('Similar Companies')

    industry_values = startup_df['verticle'].dropna()

    if not industry_values.empty:

        industry = industry_values.iloc[0]

        similar_companies = df[
            (df['verticle'] == industry) &
            (df['startup'] != selected_startup)
        ]

        similar_summary = (similar_companies.groupby('startup').agg(
                Industry=('verticle', 'first'),
                Location=('city', 'first'),
                Total_Funding=('amount', 'sum')
            )
            .sort_values('Total_Funding', ascending=False)
            .head(10)
            .reset_index()
        )

        st.dataframe(similar_summary, hide_index=True)

    else:
        st.info('Industry information is not available for this startup.')





















# overall anylysys 
def load_overall_analysis(df,clear_df):
    
    st.title('Overall Analysis')
    
    #'total_money_used_in_indian_marcket'
    total_money = round(df['amount'].sum())
    st.metric('total_money_used_in_indian_marcket', str(total_money) + '  Crore')

    # maximum amount infused in startup 
    max_amount = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1)
    max_amount = max_amount.to_string()
    st.metric('maximum amount infused in startup', str(max_amount) + " CR")

    # avg money uesd in each startup
    avg_money = round(df.groupby('startup')['amount'].sum().mean(), 3)
    st.metric('avg money uesd in each startup', str(avg_money)+' CR')

    # totall funded startup
    total_funded = clear_df['startup'].nunique()
    st.metric('total funded startup', total_funded)

    # year on year graph

    # yearly funding money
    df1 = clear_df.groupby(['year', 'month'])['amount'].sum().reset_index()
    df1['x_axis'] = clear_df['month'].astype(str)+'-'+clear_df['year'].astype(str)
    temp_df1 = df1[['amount', 'year']]

    st.subheader("yearly funding money")
    fig, ax = plt.subplots()
    ax.plot(temp_df1['year'], temp_df1['amount'])
    st.pyplot(fig)

    # yearly startup count
    df1 = clear_df.groupby(['year', 'month'])['amount'].count().reset_index()
    df1['x_axis'] = clear_df['month'].astype(str)+'-'+clear_df['year'].astype(str)
    temp_df1 = df1[['amount', 'year']]

    st.subheader("yearly startup count")
    fig, ax = plt.subplots()
    ax.plot(temp_df1['year'], temp_df1['amount'])
    st.pyplot(fig)

    # Top 10 Verticals by msot funded
    top_10_vericle_funded = clear_df.groupby('verticle')['amount'].sum().sort_values(ascending=False).head(10)
    st.subheader("Top 10 Verticals by msot funded")
    fig, ax = plt.subplots()
    ax.pie(top_10_vericle_funded, labels=top_10_vericle_funded.index, autopct= "%0.01f%%")
    st.pyplot(fig)
        
    # Top 10 Verticals by totall investment
    top_10_vericle_invest = clear_df.groupby('verticle')['amount'].sum().sort_values(ascending=False).head(10)
    st.subheader("Top 10 Verticals by totall investment")
    fig, ax = plt.subplots()
    ax.pie(top_10_vericle_invest, labels=top_10_vericle_invest.index, autopct= "%0.01f%%")
    st.pyplot(fig)  

    # type of funding
    type_investment = clear_df['investment'].value_counts(ascending=False).head(10)
    st.subheader("top 10 funding's type ")
    fig, ax = plt.subplots()
    ax.pie(type_investment, labels=type_investment.index, autopct= "%0.01f%%")
    st.pyplot(fig) 

    # top 10 most fund raised cities
    clear_df['city'] = clear_df['city'].replace({
    'Bengaluru':"Bangalore"
    })
    st.subheader("top 10 most fund raised cities")
    top_cities = clear_df.groupby('city')['amount'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    ax.pie(top_cities, labels=top_cities.index, autopct= "%0.01f%%" )
    st.pyplot(fig)
    
    
    # Top startup ---> year_wise
    st.subheader("Top startup ---> year_wise")
    selected_year = st.selectbox( 'Select Year',sorted(clear_df['year'].unique(), reverse=True))

    select_year = (clear_df[clear_df['year'] == selected_year])
    plot_df = select_year.groupby('startup')['amount'].sum().nlargest(10).sort_values().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(plot_df['startup'], plot_df['amount'])
    ax.set_title(f'Top 10 Startups by Investment — {selected_year}')
    ax.set_xlabel('Total Investment')
    ax.set_ylabel('Startup')
    plt.tight_layout()
    st.pyplot(fig)

    # top startup >> overall
    top_10_startup = clear_df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)
    st.subheader('Top 10 Startups by Investment')
    st.dataframe(top_10_startup)

    # top 10 investors
    top_10_investors = clear_df.groupby('investors')['amount'].sum().sort_values(ascending=False).head(10)
    st.subheader('Top 10 investors by investment')
    st.dataframe(top_10_investors)

    # funding heatmap
    import seaborn as sns
    st.subheader('Funding Heatmap')

    heatmap_data = clear_df.pivot_table(index='year',columns='month',values='amount',aggfunc='sum',fill_value=0)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(heatmap_data,cmap='YlOrRd',annot=True,fmt='.0f',linewidths=0.5,ax=ax,
                            cbar_kws={'label': 'Amount (Crore)'})

    ax.set_title('Monthly Funding by Year')
    ax.set_xlabel('Month')
    ax.set_ylabel('Year')

    st.pyplot(fig)




def load_investor_details(invester,df):
    st.title(invester)
    # load the recent five investement of the investor
    last5_df = df[df['investors'].str.contains(invester)].head()[['date', 'startup', 'verticle', 'city', 'amount']]
    st.subheader('most recent investment')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    
    # biggest investment 
    with col1:
        big_series= (df[df['investors'].str.contains(invester)].groupby('startup')['amount']
                .sum().sort_values(ascending=False).head())
        
        st.subheader('Biggest_Investment')
        st.dataframe(big_series)
    # gph_plot (bar_plot)
    with col2:
        st.subheader("startup(X) vs amount(Y)")
        fig, ax = plt.subplots()
        ax.bar(big_series.index , big_series.values)
        st.pyplot(fig)

    col1, col2 = st.columns(2)        
    # (pie_plot)
    with col1:
        plot_series = df[df['investors'].str.contains(invester)].groupby('verticle')['amount'].sum() 
        plot_series = plot_series[plot_series > 0]  
        st.subheader("sector_invested_in")
        fig, ax = plt.subplots()
        ax.pie(plot_series, labels=plot_series.index, autopct= "%0.01f%%")
        st.pyplot(fig)

    with col2:
        plot_series = df[df['investors'].str.contains(invester)].groupby('city')['amount'].sum() 
        plot_series = plot_series[plot_series > 0]  
        st.subheader("city_invested_in")
        fig, ax = plt.subplots()
        ax.pie(plot_series, labels=plot_series.index, autopct= "%0.01f%%")
        st.pyplot(fig)
    
    # year on year investment graph
  
    df['year'] = df['date'].dt.year
    
    year_series = df[df['investors'].str.contains(invester)].groupby('year')['amount'].sum()
    st.subheader('year on year investment graph')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index , year_series.values)
    st.pyplot(fig2)

    # similar investor
    st.subheader('"x%" comman_investor to selected_investor')

    df = df.assign(investor=df['investors'].str.split(',')).explode('investor')

    df['investor'] = df['investor'].str.strip()

    profile = df.groupby(['investor', 'city', 'verticle', 'investment']).size()

    profile = profile.reset_index(name='count')

    selected_profile = profile[profile['investor'] == invester]
    
    matches = profile.merge(selected_profile,on=['city', 'verticle', 'investment'])
   
    matches = matches[ matches['investor_x'] != invester]

    similar_investors = (matches.groupby('investor_x').size().reset_index(name='common_patterns')
                         .sort_values('common_patterns', ascending=False))

    total_patterns = profile[profile['investor'] == invester].shape[0]

    similar_investors['similarity_%'] = (similar_investors['common_patterns']/ total_patterns * 100).round(1)
    st.dataframe(similar_investors.head(5))




st.sidebar.title('Indian Startup Funding Analysis')
option = st.sidebar.selectbox('select One', ['Overall anylysis', 'Startup', 'Investor'])

if option == 'Overall anylysis':
    load_overall_analysis(df, clear_df )


elif option == 'Startup':
    selected_startup = st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    st.title('Startup Anylysis')
    btn1 = st.sidebar.button('Find Startup Detail ')
    if btn1:
        load_startup_anaylysis(selected_startup,df)

else: # {investor}
    selected_investor = st.sidebar.selectbox('Investor',sorted(set(df['investors'].str.split(',')
                                                                   .explode().str.strip().dropna().unique())))
    st.title('Investor Anylysis')
    btn2 = st.sidebar.button('Find Investor Detail ')
    if btn2:
        load_investor_details(selected_investor, df)