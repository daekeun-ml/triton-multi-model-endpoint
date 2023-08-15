docker run --gpus=1 --rm -p8000:8000 -p8001:8001 -p8002:8002 \
    -v /home/ec2-user/SageMaker/llm-workshop/lab2-stable-diffusion/option3-triton-mme/models:/models 143656149352.dkr.ecr.us-east-1.amazonaws.com/js-onboarding-mme:latest tritonserver \
    --model-repository=/models --model-control-mode=explicit --load-model=sd_base \
    --log-verbose=3 --log-info=1 --log-warning=1 --log-error=1