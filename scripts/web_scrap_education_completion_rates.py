from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd

# Using Chrome to access web
driver = webdriver.Chrome()
# Open the website
driver.get('https://data.ers.usda.gov/reports.aspx?ID=17829#P79e3276288334f1d97012f898aafe026_20_69iT1')

cc_df = pd.DataFrame()
sc_df = pd.DataFrame()
hso_df = pd.DataFrame()
nchs_df = pd.DataFrame()
for state in range(2,53):
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/form/div[7]/div/div/div/div[2]/div/table/tbody/tr[1]/td/div/div[2]/table/tbody/tr/td[2]/div/div/p/label/i').click()
    time.sleep(2)
    driver.find_element_by_xpath(f'//*[@id="MainContentPlaceHolder_reportingServicesWrapper1_tbl_menu"]/tbody/tr/td[2]/div/div/div/ul/li[{state}]/label').click()
    time.sleep(2)
    for dataset in range(1,5):
        driver.find_element_by_xpath('//*[@id="MainContentPlaceHolder_reportingServicesWrapper1_tbl_menu"]/tbody/tr/td[4]/div/div/p/label/i').click()
        time.sleep(2)
        driver.find_element_by_xpath(f'//*[@id="MainContentPlaceHolder_reportingServicesWrapper1_tbl_menu"]/tbody/tr/td[4]/div/div/div/ul/li[{dataset}]/label').click()
        time.sleep(2)
        driver.find_element_by_name('ctl00$MainContentPlaceHolder$reportingServicesWrapper1$ReportSubmitButton').click()
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find(id='VisibleReportContentctl00_MainContentPlaceHolder_reportingServicesWrapper1__reportViewer_ctl09')
        tab_data = [[cell.text for cell in row.find_all(["th", "td"])]
                        for row in table.find_all("tr")]
        if dataset == 1:
            cc_df = pd.concat([cc_df,pd.DataFrame(tab_data[16:len(tab_data)-3])])
        elif dataset == 2:
            sc_df = pd.concat([sc_df,pd.DataFrame(tab_data[16:len(tab_data)-3])])
        elif dataset == 3:
            hso_df = pd.concat([hso_df,pd.DataFrame(tab_data[16:len(tab_data)-3])])
        elif dataset == 4:
            nchs_df = pd.concat([nchs_df,pd.DataFrame(tab_data[16:len(tab_data)-3])])

cc_df.columns = ['fips','county', 'rural_urban_code','1970','1980', '1990', '2000', '2014-2018']
sc_df.columns = ['fips','county', 'rural_urban_code','1970','1980', '1990', '2000', '2014-2018']
hso_df.columns = ['fips','county', 'rural_urban_code','1970','1980', '1990', '2000', '2014-2018']
nchs_df.columns = ['fips','county', 'rural_urban_code','1970','1980', '1990', '2000', '2014-2018']

cc_df[['1970','1980', '1990', '2000', '2014-2018']] = cc_df[['1970','1980', '1990', '2000', '2014-2018']].apply(lambda x: pd.to_numeric(x.str.strip('%'), errors = 'coerce'))
sc_df[['1970','1980', '1990', '2000', '2014-2018']] = sc_df[['1970','1980', '1990', '2000', '2014-2018']].apply(lambda x: pd.to_numeric(x.str.strip('%'), errors = 'coerce'))
hso_df[['1970','1980', '1990', '2000', '2014-2018']] = hso_df[['1970','1980', '1990', '2000', '2014-2018']].apply(lambda x: pd.to_numeric(x.str.strip('%'), errors = 'coerce'))
nchs_df[['1970','1980', '1990', '2000', '2014-2018']] = nchs_df[['1970','1980', '1990', '2000', '2014-2018']].apply(lambda x: pd.to_numeric(x.str.strip('%'), errors = 'coerce'))

cc_df.to_excel('/Users/ericbutcher/Education Completion Rates 2014 - 2018/data/completed_college_per_county_2014-2018.xlsx',index=False)
sc_df.to_excel('/Users/ericbutcher/Education Completion Rates 2014 - 2018/data/completed_some_college_per_county_2014-2018.xlsx',index=False)
hso_df.to_excel('/Users/ericbutcher/Education Completion Rates 2014 - 2018/data/completed_high_school_only_per_county_2014-2018.xlsx',index=False)
nchs_df.to_excel('/Users/ericbutcher/Education Completion Rates 2014 - 2018/data/not_complete_high_school_per_county_2014-2018.xlsx',index=False)
