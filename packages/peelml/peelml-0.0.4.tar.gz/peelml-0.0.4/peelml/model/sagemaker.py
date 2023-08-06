import boto3
import datetime
import json
import sagemaker

from sagemaker.huggingface import HuggingFaceModel
from sagemaker.huggingface import get_huggingface_llm_image_uri


class SageMaker():
    def __init__(self, role_name: str = "AmazonSageMakerFullAccess"):
        self._role_name = role_name
        self._create_role()

    def _create_role(self):
        iam_client = boto3.client('iam')

        # Check if role already exists
        try:
            iam_client.get_role(RoleName=self._role_name)
            print(f"IAM Role '{self._role_name}' already exists. Skipping creation.")
            return
        except iam_client.exceptions.NoSuchEntityException:
            pass

        assume_role_policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "sagemaker.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }

        create_role_response = iam_client.create_role(
            RoleName=self._role_name,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy_document)
        )

        attach_policy_response = iam_client.attach_role_policy(
            RoleName=self._role_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonSageMakerFullAccess'
        )

        print(f"IAM Role '{self._role_name}' created successfully!")

    def deploy(self):       
        iam = boto3.client('iam')
        role = iam.get_role(RoleName=self._role_name)['Role']['Arn']
        print(f"sagemaker role arn: {role}")

        # retrieve the llm image uri
        llm_image = get_huggingface_llm_image_uri(
            "huggingface",
            version="0.8.2"
        )

        # print ecr image uri
        print(f"llm image uri: {llm_image}")

        # sagemaker config
        instance_type = "ml.g5.2xlarge"
        number_of_gpu = 1
        health_check_timeout = 300

        # TGI config
        config = {
        'HF_MODEL_ID': "tiiuae/falcon-7b-instruct", # model_id from hf.co/models
        'SM_NUM_GPUS': json.dumps(number_of_gpu), # Number of GPU used per replica
        'MAX_INPUT_LENGTH': json.dumps(1024),  # Max length of input text
        'MAX_TOTAL_TOKENS': json.dumps(2048),  # Max length of the generation (including input text)
        'HF_MODEL_QUANTIZE': "bitsandbytes", # comment in to quantize
        }

        # create HuggingFaceModel
        llm_model = HuggingFaceModel(
            role=role,
            image_uri=llm_image,
            env=config
        )

        # deploy
        now = datetime.datetime.now()
        date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
        endpoint_name = f'falcon-7b-{date_time}'
        llm_model.deploy(
            initial_instance_count=1,
            instance_type=instance_type,
            # volume_size=400, # If using an instance with local SSD storage, volume_size must be None, e.g. p4 but not p3
            container_startup_health_check_timeout=health_check_timeout, # 5 minutes to be able to load the model
            endpoint_name=endpoint_name
        )
        print(f"sagemaker endpoint name: {endpoint_name}")
        return endpoint_name
