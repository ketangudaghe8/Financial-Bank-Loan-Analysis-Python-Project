# Bank Loan Analysis

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

df = pd.read_excel("C:/Users/ketan/Downloads/Portfolio Project/Python Project/financial_loan.xlsx")

data = pd.DataFrame(df)
# print(data)

print("No of rows :", df.shape[0])

print(df.dtypes)

print(data.describe())

### KPIs
# 1) Total Loan Applications

Total_loan_applications = data["id"].count()
print("Total Loan Application =", Total_loan_applications)

2) MTD Loan Applications

Latest_issue_date = data["issue_date"].max()
Latest_year = Latest_issue_date.year
Latest_month = Latest_issue_date.month

MTD_ = data[(data['issue_date'].dt.year == Latest_year) & (data["issue_date"].dt.month == Latest_month)]

MTD_applications = MTD_['id'].count()

print(f"MTD Loan Applications (for {Latest_issue_date.strftime("%B %Y")}) : {MTD_applications}")


# 3) Total funded Amount

Total_funded_amount = data["loan_amount"].sum()
TFA_millions = Total_funded_amount/1000000
print("Total Funded Amount: ${:.2f}M".format(TFA_millions))


# MTD Total Funded Amount

Latest_issue_date = data["issue_date"].max()
Latest_year = Latest_issue_date.year
Latest_month = Latest_issue_date.month

MTD_ = data[(data['issue_date'].dt.year == Latest_year) & (data["issue_date"].dt.month == Latest_month)]

MTD_total_funded_Amount = MTD_["loan_amount"].sum()
MTD_total_funded_Amount_millions = MTD_total_funded_Amount/1000000
print("MTD Total Funded Amount : ${:.2f}M".format(MTD_total_funded_Amount_millions))


# 4) Total Amount Recieved

Total_Payment_amount = data["total_payment"].sum()
TPA_millions = Total_Payment_amount/1000000
print("Total Payment Amount : ${:.2f}M".format(TPA_millions))

#MTD Total_payment_Amount

Latest_issue_date = data["issue_date"].max()
Latest_year = Latest_issue_date.year
Latest_month = Latest_issue_date.month

MTD_ = data[(data['issue_date'].dt.year == Latest_year) & (data["issue_date"].dt.month == Latest_month)]

MTD_total_payment_Amount = MTD_["total_payment"].sum()
MTD_total_payment_Amount_millions = MTD_total_payment_Amount/1000000
print("MTD Total Payment Amount : ${:.2f}M".format(MTD_total_payment_Amount_millions))

# 5) Average Interest Rate
Avg_int_rate = data["int_rate"].mean()*100
print("Average Interest Rate :  {:.2f}%".format(Avg_int_rate))

# 6) Average Debt-TO-Income-Ratio(DTI)

Avg_DTI = data["dti"].mean()*100
print("Average Debt to Income Ratio : {:.2f}%".format(Avg_DTI))


## Good Loan Calculation

good_loans = data[data["loan_status"].isin(["Fully Paid","Current"])]

total_loan_applications = data["id"].count()

good_loan_applications = good_loans['id'].count()
good_loan_funded_amount = good_loans["loan_amount"].sum()
good_loan_recieved = good_loans["total_payment"].sum()

good_loan_funded_amount_millions = good_loan_funded_amount/1000000
good_loan_recieved_millions = good_loan_recieved/1000000

good_loan_percentage = (good_loan_applications/total_loan_applications)*100

print("Good Loan Applications :" , good_loan_applications)
print("Good loan Funded Amount (in millions) :${:.2f}M".format(good_loan_funded_amount_millions) )
print("Good loan Recieved Amount (in millions) :${:.2f}M".format(good_loan_recieved_millions) )
print("Percentage of Good Loan Applications :{:.2f}%".format(good_loan_percentage) )


# Bad Loan Applications

bad_loans = data[data["loan_status"].isin(["Charged Off"])]

total_loan_applications = data["id"].count()

bad_loan_applications = bad_loans['id'].count()
bad_loan_funded_amount = bad_loans["loan_amount"].sum()
bad_loan_recieved = bad_loans["total_payment"].sum()

bad_loan_funded_amount_millions = bad_loan_funded_amount/1000000
bad_loan_recieved_millions = bad_loan_recieved/1000000

bad_loan_percentage = (bad_loan_applications/total_loan_applications)*100

print("Bad Loan Applications :" , bad_loan_applications)
print("Bad loan Funded Amount (in millions) :${:.2f}M".format(bad_loan_funded_amount_millions) )
print("Bad loan Recieved Amount (in millions) :${:.2f}M".format(bad_loan_recieved_millions) )
print("Percentage of Bad Loan Applications :{:.2f}%".format(bad_loan_percentage) )


# Monthly Trend by issue_date for total funded amount

monthly_funded = (
data.sort_values('issue_date')
    .assign(month_name = lambda x : x['issue_date'].dt.strftime('%b %y'))
    .groupby("month_name", sort = False)["loan_amount"]
    .sum()
    .div(1000000)
    .reset_index(name= 'loan_amount_millions')
    )

plt.figure(figsize=(10,5))
plt.fill_between(monthly_funded['month_name'], monthly_funded['loan_amount_millions'], color = 'skyblue', alpha = 0.5)
plt.plot(monthly_funded['month_name'],monthly_funded['loan_amount_millions'],color = 'blue', linewidth = 2)

for i, row in monthly_funded.iterrows():
    plt.text(i, row['loan_amount_millions'] + 0.1, f"{row['loan_amount_millions']:.2f}",
          ha = 'center', va = 'bottom', fontsize = 9, rotation = 0, color = 'black')

plt.title('Total Funded Amount by Month', fontsize=14)
plt.xlabel('Month')
plt.ylabel('Funded Amount (Millions)')
plt.xticks(ticks=range(len(monthly_funded)), labels=monthly_funded['month_name'],rotation=45)
plt.grid(True, linestyle='--', alpha = 0.6)
plt.tight_layout()
plt.show()



# Monthly trend by issue_date for total amount recieved

monthly_funded = (
data.sort_values('issue_date')
    .assign(month_name = lambda x : x['issue_date'].dt.strftime('%b %y'))
    .groupby("month_name", sort = False)["total_payment"]
    .sum()
    .div(1000000)
    .reset_index(name= 'Recieved_amount_millions')
    )

plt.figure(figsize=(10,5))
plt.fill_between(monthly_funded['month_name'], monthly_funded['Recieved_amount_millions'], color = 'lightgreen', alpha = 0.5)
plt.plot(monthly_funded['month_name'],monthly_funded['Recieved_amount_millions'],color = 'green', linewidth = 2)

for i, row in monthly_funded.iterrows():
    plt.text(i, row['Recieved_amount_millions'] + 0.1, f"{row['Recieved_amount_millions']:.2f}",
          ha = 'center', va = 'bottom', fontsize = 9, rotation = 0, color = 'black')

plt.title('Total Recieved Amount by Month', fontsize=14)
plt.xlabel('Month')
plt.ylabel('Recieved Amount (Millions)')
plt.xticks(ticks=range(len(monthly_funded)), labels=monthly_funded['month_name'],rotation=45)
plt.grid(True, linestyle='--', alpha = 0.6)
plt.tight_layout()
plt.show()



#Monthly trend for total_application_Count

monthly_funded = (
data.sort_values('issue_date')
    .assign(month_name = lambda x : x['issue_date'].dt.strftime('%b %y'))
    .groupby("month_name", sort = False)["id"]
    .count()
    .reset_index(name= 'Loan_Applications_Count')
    )

plt.figure(figsize=(10,5))
plt.fill_between(monthly_funded['month_name'], monthly_funded['Loan_Applications_Count'], color = 'orange', alpha = 0.5)
plt.plot(monthly_funded['month_name'],monthly_funded['Loan_Applications_Count'],color = 'darkorange', linewidth = 2)

for i, row in monthly_funded.iterrows():
    plt.text(i, row['Loan_Applications_Count'] + 0.1, f"{row['Loan_Applications_Count']:.2f}",
          ha = 'center', va = 'bottom', fontsize = 9, rotation = 0, color = 'black')

plt.title('Total Loan Applications by Month', fontsize=14)
plt.xlabel('Month')
plt.ylabel(' Number of Applications')
plt.xticks(ticks=range(len(monthly_funded)), labels=monthly_funded['month_name'],rotation=45)
plt.grid(True, linestyle='--', alpha = 0.6)
plt.tight_layout()
plt.show()


# Statewise-Analysis of Total Funded Amount

State_funding = data.groupby('address_state')["loan_amount"].sum().sort_values(ascending=True)
State_funding_thousands = State_funding/1000

plt.figure(figsize=(10,8))
bars = plt.barh(State_funding_thousands.index,State_funding_thousands.values,color = 'lightcoral')

for bar in bars :
    width = bar.get_width()
    plt.text(width + 10, bar.get_y() + bar.get_height()/ 2,
              f'{width:,.0f}K', va ="center", fontsize = 9)

plt.title('Total Funded Amount by State (in thoudsands)')
plt.xlabel('Funded Amount ($ \'000)')
plt.ylabel('State')
plt.tight_layout()
plt.show()


# State-wise Total Amount recieved

State_Payment = data.groupby('address_state')["total_payment"].sum().sort_values(ascending=True)
State_payment_thousands = State_Payment/1000

plt.figure(figsize=(10,8))
bars = plt.barh(State_payment_thousands.index,State_payment_thousands.values,color = 'lightgreen')

for bar in bars :
    width = bar.get_width()
    plt.text(width + 10, bar.get_y() + bar.get_height()/ 2,
              f'{width:,.0f}K', va ="center", fontsize = 9)

plt.title('Total Recieved Amount by State (in thoudsands)')
plt.xlabel('Recieved Amount ($ \'000)')
plt.ylabel('State')
plt.tight_layout()
plt.show()



# State-wise Loan Applications


State_Applications = data.groupby('address_state')["id"].count().sort_values(ascending=True)

plt.figure(figsize=(10,8))
bars = plt.barh(State_Applications.index,State_Applications.values,color = 'orange')

for bar in bars :
    width = bar.get_width()
    plt.text(width + 10, bar.get_y() + bar.get_height()/ 2,
              f'{width:,.0f}', va ="center", fontsize = 9)

plt.title('Total Applications by State')
plt.xlabel('Applications')
plt.ylabel('State')
plt.tight_layout()
plt.show()


# Loan term Analysis By Total funded Amount

term_funding_millions = df.groupby('term')['loan_amount'].sum()/1000000

plt.figure(figsize=(5,5))
plt.pie(
    term_funding_millions,
    labels=term_funding_millions.index,
    autopct=lambda p : f"{p:.1f}%\n${p*sum(term_funding_millions)/100:.1f}M",
    startangle= 90,
    wedgeprops={"width":0.4}
)

plt.gca().add_artist(plt.Circle((0,0),0.70,color = "white"))
plt.title("Total Funded Amount by Term (in $ Millions) ")
plt.show()


# Loan Term Analysis By Total Amount Recieved

term_payment_millions = df.groupby('term')['total_payment'].sum()/1000000

plt.figure(figsize=(5,5))
plt.pie(
    term_payment_millions,
    labels=term_payment_millions.index,
    autopct=lambda p : f"{p:.1f}%\n${p*sum(term_payment_millions)/100:.1f}M",
    startangle= 90,
    wedgeprops={"width":0.4}
)

plt.gca().add_artist(plt.Circle((0,0),0.70,color = "white"))
plt.title("Total Recieved Amount by Term (in $ Millions) ")
plt.show()


# Loan Term Analaysis By Application Count

term_applications = df.groupby('term')['id'].count()

plt.figure(figsize=(5,5))
plt.pie(
    term_applications,
    labels=term_applications.index,
    autopct=lambda p : f"{p:.1f}%\n{p*sum(term_applications)/100:.1f}",
    startangle= 90,
    wedgeprops={"width":0.4}
)

plt.gca().add_artist(plt.Circle((0,0),0.70,color = "white"))
plt.title("Term-wise Applications")
plt.show()



# Employment Period Vs Total Funded Amount


Employee_funding = data.groupby('emp_length')["loan_amount"].sum().sort_values()/1000


plt.figure(figsize=(10,6))
bars = plt.barh(Employee_funding.index,Employee_funding.values,color = 'coral')

for bar in bars :
    width = bar.get_width()
    plt.text(width + 5, bar.get_y() + bar.get_height()/ 2,
              f'${width:,.0f}K', va ="center", fontsize = 9)

plt.title('Funded Amount By Employment Period')
plt.xlabel('Funded Amount (in thousands)')
plt.grid(axis="x" , linestyle = "--", alpha=0.5)
plt.tight_layout()
plt.show()



# Employment Period Vs Total Amount Recieved

Employee_Amount_Recieved = data.groupby('emp_length')["total_payment"].sum().sort_values()/1000


plt.figure(figsize=(10,6))
bars = plt.barh(Employee_Amount_Recieved.index,Employee_Amount_Recieved.values,color = 'skyblue')

for bar in bars :
    width = bar.get_width()
    plt.text(width + 5, bar.get_y() + bar.get_height()/ 2,
              f'${width:,.0f}K', va ="center", fontsize = 9)

plt.title('RecievedAmount By Employment Period')
plt.xlabel('Amount Recieved (in thousands)')
plt.grid(axis="x" , linestyle = "--", alpha=0.5)
plt.tight_layout()
plt.show()



# Loan Purpose Vs Total Funded Amount

Purpose_funding_millions = data.groupby('purpose')["loan_amount"].sum().sort_values()/1000000


plt.figure(figsize=(10,6))
bars = plt.barh(Purpose_funding_millions.index,Purpose_funding_millions.values,color = 'blue')

for bar in bars :
    width = bar.get_width()
    plt.text(width + 0.1, bar.get_y() + bar.get_height()/ 2,
              f'${width:,.0f}M', va ="center", fontsize = 9)

plt.title('Funded Amount by Loan Purpose')
plt.xlabel('Funded Amount (in millions)')
plt.ylabel("Loan Purpose")
plt.grid(axis="x" , linestyle = "--", alpha=0.6)
plt.tight_layout()
plt.show()



# Loan Purpose Vs Recieved Amount

Purpose_Recieved_millions = data.groupby('purpose')["total_payment"].sum().sort_values()/1000000


plt.figure(figsize=(10,6))
bars = plt.barh(Purpose_Recieved_millions.index,Purpose_Recieved_millions.values,color = 'skyblue')

for bar in bars :
    width = bar.get_width()
    plt.text(width + 0.1, bar.get_y() + bar.get_height()/ 2,
              f'${width:,.0f}M', va ="center", fontsize = 9)

plt.title('Recieved Amount by Loan Purpose')
plt.xlabel('Recieved Amount (in millions)')
plt.ylabel("Loan Purpose")
plt.grid(axis="x" , linestyle = "--", alpha=0.6)
plt.tight_layout()
plt.show()



## Total Funded Amount Vs Home Ownership

home_funding = data.groupby('home_ownership')['loan_amount'].sum().reset_index()
home_funding['loan_amount_millions'] = home_funding['loan_amount']/1000000

fig = px.treemap(
    home_funding,
    path=['home_ownership'],
    values= 'loan_amount_millions',
    color= 'loan_amount_millions',
    color_continuous_scale= 'Blues',
    title='Total Funded Amount Vs Home Ownership'

)
fig.show()


#Total Amount recieved Vs Home-Ownership

home_payment = data.groupby('home_ownership')['total_payment'].sum().reset_index()
home_payment['loan_payment_millions'] = home_payment['total_payment']/1000000

fig = px.treemap(
    home_payment,
    path=['home_ownership'],
    values= 'loan_payment_millions',
    color= 'loan_payment_millions',
    color_continuous_scale= 'Blues',
    title='Total Amount Recieved Vs Home Ownership'

)

fig.show()