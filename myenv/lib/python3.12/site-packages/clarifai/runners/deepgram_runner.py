import os
import time
import httpx
from dotenv import load_dotenv
import threading
import queue
import hashlib

from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
)

load_dotenv()

os.environ["DG_API_KEY"] = "1d5666523f0f2fbaf3e2db6ae7717f6f87280b5e"
API_KEY = os.getenv("DG_API_KEY")

from clarifai_grpc.grpc.api import resources_pb2, service_pb2
from collections.abc import Iterator
from google.protobuf import json_format

from clarifai.client.runner import Runner


class MyRunner(Runner):
  """A custom runner that adds "Hello World" to the end of the text and replaces the domain of the
  image URL as an example.
  """

  def setup_connection(self):
    print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZz")
    # STEP 2: Create a websocket connection to Deepgram
    self.dg_connection = self.deepgram.listen.live.v("1")

    output_q = self.output_q

    # STEP 3: Define the event handlers for the connection
    def on_message(self, result, **kwargs):
      if result.is_final:
        sentence = result.channel.alternatives[0].transcript
        if len(sentence) == 0:
          return
        print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
        print(f"speaker: {sentence}")
        # put it on a queue as we get responses from deepgram.
        output_q.put(sentence)

    def on_metadata(self, metadata, **kwargs):
      print(f"\n\n{metadata}\n\n")

    def on_error(self, error, **kwargs):
      print(f"\n\n{error}\n\n")

    # STEP 4: Register the event handlers
    self.dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
    self.dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
    self.dg_connection.on(LiveTranscriptionEvents.Error, on_error)

    # STEP 5: Configure Deepgram options for live transcription
    self.options = LiveOptions(
        model="nova-2",
        language="en-US",
        smart_format=True,
    )

    # STEP 6: Start the connection
    self.dg_connection.start(self.options)

    print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
    print(self.dg_connection._socket)

  def __init__(self, *args, **kwargs):
    print("MyRunner init")
    # STEP 1: Create a Deepgram client using the API key
    self.deepgram = DeepgramClient(API_KEY)
    self.output_q = queue.Queue()

    self.setup_connection()

    super().__init__(*args, **kwargs)

  def stream(self, request: service_pb2.PostModelOutputsRequest
            ) -> Iterator[service_pb2.MultiOutputResponse]:
    """Example yielding a whole batch of streamed stuff back.
    """

    assert len(request.inputs) == 1, "This runner only supports one input at a time."

    # Get the next chunk of data from the incoming stream.

    print("Got some audio data")

    data = request.inputs[0].data.audio.base64
    print(hashlib.md5(data).hexdigest())

    # FIXME(zeiler): this doesnt' work but isn't iportant to our system.
    if not self.dg_connection._socket:
      #self.dg_connection.finish()
      #self.dg_connection.start(self.options)
      self.setup_connection()
    self.dg_connection.send(data)
    print("Sent it to deepgram")

    while True:
      try:
        item = self.output_q.get(timeout=0.1)
        output = resources_pb2.Output()
        output.data.text.raw = item
        output.status.code = 10000
        print("YYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
        print("Yielding: ", output.data.text.raw)
        yield service_pb2.MultiOutputResponse(outputs=[
            output,
        ])
      except queue.Empty:
        print("Queue is empty, sleeping then breaking")
        break

  # # STEP 13: Close the connection to Deepgram
  # dg_connection.finish()


if __name__ == '__main__':
  # Make sure you set these env vars before running the example.
  # CLARIFAI_PAT
  # CLARIFAI_USER_ID

  # You need to first create a runner in the Clarifai API and then use the ID here.
  MyRunner(runner_id="matt-test-runner", base_url="http://q6:32013", num_parallel_polls=1).start()
