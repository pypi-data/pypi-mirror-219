from mb_utils.src import logging
import mb.pandas as pd
from pp_project_pkg.utils import upload_waste_data
import hydra
from omegaconf import DictConfig
import wandb

@hydra.main(config_name='./config.yml')
def data_upload_func(config: DictConfig):
    # site_number = args.site_id
    # site_start_date = args.date
    
    if config['data']['logger']:
        logger = logging.logger
    else:
        logger = None

    report_dates_res  = wandb.download(logger=logger)
    if logger:
        logger.info(report_dates_res.head())

    upload_waste_data(report_dates_res,reset=False,logger=logger)

    return None


if __name__ == '__main__':
    data_upload_func()
