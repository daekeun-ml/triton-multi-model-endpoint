import json
import numpy as np
import torch
import triton_python_backend_utils as pb_utils

from diffusers import DiffusionPipeline
from diffusers import DDIMScheduler

from io import BytesIO
import base64


def encode_images(images):
    encoded_images = []
    for image in images:
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        img_str = base64.b64encode(buffer.getvalue())
        encoded_images.append(img_str.decode("utf8"))
    
    return encoded_images


class TritonPythonModel:
    """
     Both keys and values are strings. The dictionary keys and values are:
          * model_config: A JSON string containing the model configuration
          * model_instance_kind: A string containing model instance kind
          * model_instance_device_id: A string containing model instance device
            ID
          * model_repository: Model repository path
          * model_version: Model version
          * model_name: Model name
    """

    
    def initialize(self, args):
        
        self.model_dir = args['model_repository']
        self.model_ver = args['model_version']
    
    
        device='cuda'
        self.pipe = DiffusionPipeline.from_pretrained(f'{self.model_dir}/{self.model_ver}/checkpoint',
                                                            torch_dtype=torch.float16).to(device)
        
        self.pipe.scheduler = DDIMScheduler.from_config(self.pipe.scheduler.config)
        self.pipe.unet.enable_xformers_memory_efficient_attention()
        

    def execute(self, requests):
        
        logger = pb_utils.Logger
        responses = []
        for request in requests:
            prompt = pb_utils.get_input_tensor_by_name(request, "prompt").as_numpy().item().decode("utf-8")
            negative_prompt = pb_utils.get_input_tensor_by_name(request, "negative_prompt")
            gen_args = pb_utils.get_input_tensor_by_name(request, "gen_args")
            
            input_args = dict(prompt=prompt)
            
            if negative_prompt:
                input_args["negative_prompt"] = negative_prompt.as_numpy().item().decode("utf-8")
            
            if gen_args:
                gen_args = json.loads(gen_args.as_numpy().item().decode("utf-8"))
                input_args.update(gen_args)            
            
            images = self.pipe(**input_args).images
            encoded_images = encode_images(images)
            
            responses.append(pb_utils.InferenceResponse([pb_utils.Tensor("generated_image", np.array(encoded_images).astype(object))]))
        
        return responses
