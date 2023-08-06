## Running the pp_project.py script

import argparse
from ..pp_project_pkg.utils import check_if_valid_date,site_date_res
from ..pp_project_pkg.pp_tables import queries
from ..pp_project_pkg.wrangling import wrangling_data

def main(args,logger=None):
    if logger:
        logger.info('Running the pp_project pipeline')
        logger.info('Checking the date data')
    date = args.date
    site_id = args.site_id

    check1_df =site_date_res(site_id)
    check1 = check_if_valid_date(check1_df,date)

    if check1==False:
        return None
    
    if logger:
        logger.info('Loading all the queries')

    queries_list_prep = queries(date=date)
    queries_res,site_data = queries_list_prep.run_all()

    if logger:
        logger.info('site_data: {}'.format(site_data))

    wrangling_res = wrangling_data(queries_res=queries_res,site_data=site_data,logger=logger)

    return wrangling_res



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Pp_project training Script")
    parser.add_argument("-d","--date", type=str, default='2023-06-06' , help="Date for getting the waste/production plan for. Default : 2023-06-06")
    parser.add_argument("-s","--site_id", type=int,default=30607, help="Site id. Default: 30607")
    args = parser.parse_args()
    main(args)