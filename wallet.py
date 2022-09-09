'''
@@@ Author: Vincent
@@@ Date  : 8 Sep 2022
@@@ About : Calculating All Financial Expense
'''
from datetime import datetime
import xlrd
import codebook

class MyWallet():
    '''
    year             <int>     :  year of the Wallet
    workbook         <object>  :  xlsx workbook
    worksheet        <object>  :  xlsx worksheet
    max_ros          <int>     :  maximum rows in xlsx file
    monthly_remain   <float>   :  monthly money remains
    monthly_initial  <float>   :  monthly money initial saving
    monthly_final    <float>   :  monthly money final saving
    monthly_salary   <float>   :  monthly money salary
    annual_remain    <float>   :  annual money remains (sum of monthly_remains)
    all_records      <list>    :  all records in a xlsx file
    '''
    def __init__(self,year):
        self.year = year
        self.workbook = None
        self.worksheet = None
        self.max_row = 0

        self.monthly_remain = 0
        self.monthly_initial = 0
        self.monthly_final = 0
        self.monthly_salary = 0
        self.annual_remain = 0
        self.monthly_expense = []

        self.all_records = []

    def check_xlsx_exist(self,month):
        monthly_file = './{}/{}.xlsx'.format(self.year,month)
        try:
            self.workbook = xlrd.open_workbook(monthly_file)
            print("[Wallet] {} FOUND".format(monthly_file))
            return True
        except:
            print("[Wallet] {} NOT FOUND".format(monthly_file))
            return False

    def calculate_annual_remain(self):
        x = 1
        # Go through all the months
        while x <= 12:
            month = list(codebook.months.keys())[list(codebook.months.values()).index(x)]
            file_found = self.check_xlsx_exist(month)
            if file_found:
                monthly_file = './{}/{}.xlsx'.format(self.year,month)
                print("[Wallet] Reading file: {}".format(monthly_file))
                self.workbook = xlrd.open_workbook(monthly_file)
                self.worksheet = self.workbook.sheet_by_index(0)
                self.get_max_row()
                self.calculate_monthly_remain()
                self.annual_remain += self.monthly_remain
                self.annual_remain = round(self.annual_remain,2)
            else:
                # Ignore that month
                self.annual_remain += 0
            x += 1
        print("[Wallet] Monthly Remain: ${}".format(self.monthly_remain))

    def get_monthly_salary(self):
        salary_find = False
        for i in range(0,len(self.all_records)):
            if (self.all_records[i][0] == 'salary')or(self.all_records[i][0] == 'Salary'):
                self.monthly_salary = self.all_records[i][3]
                print("[Wallet] Monthly Salary: $ {:.2f}".format(self.monthly_salary))
                salary_find = True

        # Approximate value
        if not salary_find:
            print("[Wallet] No Salary find. Use default value = {}".format(4088))
            self.monthly_salary = 4088
                
    def calculate_monthly_remain(self):
        self.monthly_initial = self.all_records[0][2]
        # TODO: Monthly_final should use last non-zero value
        self.monthly_final = self.all_records[-1][4]
        self.monthly_remain = self.monthly_final - self.monthly_initial
        self.monthly_remain = round(self.monthly_remain,2)
        print("[Wallet] Monthly Initial: ${:.2f} | Monthly Final: $ {:.2f} | Monthly Remain: $ {:.2f}".format(self.monthly_initial,self.monthly_final,self.monthly_remain))

    def get_max_row(self):
        self.all_records = []
        if self.worksheet is not None:
            # Unreasonably large value
            max_data = 100
            self.max_row = 0
            try:
                for i in range(0,max_data):
                    k = []
                    for j in range(0,5):
                        x = self.worksheet.cell_value(i, j)
                        k.append(x)
                    self.all_records.append(k)
                    self.max_row += 1
            except:
                pass
    
    def get_monthly_expense(self,month,show_detail=True,max_data=10):
        '''
        Note that month has to be short form using the first 3 characters
        Example: Jan, Feb, Sep, Dec
        '''
        monthly_file = './{}/{}.xlsx'.format(self.year,month)
        print("[Wallet] Reading file: {}".format(monthly_file))

        self.workbook = xlrd.open_workbook(monthly_file)
        self.worksheet = self.workbook.sheet_by_index(0)

        self.get_max_row()

        monthly_json_output = '{'

        try:
            z = 0
            # Get the latest max_data
            for i in reversed(range((self.max_row-max_data),self.max_row)):
                print("[Wallet]", end='\t')
                single_expense = []
                for j in range(0,5):
                    # Item
                    if j == 0:
                        monthly_json_output += "\"item{}\":\"".format(z) + str(self.worksheet.cell_value(i, j)) + '\",'
                        single_expense.append(str(self.worksheet.cell_value(i, j)))
                    # Date
                    elif j == 1:
                        # Convert date <int> to date <str>
                        date = datetime.fromordinal(datetime(1900,1,1).toordinal() + int(self.worksheet.cell_value(i, j)) - 2)
                        # Remove Hour:Minute:Second because it is not necessary
                        date = date.date()
                        # Write as a json message
                        monthly_json_output += "\"date{}\":\"".format(z) + str(date) + '\",'
                        if show_detail:
                            print(date, end='\t')
                            single_expense.append(str(date))
                    # Previous Saving
                    elif j == 2:
                        money = self.worksheet.cell_value(i, j)
                        money = round(money,2)
                        monthly_json_output += "\"previous{}\":\"".format(z) + '$' + str(money) + '\",'
                        single_expense.append(money)
                    # Cost
                    elif j == 3:
                        money = self.worksheet.cell_value(i, j)
                        money = round(money,2)
                        monthly_json_output += "\"cost{}\":\"".format(z) + '$' + str(money) + '\",'
                        single_expense.append(money)
                    # Current Saving
                    elif j == 4:
                        money = self.worksheet.cell_value(i, j)
                        money = round(money,2)
                        monthly_json_output += "\"current{}\":\"".format(z) + '$' + str(money) + '\",'
                        single_expense.append(money)
                    else:
                        pass
                     # Ignore the date because it is printed previously
                    if (show_detail and j != 1):
                        try:
                            print('{:.2f}'.format(float(self.worksheet.cell_value(i, j))), end='\t')
                        except:
                            print(self.worksheet.cell_value(i, j), end='\t')

                self.monthly_expense.append(single_expense)
                if show_detail:
                    print('')
                
                z += 1

            # Wrap Up the JSON message
            if monthly_json_output is not None:
                # Remove the last comma
                monthly_json_output = monthly_json_output.rstrip(monthly_json_output[-1])
                # Add } to the json message
                monthly_json_output += '}'
            return monthly_json_output

        except Exception as e:
            print('')
            if 'out of range' not in str(e):
                print("[Wallet] Failed To Extract Data. Reason: {}".format(e))
            return monthly_json_output









