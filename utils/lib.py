import os
import shutil
import boto3
from pathlib import Path
from huggingface_hub import snapshot_download

def download_model(hf_model_id, local_model_path, ignore_patterns=["*.ckpt", "*.safetensors"]):
    local_model_path = Path(local_model_path)
    local_cache_path = Path("./tmp_cache")
    print(local_model_path)
    if not os.path.isdir(local_model_path):
        os.makedirs(local_model_path, exist_ok=True)
        # Download model from Hugging Face into model_dir
        snapshot_download(
            repo_id=hf_model_id,
            local_dir_use_symlinks=False,
            revision="fp16",
            cache_dir=local_cache_path,
            local_dir=local_model_path,
            ignore_patterns=ignore_patterns
        )
        shutil.rmtree(local_cache_path)
        print(f"Downloaded - [HF_MODEL_ID] {hf_model_id}")
    else:
        print(f"Hugging Face model already exists! - [HF_MODEL_ID] {hf_model_id}")
    return local_model_path


def get_triton_image_uri():
    # account mapping for SageMaker Triton Image
    account_id_map = {
        "us-east-1": "785573368785",
        "us-east-2": "007439368137",
        "us-west-1": "710691900526",
        "us-west-2": "301217895009",
        "eu-west-1": "802834080501",
        "eu-west-2": "205493899709",
        "eu-west-3": "254080097072",
        "eu-north-1": "601324751636",
        "eu-south-1": "966458181534",
        "eu-central-1": "746233611703",
        "ap-east-1": "110948597952",
        "ap-south-1": "763008648453",
        "ap-northeast-1": "941853720454",
        "ap-northeast-2": "151534178276",
        "ap-southeast-1": "324986816169",
        "ap-southeast-2": "355873309152",
        "cn-northwest-1": "474822919863",
        "cn-north-1": "472730292857",
        "sa-east-1": "756306329178",
        "ca-central-1": "464438896020",
        "me-south-1": "836785723513",
        "af-south-1": "774647643957",
    }

    region = boto3.Session().region_name
    if region not in account_id_map.keys():
        raise ("UNSUPPORTED REGION")

    base = "amazonaws.com.cn" if region.startswith("cn-") else "amazonaws.com"
    account_id = account_id_map[region]
    mme_triton_image_uri = (
        "{account_id}.dkr.ecr.{region}.{base}/sagemaker-tritonserver:23.05-py3".format(
            account_id=account_id, region=region, base=base
        )
    )
    return mme_triton_image_uri, account_id


def delete_endpoint(client, endpoint_name):
    response = client.describe_endpoint(EndpointName=endpoint_name)
    EndpointConfigName = response['EndpointConfigName']
    
    response = client.describe_endpoint_config(EndpointConfigName=EndpointConfigName)
    model_name = response['ProductionVariants'][0]['ModelName']
    
    client.delete_model(ModelName=model_name)    
    client.delete_endpoint_config(EndpointConfigName=EndpointConfigName) 
    client.delete_endpoint(EndpointName=endpoint_name)
   
    print(f'--- Deleted model: {model_name}')
    print(f'--- Deleted endpoint_config: {EndpointConfigName}')     
    print(f'--- Deleted endpoint: {endpoint_name}')