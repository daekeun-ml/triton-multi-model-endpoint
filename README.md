# Deploy Models on a SageMaker GPU Multi-Model Endpoint with Triton

## Overview

SageMaker는 기본적으로 단일 호스팅 인스턴스에서 단일 ML 모델만 배포하는 단일 모델 엔드포인트(SME; Single-Model-Endpoint)를 제공하지만, 유스케이스에 따라 동일 사양의 인스턴스에서 논리적인 엔트포인트 뒤에 호스팅할 여러 모델들을 지정하는 다중 모델 엔드포인트(MME: Multi-Model Endpoint) 기능도 지원하고 있습니다. 2021년부터 NVIDIA Triton Inference 기반의 GPU도 지원하기 때문에 sLLM(Small Large Language Model)이나 Stable Diffusion 등의 여러 모델들을 단일 호스팅 인스턴스에서 서빙할 수 있습니다. MME를 사용하면 엔드포인트 뒤에서 여러 모델에 걸쳐 GPU 인스턴스를 공유하고 들어오는 트래픽에 따라 모델을 동적으로 로드 및 언로드합니다. 따라서, 큰 비용 부담 없이 최적의 가격 대비 성능을 달성할 수 있습니다.

## Getting Started
- [`0_setup.ipynb`](0_setup.ipynb) 실행
- [`1_mme-hosting-stable-diffusion.ipynb`](1_mme-hosting-stable-diffusion.ipynb) 실행
- (Optional) [`2_simple-test-tritonclient.ipynb`](2_simple-test-tritonclient.ipynb) 실행

## Requirements

이 핸즈온을 수행하기 위해 아래 사양의 인스턴스를 준비하는 것을 권장합니다.

### SageMaker Notebook instance
대안으로 SageMaker Studio Lab이나 SageMaker Studio를 사용할 수 있습니다.
- `ml.t3.medium` (최소 사양 - 로컬 모드 테스트 불가능)
- `ml.g5.2xlarge` (권장 사양)

### SageMaker Hosting instance
- `ml.g5.2xlarge` (최소 사양)
- `ml.g5.12xlarge` (권장 사양)

## References
- https://github.com/aws/amazon-sagemaker-examples/tree/main/inference/generativeai/llm-workshop

## License Summary

이 샘플 코드는 MIT-0 라이선스에 따라 제공됩니다. 라이선스 파일을 참조하세요.