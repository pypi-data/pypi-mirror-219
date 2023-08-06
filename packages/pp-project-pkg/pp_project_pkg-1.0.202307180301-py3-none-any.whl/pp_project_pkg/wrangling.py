## function for wrangling data
from dateutil import parser
import mb.pandas as pd

__all__ = ['wrangling_data']

def wrangling_data(queries_res,site_data=None,date = '2023-06-06',logger=None):
    """
    Args:
        query_res: query result from database
    Output:
        wrangled data : csv file
    """
    
    hub_custom_breakdown = queries_res[0]
    site_info = queries_res[1]
    pp_driver_input = queries_res[2]
    food_items = queries_res[3]
    meal_period_configuration = queries_res[4]
    #pp_production_rework = queries_res[5]
    pp_production = queries_res[5]
    pp_rework = queries_res[6]
    waste_data_for_site = queries_res[7]
    
    meal_period_start = meal_period_configuration['waste_disposal_start_time'].values[0]
    meal_period_end = meal_period_configuration['waste_disposal_end_time'].values[0]
    
    meal_period_end_dt =parser.parse(meal_period_end)   
    meal_period_start_dt =parser.parse(meal_period_start)
    
    covers = pp_driver_input[pp_driver_input['driver_type'] == 'NO_OF_COVERS']['value']
    actual_covers = pp_driver_input[pp_driver_input['driver_type'] == 'ACTUAL_NO_OF_COVERS']['value']

    cover_count = None
    if len(actual_covers.values) > 0:
        cover_count = actual_covers.values[0]
    else:
        cover_count = covers.values[0]
    
    pp_rework = pp_rework.drop(columns=['meal_service_id']).reset_index(drop=True)
    pp_production_rework = pd.merge(pp_production, pp_rework, on=['taxonomy_code'])
    name_pd = pd.read_csv('./taxcode_name_mapping.csv')
    name_pd = name_pd.drop(columns=['Unnamed: 0']).reset_index(drop=True)
    name_pd = name_pd.rename(columns={name_pd.columns[1]:'taxonomy_code',name_pd.columns[0]:'name'})
    pp_production_rework = pd.merge(pp_production_rework, name_pd, on=['taxonomy_code'])

    actual_production_and_rework = pp_production_rework.copy()
    actual_production_and_rework['quantity_g'] = actual_production_and_rework['actual_production_kg']*1000
    actual_production_and_rework['rework_g'] = actual_production_and_rework['rework_kg']*1000
    
    joined_df = waste_data_for_site.join(hub_custom_breakdown.set_index('id'), on='reason_guid', how='inner')

    # Filter the joined dataframe based on the 'name' column
    filtered_df = joined_df.loc[joined_df['name'] == 'Overproduction']
     
    if logger and site_data:
        logger.info('Site info {} : {}'.format(site_data['site_id'],site_info['tracker_name'].values[0]))
        logger.info('Cover count for the date {} : {}'.format(site_data['date'],cover_count))
        logger.info('pp_production_rework total : {}'.format(pp_production_rework['rework'].sum()))

    # Filter the filtered dataframe based on the 'local_time' column
    if filtered_df.empty:
        itemised_overproduction = pd.DataFrame(columns=list(waste_data_for_site.columns))
    else:
        itemised_overproduction = filtered_df.loc[(filtered_df['local_time'].dt.time >= meal_period_start_dt.time()) & (filtered_df['local_time'].dt.time <= meal_period_end_dt.time())]
        itemised_overproduction = itemised_overproduction[list(waste_data_for_site.columns)]


    joined_df = food_items.join(itemised_overproduction.set_index('item_id'), on='waste_identifier', how='left',rsuffix='_2')

    # Group the joined dataframe by 'food_item_id' and calculate the sum of 'weight_g' column while replacing null values with 0
    grouped_df = joined_df.groupby('food_item_id')['weight_g'].sum().fillna(0)

    # Convert the resulting series object to a dataframe
    overproduction = pd.DataFrame(grouped_df).reset_index().rename(columns={'weight_g': 'quantity_g'})

    joined_df = pd.merge(food_items, overproduction, how='left', on='food_item_id').fillna(0)

    # Join the resulting dataframe with 'actual_production_and_rework' dataframe on 'taxonomy_code' column and replace null values with 0
    joined_df2 = pd.merge(joined_df, actual_production_and_rework, how='left', on='taxonomy_code').fillna(0)

    #print(joined_df2.columns)
    # Select the required columns from the resulting dataframe
    result_df = joined_df2[[ 'name_x', 'taxonomy_code', 'quantity_g_y', 'rework_g', 'quantity_g_x']]

    #print(result_df.columns)
    # Rename the columns to match the column names in the SQL query
    meal_service_summary = result_df.rename(columns={'name_x': 'name','quantity_g_y': 'actual_production', 'rework_g': 'rework_or_reuse', 'quantity_g_x': 'waste'})

    meal_service_summary_df = meal_service_summary.copy()

    # Calculate the new columns as required
    meal_service_summary_df['covers'] = cover_count
    meal_service_summary_df['actual_consumption'] = meal_service_summary_df['actual_production'] - meal_service_summary_df['rework_or_reuse'] - meal_service_summary_df['waste']
    meal_service_summary_df['consumption_per_cover'] = meal_service_summary_df['actual_consumption'] / cover_count
    meal_service_summary_df['scaling_factor'] = meal_service_summary_df['actual_consumption'] / (cover_count * 1000)

    # Select all columns from the resulting dataframe
    result_df = meal_service_summary_df.loc[:, :]
    result_df['date'] = date

    if logger:
        logger.info("Added date column to the result_df")
        logger.info("result_df : {}".format(result_df.head(2)))
                        
    return result_df