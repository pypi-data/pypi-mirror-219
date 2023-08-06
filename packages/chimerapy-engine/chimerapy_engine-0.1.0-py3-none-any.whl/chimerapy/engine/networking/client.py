# Built-in
from typing import Dict, Optional, Callable, Any
import os
import asyncio
import threading
import collections
import uuid
import pathlib
import shutil
import tempfile
import json
import enum
import logging
import traceback
import multiprocess as mp
from concurrent.futures import Future

# Third-party
import aiohttp

# Internal Imports
from chimerapy.engine import config
from .async_loop_thread import AsyncLoopThread
from chimerapy.engine.utils import create_payload, async_waiting_for
from .enums import GENERAL_MESSAGE

# Logging
from chimerapy.engine import _logger

logger = _logger.getLogger("chimerapy-engine-networking")

# References
# https://gist.github.com/dmfigol/3e7d5b84a16d076df02baa9f53271058
# https://docs.aiohttp.org/en/stable/web_advanced.html#application-runners
# https://docs.aiohttp.org/en/stable/client_reference.html?highlight=websocket%20close%20open#clientwebsocketresponse


class Client:
    def __init__(
        self,
        id: str,
        host: str,
        port: int,
        ws_handlers: Dict[enum.Enum, Callable] = {},
        parent_logger: Optional[logging.Logger] = None,
    ):

        # Store parameters
        self.id = id
        self.host = host
        self.port = port
        self.ws_handlers = {k.value: v for k, v in ws_handlers.items()}
        self._ws = None
        self._session = None

        # State variables
        self.running = threading.Event()
        self.running.clear()
        self.msg_processed_counter = 0
        self._client_shutdown_complete = threading.Event()
        self._client_shutdown_complete.clear()

        # Create thread to accept async request
        self._thread = AsyncLoopThread()
        self._thread.start()

        # Adding default client handlers
        self.ws_handlers.update(
            {
                GENERAL_MESSAGE.OK.value: self._ok,
                GENERAL_MESSAGE.SHUTDOWN.value: self._client_shutdown,
            }
        )

        # Adding file transfer capabilities
        self.tempfolder = pathlib.Path(tempfile.mkdtemp())

        if parent_logger is not None:
            self.logger = _logger.fork(parent_logger, "client")
        else:
            self.logger = _logger.getLogger("chimerapy-engine-networking")

    def __str__(self):
        return f"<Client {self.id}>"

    def setLogger(self, parent_logger: logging.Logger):
        self.logger = _logger.fork(parent_logger, "client")

    ####################################################################
    # Client WS Handlers
    ####################################################################

    async def _ok(self, msg: Dict):
        self.uuid_records.append(msg["data"]["uuid"])

    ####################################################################
    # IO Main Methods
    ####################################################################

    async def _read_ws(self):
        self.logger.debug(f"{self}: reading")
        async for aiohttp_msg in self._ws:

            # Tracking the number of messages processed
            self.msg_processed_counter += 1

            # Extract the binary data and decoded it
            msg = aiohttp_msg.json()
            self.logger.debug(f"{self}: read - {msg}")

            # Select the handler
            self.logger.debug(f"{self}: read executing {msg['signal']}")
            handler = self.ws_handlers[msg["signal"]]

            self.logger.debug(f"{self}: read handler {handler}")
            await handler(msg)
            self.logger.debug(f"{self}: finished read executing {msg['signal']}")

            # Send OK if requested
            if msg["ok"]:
                self.logger.debug(f"{self}: sending OK")
                try:
                    await self._ws.send_json(
                        create_payload(GENERAL_MESSAGE.OK, {"uuid": msg["uuid"]})
                    )
                except ConnectionResetError:
                    self.logger.warning(
                        f"{self}: ConnectionResetError, shutting down ws"
                    )
                    await self._ws.close()
                    return None

    async def _write_ws(self, msg: Dict):
        self.logger.debug(f"{self}: writing - {msg}")
        await self._send_msg(**msg)

    ####################################################################
    # Client Utilities
    ####################################################################

    async def _send_msg(
        self,
        signal: enum.Enum,
        data: Dict,
        msg_uuid: str = str(uuid.uuid4()),
        ok: bool = False,
    ):

        # Create payload
        self.logger.debug(f"{self}: send_msg -> {signal} with OK={ok}")
        payload = create_payload(signal=signal, data=data, msg_uuid=msg_uuid, ok=ok)

        # Send the message
        self.logger.debug(f"{self}: send_msg -> {signal} with OK={ok}")
        try:
            await self._ws.send_json(payload)
        except ConnectionResetError:
            self.logger.warning(f"{self}: ConnectionResetError, shutting down ws")
            await self._ws.close()
            return None

        # If ok, wait until ok
        if ok:

            success = await async_waiting_for(
                lambda: msg_uuid in self.uuid_records,
                timeout=config.get("comms.timeout.ok"),
            )
            if success:
                self.logger.debug(f"{self}: receiving OK: SUCCESS")
            else:
                self.logger.debug(f"{self}: receiving OK: FAILED")

    async def _send_file_async(
        self, url: str, sender_id: str, filepath: pathlib.Path
    ) -> bool:

        # Make a post request to send the file
        data = aiohttp.FormData()
        data.add_field(
            "meta",
            json.dumps({"sender_id": sender_id, "size": os.path.getsize(filepath)}),
            content_type="application/json",
        )
        data.add_field(
            "file",
            open(filepath, "rb"),
            filename=filepath.name,
            content_type="application/zip",
        )

        # Create a new session for the moment
        async with aiohttp.ClientSession() as session:
            self.logger.debug(f"{self}: Executing file transfer to {url}")
            response = await session.post(url, data=data)
            self.logger.debug(f"{self}: File transfer response => {response}")

        return True

    async def _send_folder_async(self, sender_id: str, dir: pathlib.Path):

        self.logger.debug(f"{self}: _send_folder_async")

        if not dir.is_dir() and not dir.exists():
            self.logger.error(f"Cannot send non-existent dir: {dir}.")
            return False

        # Having continuing attempts to make the zip folder
        miss_counter = 0
        delay = 1
        zip_timeout = config.get("comms.timeout.zip-time")

        # First, we need to archive the folder into a zip file
        while True:
            try:
                self.logger.debug(
                    f"{self}: creating zip folder of {dir}, by {sender_id} of size: \
                    {os.path.getsize(str(dir))}"
                )
                process = mp.Process(
                    target=shutil.make_archive,
                    args=(
                        str(dir),
                        "zip",
                        dir.parent,
                        dir.name,
                    ),
                )
                process.start()
                process.join()
                assert process.exitcode == 0

                self.logger.debug(
                    f"{self}: created zip folder of {dir}, by {sender_id}"
                )
                break
            except Exception:
                self.logger.warning("Temp folder couldn't be zipped.")
                self.logger.error(traceback.format_exc())
                await asyncio.sleep(delay)
                miss_counter += 1

                if zip_timeout < delay * miss_counter:
                    self.logger.error("Temp folder couldn't be zipped.")
                    return False

        zip_file = dir.parent / f"{dir.name}.zip"

        # Compose the url
        url = f"http://{self.host}:{self.port}/file/post"

        # Then send the file
        await self._send_file_async(url, sender_id, zip_file)

        self.logger.debug(f"{self}: finished sending folder")
        return True

    ####################################################################
    # Client Async Setup and Shutdown
    ####################################################################

    async def _register(self):

        # First message should be the client registering to the Server
        await self._send_msg(
            signal=GENERAL_MESSAGE.CLIENT_REGISTER,
            data={"client_id": self.id},
            ok=True,
        )

        # Mark that client has connected
        self._client_ready.set()

    async def _main(self):

        self.logger.debug(f"{self}: _main -> http://{self.host}:{self.port}/ws")

        # Create record of message uuids
        self.uuid_records = collections.deque(maxlen=100)

        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(f"http://{self.host}:{self.port}/ws") as ws:

                self.logger.debug(f"{self}: successfully connected!")

                # Store the Client session
                self._session = session
                self._ws = ws

                # Establish read and write
                read_task = asyncio.create_task(self._read_ws())

                # Register the client
                await self._register()

                # Continue executing them
                await asyncio.gather(read_task)

        # After the ws is closed, do the following
        await self._client_shutdown()

    async def _client_shutdown(self, msg: Dict = {}):

        # Mark to stop and close things
        self.running.clear()

        if self._ws:
            await asyncio.wait_for(self._ws.close(), timeout=2)
        if self._session:
            await asyncio.wait_for(self._session.close(), timeout=2)

        self._client_shutdown_complete.set()

    ####################################################################
    # Client ASync Lifecyle API
    ####################################################################

    async def async_send(self, signal: enum.Enum, data: Any, ok: bool = False) -> bool:

        # Create uuid
        msg_uuid = str(uuid.uuid4())

        # Create msg container and execute writing coroutine
        msg = {"signal": signal, "data": data, "msg_uuid": msg_uuid, "ok": ok}
        await self._write_ws(msg)

        if ok:

            success = await async_waiting_for(
                lambda: msg_uuid in self.uuid_records,
                timeout=config.get("comms.timeout.ok"),
            )
            if success:
                self.logger.debug(f"{self}: receiving OK: SUCCESS")
                return True
            else:
                self.logger.debug(f"{self}: receiving OK: FAILED")
                return False

        return True

    ####################################################################
    # Client Sync Lifecyle API
    ####################################################################

    def send(self, signal: enum.Enum, data: Any, ok: bool = False) -> Future[bool]:
        return self._thread.exec(self.async_send(signal, data, ok))

    def send_file(self, sender_id: str, filepath: pathlib.Path) -> Future[bool]:
        # Compose the url
        url = f"http://{self.host}:{self.port}/file/post"
        return self._thread.exec(self._send_file_async(url, sender_id, filepath))

    def send_folder(self, sender_id: str, dir: pathlib.Path) -> Future[bool]:

        assert (
            dir.is_dir() and dir.exists()
        ), f"Sending {dir} needs to be a folder that exists."

        return self._thread.exec(self._send_folder_async(sender_id, dir))

    def connect(self):

        self.logger.debug(f"{self}: start connect routine")

        # Mark that the client is running
        self.running.set()

        # Create async loop in thread
        self._client_ready = threading.Event()
        self._client_ready.clear()

        # Start async execution
        logger.debug(f"{self}: executing _main")
        self._thread.exec(self._main())

        # Wait until client is ready
        flag = self._client_ready.wait(timeout=config.get("comms.timeout.client-ready"))
        if flag == 0:
            self.shutdown()
            raise TimeoutError(f"{self}: failed to connect, shutting down!")
        else:
            self.logger.debug(f"{self}: connected to {self.host}:{self.port}")

    def shutdown(self):

        if self.running.is_set():

            # Execute shutdown
            self._thread.exec(self._client_shutdown())

            # Wait for it
            if not self._client_shutdown_complete.wait(
                timeout=config.get("comms.timeout.client-shutdown")
            ):
                self.logger.warning(f"{self}: failed to gracefully shutdown")

            # Stop threaded loop
            self._thread.stop()

    def __del__(self):
        self.shutdown()
