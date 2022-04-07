from typing import (
    List,
    Tuple,
)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class Transformer:

    def __init__(self):
        self

    def read_orders(self) -> pd.DataFrame:
        orders = pd.read_csv('/Users/mhaikunchorn/Desktop/intern-tech-tests/data-tech-test/orders.csv', header=0)
        return orders

    def enrich_orders(self, orders: pd.DataFrame, col_name: str, value: List[str]) -> pd.DataFrame:
        """
        Adds a column to the data frame

        Args:
            orders (pd.Dataframe): The dataframe to be enriched
            col_name (str): Name of the new enriched column
            value (List[str]): Data to go into the new column

        Returns:
            The enriched dataframe
        """
        self.orders = orders
        self.col_name = col_name
        self.value = value
        enriched = self.orders.assign(col_name = value)
        enriched.rename(columns = {'col_name': col_name}, inplace = True)

        return enriched

    def split_customers(self, orders: pd.DataFrame, threshold: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Splits customers into two groups based on a threshold

        Args:
            orders (pd.DataFrame): The dataframe to be split
            threshold (int): Value to split the customer base on

        Returns:
            Tuple containing the split dataframes
        """
        self.orders = orders.astype({'amount': 'int'})
        self.threshold = threshold
        low_spending_customers = self.orders[self.orders['amount'] < self.threshold]
        high_spending_customers = self.orders[self.orders['amount'] >= self.threshold]
        return low_spending_customers, high_spending_customers

        # As the average amount spent is 750, I have set the threshold to 900 as the higher spending customers.

# ================== BONUS TASK ==================

# Create an instance and read in the data
transformer = Transformer()
data = transformer.read_orders()

# Checking the data types to convert to correct appropriate one
# print(data.dtypes)

# Converting data types
data = data.astype({'date': 'datetime64[ns]'})

# Checking this has been properly converted
# print(data.dtypes)

# Q1. Who was the highest spender?
highest_spender = data[data['amount'] == data.amount.max()]
print(f"The highest spending customer is: \n {highest_spender}\n\n")

# Visualisation
high_color = ['#debbfb' if (x < max(data.amount)) else '#9774e8' for x in data.amount]
ax = sns.barplot(x='customer',
                 y='amount',
                 data=data,
                 palette=high_color)

ax.set(xlabel='Customers',
       ylabel='Order amount',
       title='Total order amount per customer')

ax.axhline(1100, ls='--', color='#9774e8', label="1100")


ax.legend(title='Highest amount spent',bbox_to_anchor=(1,0.6))

plt.show()

# Q2. Which customer placed the lowest order amount?
lowest_spender = data[data['amount'] == data.amount.min()]
print(f"The customer who placed the lowest order amount:\n {lowest_spender}\n\n")

# Visualisation
low_colour = ['#debbfb' if (x > min(data.amount)) else '#9774e8' for x in data.amount]
ax2 = sns.barplot(x='customer',
                  y='amount',
                  data=data,
                  palette=low_colour,
                  label='Lowest order customer')
ax2.set(xlabel='Customers',
        ylabel='Order amount',
        title='Total order amount per customer')
ax2.axhline(400, ls='--', color='#9774e8', label="Lowest amount spent")
ax2.legend(bbox_to_anchor=(1,0.6))

plt.show()

# Q3. What was the average order amount across all customers?
avg_order_amount = data['amount'].mean()
print(f"The average order amount across all customers is {avg_order_amount}\n\n")

# Visualisation
ax3 = sns.barplot(x='customer', y='amount', data=data, color="#debbfb")
ax3.set(xlabel='Customers',
       ylabel='Order amount',
       title='Total order amount per customer')
ax3.axhline(avg_order_amount, ls='--', color='#9774e8', label="750")
ax3.legend(title="Average order amount",bbox_to_anchor=(1,0.5))

plt.show()

# Q4. Which customer placed the earliest order?
earliest_order = data[data['date'] == data.date.min()]
print(f"The earliest order was placed by:\n {earliest_order}\n\n")

# Visualisation
ax4 = sns.scatterplot(x='date',
                      y='customer',
                      data=data,
                      hue='amount',
                      palette='Purples_d',
                      size='amount',
                      sizes=(20,200))
ax4.set(xlabel='Date',
       ylabel='Customers',
       title='Customer order by date')
ax4.legend(bbox_to_anchor=(1,0.7))

plt.xticks(rotation=45)
plt.show()

# Q5. In which month did most of the orders happen (the year can be ignored)?
# Extracting the month from the date column and creating a new month column
data['month'] = pd.DatetimeIndex(data['date']).month
data['month'] = data['month'].replace([1,2,3,4,5,6,7,8,9,10,11,12],
                                    ['January',
                                     'February',
                                     'March',
                                     'April',
                                     'May',
                                     'June',
                                     'July',
                                     'August',
                                     'September',
                                     'October',
                                     'November',
                                     'December'])
highest_month = data.groupby(['month'], as_index=False)['amount'].sum()

# Visualisation
high_color2 = ['#debbfb' if (x < max(highest_month.month)) else '#9774e8' for x in highest_month.month]
ax5 = sns.barplot(
    x='month',
    y='amount',
    data=highest_month,
    ci= False,
    palette=high_color2,
    dodge=False,
    order=['January',
           'February',
           'June',
           'December'])

ax5.set(xlabel='Month',
        ylabel='Order amount',
        title='Total orders per month')
ax5.axhline(2600, ls='--', color='#9774e8', label='2600')
ax5.legend(title='Highest order amount', bbox_to_anchor=(1,0.6))

plt.show()

print(f'The month with the most orders was December at {highest_month.amount.max()}')




if __name__ == '__main__':
    transformer = Transformer()
    data = transformer.read_orders()

    countries = ['GBR', 'AUS', 'USA', 'GBR', 'RUS', 'GBR', 'KOR', 'NZ']
    data = transformer.enrich_orders(data, 'Country', countries)

    threshold = 900  # Change this value
    low_spending_customers, high_spending_customers = transformer.split_customers(data, threshold)


