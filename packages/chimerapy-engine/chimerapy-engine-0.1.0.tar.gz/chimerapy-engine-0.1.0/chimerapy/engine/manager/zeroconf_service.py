import socket
from typing import Optional

from zeroconf import ServiceInfo, Zeroconf

from .manager_service import ManagerService
from chimerapy.engine import _logger

logger = _logger.getLogger("chimerapy-engine")


class ZeroconfService(ManagerService):

    enabled: bool

    def __init__(self, name: str):
        super().__init__(name=name)

        # Save information
        self.name = name
        self.zeroconf: Optional[Zeroconf] = None
        self.enabled: bool = False

    def start(self):

        # Create the zeroconf service name
        self.service_name = (
            f"chimerapy-{self.services.session_record.rand_num}._http._tcp.local."
        )

        # Create service information
        self.zeroconf_info = ServiceInfo(
            "_http._tcp.local.",
            self.service_name,
            addresses=[socket.inet_aton(self.state.ip)],
            port=self.state.port,
            properties={
                "path": str(self.services.session_record.logdir),
                "timestamp": self.services.session_record.timestamp,
            },
        )

    async def shutdown(self):
        await self.disable()

    #####################################################################################
    ## Helper Methods
    #####################################################################################

    async def enable(self) -> bool:

        if not self.enabled:

            # Start Zeroconf Service
            self.zeroconf = Zeroconf()
            await self.zeroconf.async_register_service(self.zeroconf_info, ttl=60)
            logger.info(f"Manager started Zeroconf Service named {self.service_name}")

            # Mark the service
            self.enabled = True

        return True

    async def disable(self) -> bool:

        if self.enabled:

            # Unregister the service and close the zeroconf instance
            if self.zeroconf:
                await self.zeroconf.async_unregister_service(self.zeroconf_info)
                self.zeroconf.close()

            # Mark the service
            self.enabled = False

        return True
