import base64
from PIL import Image
from io import BytesIO
import numpy as np
import tritonclient.http as httpclient


def encode_image(image):
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    img_str = base64.b64encode(buffer.getvalue())
    return img_str


def decode_image(img):
    img = img.encode("utf8") if type(img) == "bytes" else img
    buff = BytesIO(base64.b64decode(img))
    image = Image.open(buff)
    return image


def describe_endpoint(endpoint_name):
    '''
    엔드포인트 생성 유무를 확인. 생성 중이면 기다림.
    '''
    sm_client = boto3.client("sagemaker")

    while(True):
        response = sm_client.describe_endpoint(
            EndpointName= endpoint_name
        )    
        status = response['EndpointStatus']
        if status == 'Creating':
            print("Endpoint is ", status)
            time.sleep(30)
        else:
            print("Endpoint is ", status)
            break


def get_sample_binary(payload):

    inputs = []
    outputs = []
    for idx, dic in enumerate(payload["inputs"]):
        input_name = dic["name"]
        input_value = dic["data"][0]

        input_value = np.array([input_value.encode('utf-8')], dtype=np.object_)

        input_value = np.expand_dims(input_value, axis=0)
        inputs.append(httpclient.InferInput(input_name, [1, 1], "BYTES"))
        inputs[idx].set_data_from_numpy(input_value)

    outputs.append(httpclient.InferRequestedOutput("generated_image", binary_data=True))

    request_body, header_length = httpclient.InferenceServerClient.generate_request_body(
        inputs, outputs=outputs
    )
    return request_body, header_length