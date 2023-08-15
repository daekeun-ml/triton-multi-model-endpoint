
FROM 785573368785.dkr.ecr.us-east-1.amazonaws.com/sagemaker-tritonserver:23.05-py3
RUN pip install -U pip && \
    pip install --no-cache-dir sagemaker \
    boto3 \
    torch --extra-index-url https://download.pytorch.org/whl/cu118 \
    accelerate \
    transformers \
    diffusers \
    xformers

ENV PYTHONUNBUFFERED=TRUE