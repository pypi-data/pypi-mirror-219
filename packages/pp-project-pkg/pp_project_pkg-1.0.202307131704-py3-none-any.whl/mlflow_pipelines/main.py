import mlflow
import os
import wandb
import hydra
from omegaconf import DictConfig


#@hydra.main(config_path='mlflow_pipelines',config_name='config.yaml')
@hydra.main(config_path='./',config_name='config.yaml')
def go(config: DictConfig):

    os.environ["WANDB_PROJECT"] = config["main"]["project_name"]
    os.environ["WANDB_RUN_GROUP"] = config["main"]["experiment_name"]

    root_path = hydra.utils.get_original_cwd()
    print('config :{}'.format(config))

    _ = mlflow.run(
        os.path.join(root_path, "fetch_data"),
        "main",
        parameters={
            "site_res": config["data"]["site_res"],
            "start_date" : config["data"]["start_date"],
            "logger" : config["data"]["logger"],
            "artifact_name": "upload_file.csv",
            "artifact_type": "fetch_upload_data_file",
            "artifact_description": "Fetching the data which has been uploaded in the DB"
        },
    )

    _ = mlflow.run(
        os.path.join(root_path, "upload_data"),
        "main",
        parameters={
            "input_artifact": "to_upload.csv:latest",
            "artifact_name": "uploaded_data.csv",
            "artifact_type": "processed_data",
            "artifact_description": "uploading all the data to the DB"
        },
        
    _ = mlflow.run(
        os.path.join(root_path, "train_model"),
        "main",
        parameters={
            "input_artifact": "clean_data.csv:latest",
            "artifact_name": "model.pkl",
            "artifact_type": "model",
            "artifact_description": "Trained model"
        },
    )
    )

if __name__ == "__main__":
    go()