import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import calendar

def filter_transaction_dataframe(df, filters):
    filtered_df = df.copy()
    if filters["Start Date"] or filters["End Date"]:
        if filters["Start Date"]:
            filtered_df = filtered_df[filtered_df["Date"] >= filters["Start Date"]]
        if filters["End Date"]:
            filtered_df = filtered_df[filtered_df["Date"] <= filters["End Date"]]
    if filters["Category"]:
            filtered_df = filtered_df[filtered_df["Category"].isin(filters["Category"])]
    if filters["Sub-Category"]:
            filtered_df = filtered_df[filtered_df["Sub-Category"].isin(filters["Sub-Category"])]
    if filters["Lower Amount"] or filters["Upper Amount"]:
         if filters["Lower Amount"]:
            filtered_df = filtered_df[filtered_df["Amount"] >= filters["Lower Amount"]]
         if filters["Upper Amount"]:
            filtered_df = filtered_df[filtered_df["Amount"] <= filters["Upper Amount"]]
    
    return filtered_df

def get_table_totals(df):
    total_income = "{:,.2f}".format(round(df[df['Category']=='Income']['Amount'].sum(), 2))
    total_spending = "{:,.2f}".format(round(df[~df['Category'].isin(['Income','Savings'])]['Amount'].sum(), 2))
    total_savings = "{:,.2f}".format(round(df[df['Category'].isin(['Savings & Investments'])]['Amount'].sum(), 2))

    return [total_income, total_spending, total_savings]

def draw_cash_flow(df):
    cash_flow_df = df.copy()

    # all categories not income are considered expense
    cash_flow_df.loc[cash_flow_df['Category'] != "Income", 'Category'] = "Expense"
    # get the totals for each category of each month
    cash_flow_df = cash_flow_df.groupby(['Month','Category'])[['Amount']].sum().reset_index()
    # determining palette for each category
    palette = {'Income': '#4bd02b', 'Expense': '#e33434'}

    # create net income for each month to display at top of plot
    net_income_df = df.copy()
    net_income_df.loc[net_income_df['Category'] != 'Income', 'Amount'] *= -1
    net_income_df = net_income_df.groupby(['Month'])[['Amount']].sum().reset_index()
    net_income = net_income_df.loc[net_income_df['Month']== net_income_df['Month'].max(), 'Amount'].values[0]

    fig, ax = plt.subplots()
    
    sns.barplot(cash_flow_df,
                x='Month',
                y='Amount',
                hue = 'Category',
                hue_order=palette.keys(),
                errorbar=None,
                palette=palette)
    # setting custom plot title, labels, and text
    ax.set_title('Monthly Cash Flow')
    ax.set_xlabel('Month')
    ax.set_ylabel('Amount ($)')
    ax.set_ylim(top=cash_flow_df['Amount'].max() + (cash_flow_df['Amount'].max() * 0.3))
    # display net income text
    net_income_text = ax.text(x=0.05, 
                              y=0.95,
                              s='${:.2f}'.format(net_income),
                              fontdict=
                                {
                                  "color": '#e33434' if net_income < 0 else '#4bd02b',
                                  "fontsize":20
                                },
                              horizontalalignment='left',
                              verticalalignment='top',
                              transform=ax.transAxes
                            )
    # get box of net_income_text
    renderer = plt.gcf().canvas.get_renderer()
    bbox_1 = net_income_text.get_window_extent(renderer=renderer)
    # getting dimensions of net_income_text box
    bbox_width = bbox_1.width / ax.figure.dpi / ax.get_window_extent().width
    bbox_height = bbox_1.height / ax.figure.dpi / ax.get_window_extent().height

    # adding net_income subtext
    ax.text(
        x=0.05 + bbox_width +  0.27,
        y=0.95 - bbox_height - 0.02,
        s=f"{calendar.month_abbr[net_income_df['Month'].max()]} Net Income",
        fontdict={"fontsize":12},
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax.transAxes
    )
    for container in ax.containers:
        ax.bar_label(container)

    return fig