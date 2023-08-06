from mb_utils.src import logging
import mb.pandas as pd
from pp_project_pkg.utils import site_date_res,check_report_close_date,download_upload_dates_report
import argparse
from omegaconf import DictConfig
import wandb

@hydra.main(config_name='./config.yml')
def fetch_data_run(config: DictConfig):
    # site_number = args.site_id
    # site_start_date = args.date
    
    if config['data']['logger']:
        logger = logging.logger
    else:
        logger = None


    site_res =  site_date_res(config['data']['site_res'],logger=logger)
    
    report_res = check_report_close_date(site_res,start_date=config['data']['site_res'],logger=logger)

    if logger:
        logger.info(report_res.head())

    report_dates_res  = download_upload_dates_report(report_res,logger=logger)
    report_dates_res.to_csv('report_dates_res.csv')
    
    if logger:
        logger.info('report_dates_res saved')
        logger.info(report_dates_res.head())
        logger.info("Creating run")
    
    with wandb.init(job_type="fetch_data") as run:
            logger.info("Creating artifact")
            artifact = wandb.Artifact(
                name=args.artifact_name,
                type=args.artifact_type,
                description=args.artifact_description,
            )
            artifact.add_file('report_dates_res.csv')

            logger.info("Logging artifact")
            run.log_artifact(artifact)

    #return report_dates_res


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Fetch data from the DB")
    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Fully-qualified name for the input artifact",
        required=True,
    )

    parser.add_argument(
        "--artifact_name", type=str, help="Name for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_type", type=str, help="Type for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_description",
        type=str,
        help="Description for the artifact",
        required=True,
    )

    args = parser.parse_args()

    fetch_data_run(args)

