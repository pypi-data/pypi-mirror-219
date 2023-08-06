import os
import tempfile
from promptflow import tool
from promptflow.connections import CustomConnection
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioDataStream
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from azure.storage.blob import BlobServiceClient
import uuid

@tool
def azure_speech_tts(connection: CustomConnection, input_text: str, output_blob_account_name: str, output_blob_container_name: str, voice_name: str = 'en-us-jennyneural') -> str:
    
    temp_dir = tempfile.gettempdir()
    file_name = str(uuid.uuid4()) + ".wav"
    file_path = os.path.join(temp_dir, file_name)
    audio_config = AudioOutputConfig(filename=file_path)
    speech_config = SpeechConfig(subscription=connection.api_key, region=connection.api_region)
    speech_config.speech_synthesis_voice_name=voice_name
    speech_syntheizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_syntheizer.speak_text_async(input_text).get()

    account_url = f"https://{output_blob_account_name}.blob.core.windows.net"
    shared_access_key = connection.azure_storage_access_key
    credential = shared_access_key
    blob_service_client = BlobServiceClient(account_url, credential=credential)
    blob_client = blob_service_client.get_blob_client(container=output_blob_container_name, blob=file_name)
    with open(file=file_path, mode="rb") as data:
        blob_client.upload_blob(data=data, overwrite=True)

    return str(blob_client.url)
