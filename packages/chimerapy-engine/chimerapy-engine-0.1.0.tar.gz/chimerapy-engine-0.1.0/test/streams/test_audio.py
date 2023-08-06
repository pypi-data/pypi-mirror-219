from .data_nodes import AudioNode

# Built-in Imports
import os
import pathlib
import uuid
import time

# Third-party
import numpy as np
import pytest
import pyaudio

# Internal Imports
import chimerapy.engine as cpe
from chimerapy.engine.records.audio_record import AudioRecord

logger = cpe._logger.getLogger("chimerapy-engine")

# Constants
CWD = pathlib.Path(os.path.abspath(__file__)).parent.parent
TEST_DATA_DIR = CWD / "data"
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 2


@pytest.fixture
def audio_node():

    # Create a node
    an = AudioNode("an", CHUNK, CHANNELS, FORMAT, RATE)

    return an


def test_audio_record():

    # Check that the audio was created
    expected_audio_path = TEST_DATA_DIR / "test.wav"
    try:
        os.remove(expected_audio_path)
    except FileNotFoundError:
        ...

    # Create the record
    ar = AudioRecord(dir=TEST_DATA_DIR, name="test")

    # Write to audio file
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = (np.random.rand(CHUNK) * 2 - 1) * (i * 0.1)
        audio_chunk = {
            "uuid": uuid.uuid4(),
            "name": "test",
            "data": data,
            "dtype": "audio",
            "channels": CHANNELS,
            "format": FORMAT,
            "rate": RATE,
        }
        ar.write(audio_chunk)

    assert expected_audio_path.exists()


def test_node_save_audio_stream(audio_node):

    # Check that the audio was created
    expected_audio_path = pathlib.Path(audio_node.logdir) / "test.wav"
    try:
        os.remove(expected_audio_path)
    except FileNotFoundError:
        ...

    # Stream
    audio_node.run(blocking=False)

    # Wait to generate files
    time.sleep(3)

    audio_node.shutdown()

    # Check that the audio was created
    assert expected_audio_path.exists()
