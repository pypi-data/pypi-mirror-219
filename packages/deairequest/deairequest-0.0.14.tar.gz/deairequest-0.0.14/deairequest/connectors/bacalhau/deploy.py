from bacalhau_sdk.api import submit
from bacalhau_sdk.config import get_client_id
from bacalhau_apiclient.models.storage_spec import StorageSpec
from bacalhau_apiclient.models.spec import Spec
from bacalhau_apiclient.models.job_spec_language import JobSpecLanguage
from bacalhau_apiclient.models.job_spec_docker import JobSpecDocker
from bacalhau_apiclient.models.resource_usage_config import ResourceUsageConfig
from bacalhau_apiclient.models.publisher_spec import PublisherSpec
from bacalhau_apiclient.models.deal import Deal
from pathlib import Path
import os
import base64
import tarfile
import ipfshttpclient
from os.path import exists




def deploy(base_path: Path, root_file: str, config: dict):
    # The 'initiator' function expects a JSON blob encoding notebook steps:
    #with (base_path / root_file).open("r") as reader:
    #    body = json.load(reader)
    #print(f"code:'{os.path.join(base_path,'code.py')}")

    # Initiate execution against the backend functionapp:
    job = create_job(config, base_path, root_file)
    #print(f"job:'{job}")
    try:
        res = submit(job)
    except Exception as err:
        raise RuntimeError(f"The 'bacalhau' backend gave an error: {err}")

    # Result is a JSON blob describing the 'job' execution context:
    #data = json.loads(res.to_str())
    #print(f"Successfully started an execution of notebook '{config.get('notebook').get('name')}', visit the following link for results:\n\t{res.job.metadata.id}")

    return res.job.metadata.id
    
def create_job(config: dict, base_path: Path, root_file: str) -> str:
    # use the requirements md5 hash to see if an image is already available
    #requirements=os.path.join(base_path,root_file,"requirements.txt")
    #openedFile=open(requirements,"r",encoding='utf-8')
    #readFile=openedFile.read()
    #readFile="python:3.9-slim:"+readFile
    #md5Hash = hashlib.md5(readFile.encode('utf-8'))
    #md5Hashed = md5Hash.hexdigest()
    #client = docker.from_env()
    #try:
    #    print(f"pulling:{md5Hashed}")
    #    client.images.pull(md5Hashed)
    #    print(f"pull worked")
    #except docker.errors.ImageNotFound:
    #    dockerpath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"Dockerfile")
    #    print(f"docker:{dockerpath}")                          
    #    client.images.build(
    #        path = os.path.join(base_path,root_file), 
    #        dockerfile=dockerpath,
    #        tag=md5Hashed+":lastest",
    #    )

    #    print(f'user:{config.get("runtime_options").get("docker_user")}')  
    #    print(f'pwd:{config.get("runtime_options").get("docker_password")}')
        #client.push.
    datasets=_generateStorageSpec(config)

    requirements=os.path.join(base_path,"inputs/requirements.txt")
    if exists(requirements):
        cids = _download_wheels(base_path,requirements)
        cid = ""
        # get the directory CID
        for x in cids:
            if x['Name'] == "wheels":
                cid = x['Hash']
        if datasets != {}:
            datasets.append(StorageSpec(
                        storage_source="IPFS",
                        path="/wheels",
                        cid=cid, 
                    ))
            datasets.append(
                    StorageSpec(
                        storage_source="Inline",
                        path="/inputs",
                        url=_encode_tar_gzip(base_path,"inputs"),
    
                    ))
        command=["/bin/sh","-c","pip3 install --no-index --find-links /wheels -r /inputs/inputs/requirements.txt;mv /inputs/inputs/code.py /inputs/code.py;python3 /inputs/code.py"]
    else:
        if datasets != {}:
            datasets.append(
                    StorageSpec(
                        storage_source="Inline",
                        path="/inputs",
                        url=_encode_tar_gzip(base_path,"inputs"),
    
                    ),)
        command=["/bin/sh","-c","mv /inputs/inputs/code.py /inputs/code.py;python3 /inputs/code.py"]


    data = dict(
        APIVersion='V1beta1',
        ClientID=get_client_id(),
        Spec=Spec(
            engine="Docker",
            verifier="Noop",
            publisher_spec=PublisherSpec(type="ipfs"),
            docker=JobSpecDocker(
                image=config.get('environments').get('default').get('image_tag'),
                entrypoint=command,
                working_directory="/inputs",
            ),
            resources=ResourceUsageConfig(
                gpu="1",
            ),
            inputs=datasets
            ,
            outputs=[
                StorageSpec(
                    storage_source="IPFS",
                    name="outputs",
                    path="/outputs",
                )
            ],
            language=JobSpecLanguage(job_context=None),
            wasm=None,
            timeout=1800,
            deal=Deal(concurrency=1, confidence=0, min_bids=0),
            do_not_track=False,
        ),
    )

    #print(data)
       
    return data

def _download_wheels(dir: Path, reqs: Path) -> str:
    wheelsdir=os.path.join(dir,"wheels")
    try:
        api = ipfshttpclient.connect()
        cid = api.add(wheelsdir)
    finally:
        if api != None:
            api.close()
    return cid
    

def _encode_tar_gzip(dir: Path, name: str) -> str:
    """Encodes the given data as an urlsafe base64 string."""
    inputsdir=os.path.join(dir,name)
    #print(f"tar:{dir} {name}")
    tarname=os.path.join(dir,name+".tar.gz")
    try:
        with tarfile.open(tarname, "w:gz") as tar:
            tar.add(inputsdir, arcname=os.path.basename(inputsdir))
            #print(f"dir:{inputsdir}")
    finally:
        tar.close
    try:
        code = open(tarname, "rb")
        code_read = code.read()
        encoded = "data:application/gzip;base64,"+base64.b64encode(code_read).decode("utf-8")
    finally:
        code.close()
    return encoded


def _generateStorageSpec(config:dict) -> list:
    ss=[]
    dss=config.get("datasources")
    for ds in dss:
        type = list(ds.keys())[0]
        value = ds.get(type).get('value')
        encrypted = ds.get(type).get('encrypted')
        if type == 'file' or type == 'directory':

            try:
                api = ipfshttpclient.connect()
                cid = api.add(os.path.join(value))
                if isinstance(cid,list):
                    cid=cid[len(cid)-1].as_json().get("Hash")
                else:
                    cid=cid.as_json().get("Hash")
            finally:
                if api != None:
                    api.close()
            ss.append(StorageSpec(
                    storage_source="IPFS",
                    path="/inputs/"+os.path.basename(value),
                    cid=cid, 
                ),)
        elif type == 'ipfs':

            if value.startswith('ipfs://'):
                value=value[7:]

            dir=value
            # check if the CID is of the format CID:/path
            pos = value.find(':')
            if pos > -1:
                nt=pos+1
                dir=value[nt:]
                value=value[:pos]

            ss.append(StorageSpec(
                    storage_source="IPFS",
                    path="/inputs/"+dir,
                    cid=value, 
                ),)

        else: #url
            ss.append(StorageSpec(
                        name=value,
                        storage_source="URLDownload",
                        path="/inputs",
                        url=value,
                    ),)
            
    return ss