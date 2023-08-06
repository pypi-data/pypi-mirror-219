import wml.visionml as wv
import datetime
import mb.pandas as pd
from .pp_tables import queries
from .wrangling import wrangling_data

__all__ = ['site_date_res','check_if_valid_date','check_report_close_date','create_date_table',
           'download_upload_dates_report','compare_report_dates','upload_waste_data','get_drivers_data','upload_drivers_data']


def site_date_res(site_id= 30607):
    """
    Get the site date report closure data
    Args:
        site_id : Site id for fetching the date wise result. Site_id : 30607 (Waldof Astoria)
    
    Returns:
        pd.DateFrame
    """
    q1 = """
    select s.start_date,s.id,s.meal_service_state, s.closed,s.updated from pp_meal_service.view_current_state cs
               join pp_meal_service.view_service s on s.view_current_state_id = cs.id
		       where cs.site_id = {} 
               """.format(site_id)
    return wv.read_sql(q1,wv.ml_engine)

def check_if_valid_date(site_res, date):
    """
    Check if the date (str) has closed the report.

    Args:
        site_res: complete report of the site_data_res
        date: string value of date. format : '2023-06-06'
    
    Output:
        Bool
    """

    k =datetime.datetime.strptime(date,'%Y-%m-%d').date()
    l = site_res[site_res['start_date']==k]
    
    l_d = l['closed'].iloc[0]
    
    if pd.isnull(l_d):
        return False
    
    if  (l_d).to_pydatetime().date() < k:
        return False
    
    return True

def create_date_table(start_date='2023-06-06', end_date='2023-12-31'):
    """
    Creates a date table with the start_date and end_date as the range.
    Args:
        start_date: start date of the date table. format : '2023-06-06'
        end_date: end date of the date table. format : '2023-06-06'
    Output:
        pd.DataFrame
    """    
    date_index = pd.date_range(start=start_date, end=end_date, freq='D')
    df = pd.DataFrame({'date': date_index.date,'closed':None})
    return df

def check_report_close_date(site_res,start_date='2023-06-06', end_date='2023-12-31'):
    """
    Check if the dates has closed the report.

    Args:
        site_res: complete report of the site_data_res
        date: string value of date. format : '2023-06-06'.
        today: string value of today's date. format : '2023-06-06'
    Output:
        df : pd.DataFrame
    """
    
    create_date_table_res = create_date_table(start_date=start_date,end_date=end_date)
    site_res_date = site_res[['start_date','closed','meal_service_state']]
    today = datetime.datetime.today().date()
    start_date =datetime.datetime.strptime(start_date,'%Y-%m-%d').date()
    site_res_date_new = site_res_date[(site_res_date['start_date']<=today) & (site_res_date['start_date']>=start_date) & 
                                      (site_res_date['meal_service_state']=='REPORT')]
    for i in range(len(site_res_date_new)):
        k = site_res_date_new.iloc[i]['start_date']
        l = site_res_date_new.iloc[i]['closed']
        if l is not None or l is not pd.NaT:
            l = l.to_pydatetime().date()
        else:
            l = None
        create_date_table_res.loc[create_date_table_res['date']==k,'closed']=l
    return create_date_table_res

def compare_report_dates(rep_new,rep_old = 'site_30607_report_dates'):
    """
    Compare two report dates and return the difference in days.
    Args:
        rep_new : newly created on todays date
        rep_old : table on the production project pp_tables schema
    Returns:
        df : pd.DataFrame of newly closed report dates
    """
    merged_df = pd.merge(rep_new, rep_old, on='date', how='left', indicator=True)
    result_df = merged_df[merged_df['_merge'] == 'left_only'].drop(columns='_merge')
    result_df.rename(columns={'closed_x':'closed'},inplace=True)
    result_df = result_df[result_df['closed'].notnull()]
    result_df = result_df[['date','closed']]
    return result_df

def download_upload_dates_report(res_new,logger=None):
    """
    Download the report of the dates of the result of the compared report 
    Args:
        res_rep : result of the compared report
    Returns:
        none
    """
    q1 = """ 
    SELECT * FROM pp_tables.waldorf_report_closed_data_all
    """
    download_file = wv.read_sql(q1,wv.ml_engine)
    res_rep = compare_report_dates(res_new,download_file)
    if logger:
        logger.info("Uploading records total : {}".format(len(res_rep)))
    res_rep.to_sql(name='waldorf_report_closed_data_latest',con=wv.ml_engine,schema='pp_tables' ,if_exists='replace',index=False)
    res_rep.to_sql(name='waldorf_report_closed_data_all',con=wv.ml_engine,schema='pp_tables' ,if_exists='append',index=False)
    return res_rep
    
def upload_waste_data(res_rep,reset=False,logger=None):
    """
    function to get the new waste data for each date which are not there in DB and upload to the database
    
    Args:
        res_rep : result of the compared report
        reset : if True, it will delete the existing data and upload the new data
    Returns:
        None
    """
    
    ##fetching the dates which are not there in DB
    dates = list(res_rep['date'])
    for i in range(len(dates)):
        date_str = dates[i].strftime('%Y-%m-%d')
        if logger:
            logger.info("Uploading date : {}".format(date_str))
        a = queries(date=date_str)
        queries_res = a.run_all()
        queries_date = a.date
        res= wrangling_data(queries_res,date=queries_date)
        if reset and i==0:
            res.to_sql(name='waldorf_waste_data',con=wv.ml_engine,schema='pp_tables' ,if_exists='replace',index=False)    
        res.to_sql(name='waldorf_waste_data',con=wv.ml_engine,schema='pp_tables' ,if_exists='append',index=False)
        
        #uploading drivers data
        res_driver = get_drivers_data(date=date_str)
        if reset and i==0:
            res_driver.to_sql(name='waldorf_drivers_data',con=wv.ml_engine,schema='pp_tables' ,if_exists='replace',index=False)
        res_driver.to_sql(name='waldorf_drivers_data',con=wv.ml_engine,schema='pp_tables' ,if_exists='append',index=False)

        if logger:
            logger.info("Uploaded date : {}".format(date_str))
    if logger:
        logger.info("Uploaded records total : {}".format(len(dates)))
    
def get_drivers_data(site_id= 30607, date='2023-06-06' ,logger=None):
    """ 
    Function to get the data for the drivers for the site
    Args:
        site_id : site id of the site
        date : date for which the data is required

    Returns:
        df : pd.DataFrame
    """
    
    q1 = """
    SELECT 
        vs.start_date, 
        vcs.site_id, 
        vmpc.meal_period, 
        vd.driver_type, 
        (jsonb_array_elements(vd.payload)::jsonb)->'label' AS label, 
        (jsonb_array_elements(vd.payload)::jsonb)->'value' AS value 
    FROM 
        pp_meal_service.view_drivers vd, 
        pp_meal_service.view_service vs, 
        pp_meal_service.view_meal_period_configuration vmpc, 
        pp_meal_service.view_current_state vcs 
    where vd.view_service_id  = vs.id 
    and vmpc.view_service_id = vs.id
    and vcs.id  = vs.view_current_state_id
    and vcs.site_id = {}
    and date(vs.start_date) = '{}'
    order by vs.start_date desc """.format(site_id,date)
        
    return wv.read_sql(q1,wv.ml_engine)

def upload_drivers_data(data,logger=None):
    """
    Function to upload the drivers data to the database
    Args:
        data : data to be uploaded
    Returns:
        None
    """
    #columns = ['start_date','site_id','meal_period','driver_type','label','value']
    assert len(data.columns) == 6, "Dataframe should have 6 columns"
    
    data.to_sql(name='waldorf_drivers_data',con=wv.ml_engine,schema='pp_tables' ,if_exists='append',index=False)
    if logger:
        logger.info("Uploaded records total : {}".format(len(data)))
        