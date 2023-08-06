import datetime
import mb.pandas as pd
import wml.visionml as wv
from .train_loop import *

__all__ = ['reset_tables','convert_tables_to_data','train_for_all_items']


def reset_tables(start_date='2023-06-19',date_2='2023-06-20',logger=None):
    """
    Function to get the inital config of the tables in pp_project.
    Args:
        start_date : date from which the data is required
    Returns:
        None
    """

    d1 =datetime.datetime.strptime(start_date,'%Y-%m-%d').date()
    #d2 =datetime.datetime.strptime(d2,'%Y-%m-%d').date()

    dates_to_add = [d1,d1]
    #dates_closing = [d2,d2]
    
    tx = pd.DataFrame(data=[dates_to_add],columns=['date','closed'])
    if logger:
        logger.info(tx.head())
    tx.to_sql(name='waldorf_report_closed_data_latest',con=wv.ml_engine,schema='pp_tables' ,if_exists='replace',index=False)
    tx.to_sql(name='waldorf_report_closed_data_all',con=wv.ml_engine,schema='pp_tables' ,if_exists='replace',index=False)
    if logger:
        logger.info("Tables resetted to initial config date : {}".format(start_date))

    
    
    
def convert_tables_to_data(logger=None):
    """
    Function to convert the tables to data
    """
    
    #reading tables
    q1 = """SELECT * FROM pp_tables.waldorf_waste_data"""
    q2 = """SELECT * FROM pp_tables.waldorf_drivers_data"""
    t1 = wv.read_sql(q1)
    t2 = wv.read_sql(q2)
    if logger:
        logger.info("Tables read")
 
    t1['date'] = t1['date'].astype(str)
    waste_result_dict = dict(tuple(t1.groupby('date')))
    for key, groupby_obj in waste_result_dict.items():
        waste_result_dict[key] = groupby_obj.drop(columns=['date','covers','consumption_per_cover','scaling_factor'])    
        
    t2['start_date'] = t2['start_date'].astype(str)
    driver_result_dict = dict(tuple(t2.groupby('start_date')))
    for key, groupby_obj in driver_result_dict.items():
        driver_result_dict[key] = groupby_obj.drop(columns=['start_date','site_id','meal_period','label'])

    if logger:
        logger.info("dict created per date for tables")
    
    #get the list of common dates
    final_list=[]
    for key in driver_result_dict:
        if key in waste_result_dict:
            final_list.append(key)

    if logger:
        logger.info("Common dates list created of size : {}".format(len(final_list)))
        
    dict_1 = {}
    for val in final_list:
        dd = driver_result_dict[val]
        wd = waste_result_dict[val]
        wd['actual_covers'] = dd[dd['driver_type']=='ACTUAL_NO_OF_COVERS']['value'].iloc[0]
        wd['no_of_covers'] = dd[dd['driver_type']=='NO_OF_COVERS']['value'].iloc[0]
        dict_1[val]= wd
        
    ## getting the final list with all events for each item is segregated by dict in the list    
    matching_rows = []
    total_names = list(dict_1['2023-06-20']['name'])
    for i in range(len(total_names)):
        for df in dict_1.values():
            matching_rows.extend(df.loc[df['name'] == total_names[i]].to_dict('records'))
            
    if logger:
        logger.info("Final list created of size : {}".format(len(matching_rows)))
        
    dict_to_train={}
    for i in range(len(matching_rows)):
        if matching_rows[i]['name'] not in dict_to_train.keys():
            dict_to_train[matching_rows[i]['name']] = [[matching_rows[i]['actual_production'],
                                                       matching_rows[i]['rework_or_reuse'],
                                                       matching_rows[i]['actual_consumption'],
                                                       matching_rows[i]['waste'],
                                                       matching_rows[i]['actual_covers'],
                                                       matching_rows[i]['no_of_covers']]]
        else:
            dict_to_train[matching_rows[i]['name']].append([matching_rows[i]['actual_production'],
                                                       matching_rows[i]['rework_or_reuse'],
                                                       matching_rows[i]['actual_consumption'],
                                                       matching_rows[i]['waste'],
                                                       matching_rows[i]['actual_covers'],
                                                       matching_rows[i]['no_of_covers']])
            
    columns = ['actual_production','rework_or_reuse','actual_consumption','waste','actual_covers','no_of_covers']
    asd = list(dict_to_train.keys())
    for i in range(len(asd)):
        dict_to_train[asd[i]] = pd.DataFrame(dict_to_train[asd[i]], columns=columns)

    return dict_to_train

def train_for_all_items(dict_to_train,logger=None,*kwargs):
    """
    Function to train for all items
    """
    #training for all items
    list_of_models = []
    for i in range(len(dict_to_train)):
        if logger:
            logger.info("Training for item : {}".format(list(dict_to_train.keys())[i]))
        t_model = linear_train(dict_to_train[list(dict_to_train.keys())[i]],logger=logger,*kwargs)
        list_of_models.append(t_model)
    return list_of_models