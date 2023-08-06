import logging
from typing import Any

from pydantic import BaseModel

from ipfabric import models

logger = logging.getLogger("ipfabric")


class SerialPorts(BaseModel):
    client: Any

    @property
    def serial_ports(self):
        return models.Table(client=self.client, endpoint="/tables/serial-ports")
