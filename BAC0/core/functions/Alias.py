import asyncio
import typing as t
from typing import List, Optional, Tuple, Union

from bacpypes3.app import Application
from bacpypes3.netservice import RouterEntryStatus
from bacpypes3.npdu import RejectMessageToNetwork
from bacpypes3.pdu import Address, GlobalBroadcast

from BAC0.core.app.asyncApp import BAC0Application

from ...core.utils.notes import note_and_log

if t.TYPE_CHECKING:
    from bacpypes3.apdu import IAmRequest, IHaveRequest

ROUTER_TUPLE_TYPE = Union[
    Tuple[Union[Address, str], Union[int, List[int]]],
    Tuple[Union[Address, str], Union[int, List[int]], Optional[int]],
]


@note_and_log
class Alias:
    """
    Bacpypes3 now offer a wide range a functions out of the box
    This mixin bring them to the BAC0 app so it's easy to use
    """

    async def who_is(self, address: t.Optional[str] = None, low_limit: int = 0, high_limit: int = 4194303, timeout: int = 3) -> t.List["IAmRequest"]:
        """
        Discover BACnet devices on the network using Who-Is requests.
        
        This is the primary device discovery function in BAC0. It sends Who-Is requests
        to discover all BACnet devices or specific devices by ID range. Discovered devices
        respond with I-Am messages containing their device information.
        
        Args:
            address: Target address for directed discovery (e.g., "192.168.1.100" or "2:5")
                    If None, broadcasts to discover all devices on local network
            low_limit: Minimum device instance ID to discover (default: 0)
            high_limit: Maximum device instance ID to discover (default: 4194303)
            timeout: Time in seconds to wait for responses (default: 3)
            
        Returns:
            List of I-Am response objects containing device information:
            - Device instance ID and vendor information
            - Device address and network details  
            - Object identifier and device capabilities
            
        Examples:
            Basic device discovery (broadcast to all devices):
            >>> import BAC0
            >>> bacnet = BAC0.start(ip="192.168.1.100/24")
            >>> devices = await bacnet.who_is()
            >>> print(f"Found {len(devices)} devices")
            >>> for device in devices:
            ...     print(f"Device {device.iAmDeviceIdentifier[1]} at {device.pduSource}")
            
            Discover devices in specific ID range:
            >>> devices = await bacnet.who_is(low_limit=1000, high_limit=2000)
            >>> controllers = [d for d in devices if 1000 <= d.iAmDeviceIdentifier[1] <= 2000]
            
            Directed discovery to specific address:
            >>> device = await bacnet.who_is(address="192.168.1.50")
            >>> if device:
            ...     print(f"Found device: {device[0].iAmDeviceIdentifier}")
            
            Discovery on remote network:
            >>> remote_devices = await bacnet.who_is(address="2:5")  # Network 2, MAC 5
            >>> for dev in remote_devices:
            ...     print(f"Remote device: {dev.iAmDeviceIdentifier[1]}")
            
            Discovery with custom timeout:
            >>> devices = await bacnet.who_is(timeout=10)  # Wait longer for slow networks
            
            Filter by vendor after discovery:
            >>> devices = await bacnet.who_is()
            >>> johnson_devices = []
            >>> for device in devices:
            ...     if device.vendorIdentifier == 5:  # Johnson Controls vendor ID
            ...         johnson_devices.append(device)
            
            Connect to discovered devices:
            >>> devices = await bacnet.who_is()
            >>> for iam in devices:
            ...     device_id = iam.iAmDeviceIdentifier[1]
            ...     address = str(iam.pduSource)
            ...     controller = await BAC0.device(address, device_id, bacnet)
            ...     print(f"Connected to {controller.properties.name}")
            
            Discovery in automation scripts:
            >>> async def discover_and_connect():
            ...     async with BAC0.start(ip="192.168.1.100/24") as bacnet:
            ...         # Discover all devices
            ...         devices = await bacnet.who_is()
            ...         
            ...         # Connect to each device
            ...         controllers = []
            ...         for iam in devices:
            ...             try:
            ...                 device_id = iam.iAmDeviceIdentifier[1]
            ...                 address = str(iam.pduSource)
            ...                 controller = await BAC0.device(address, device_id, bacnet)
            ...                 controllers.append(controller)
            ...                 print(f"✓ Connected: {controller.properties.name}")
            ...             except Exception as e:
            ...                 print(f"✗ Failed to connect to device {device_id}: {e}")
            ...         
            ...         return controllers
        """
        _iams = await self.this_application.app.who_is(
            address=Address(address) if address else None,
            low_limit=low_limit,
            high_limit=high_limit,
            timeout=timeout,
        )
        return _iams

    def iam(self, address: t.Optional[str] = None) -> None:
        """
        Build an IAm response.  IAm are sent in response to a WhoIs request that;
        matches our device ID, whose device range includes us, or is a broadcast.
        Content is defined by the script (deviceId, vendor, etc...)

        Example::

            iam()
        """
        _this_application: BAC0Application = self.this_application
        _app: Application = _this_application.app
        self.log("do_iam", level="debug")

        _app.i_am(address=address)

    async def whois_router_to_network(
        self, network: t.Optional[int] = None, *, destination: t.Optional[str] = None, timeout: int = 3, global_broadcast: bool = False
    ) -> t.List[int]:
        """
        Send a Who-Is-Router-To-Network request. This request is used to discover routers
        on the network that can route messages to a specific network.

        The function sends a broadcast message to the local network to find routers that
        can route messages to the specified network. The response will contain information
        about the routers that can handle the routing.

        Example::

            whois_router_to_network()
        """
        # build a request
        _this_application: BAC0Application = self.this_application
        _app: Application = _this_application.app
        if destination and not isinstance(destination, Address):
            destination = Address(destination)
        elif global_broadcast:
            destination = GlobalBroadcast()

        try:
            network_numbers = await asyncio.wait_for(
                _app.nse.who_is_router_to_network(
                    destination=destination, network=network
                ),
                timeout,
            )
            return network_numbers
        except asyncio.TimeoutError:
            # Handle the timeout error
            self.log(
                "Request timed out for whois_router_to_network, no response",
                level="warning",
            )
            return []

    async def init_routing_table(self, address: t.Optional[str] = None) -> None:
        """
        irt <addr>

        Send an empty Initialize-Routing-Table message to an address, a router
        will return an acknowledgement with its routing table configuration.
        """
        # build a request
        self.log(f"Addr : {address}", level="info")
        _this_application: BAC0Application = self.this_application
        _app: Application = _this_application.app
        if address is not None and not isinstance(address, Address):
            address = Address(address)
        await _app.nse.initialize_routing_table(destination=address)

    async def use_router(
        self,
        router_infos: Union[
            Tuple[Union[Address, str], Union[int, List[int]]],
            Tuple[Union[Address, str], Union[int, List[int]], Optional[int]],
        ] = (None, None, None),
    ):
        address, dnets = router_infos[:2]
        try:
            snet = router_infos[2]
        except IndexError:
            snet = None
        _this_application: BAC0Application = self.this_application
        _app: Application = _this_application.app
        if not isinstance(address, Address):
            address = Address(address)
        if not isinstance(dnets, list):
            dnets = [dnets]
        response = await self.who_is(address=address)
        if response:
            self._log.info(f"Router found at {address}")
            self._log.info(
                f"Adding router reference -> Snet : {snet} Addr : {address} dnets : {dnets}"
            )
            await _app.nsap.update_router_references(
                snet=snet, address=address, dnets=dnets
            )
            self._ric = self.this_application.app.nsap.router_info_cache
            self._log.info(
                f"Updating router info cache -> Snet : {snet} Addr : {address} dnets : {dnets}"
            )
            for each in dnets:
                await self._ric.set_path_info(
                    snet, each, address, RouterEntryStatus.available
                )
                _this_application._learnedNetworks.add(each)
        else:
            self._log.warning(f"Router not found at {address}")

    async def what_is_network_number(self, destination: t.Optional[str] = None, timeout: int = 3) -> t.Optional[int]:
        """
        winn [ <addr> ]

        Send a What-Is-Network-Number message.  If the address is unspecified
        the message is locally broadcast.
        """
        # build a request
        # self.log("Addr : {}".format(address), level='info')
        _this_application: BAC0Application = self.this_application
        _app: Application = _this_application.app
        try:
            network_number = await asyncio.wait_for(
                _app.nse.what_is_network_number(), timeout
            )
            return network_number

        except asyncio.TimeoutError:
            # Handle the timeout error
            self.log(
                "Request timed out for what_is_network_number, no response",
                level="warning",
            )
            return None

    async def whohas(
        self,
        object_id: t.Optional[str] = None,
        object_name: t.Optional[str] = None,
        low_limit: int = 0,
        high_limit: int = 4194303,
        destination: t.Optional[str] = None,
        timeout: int = 5,
    ) -> t.List["IHaveRequest"]:
        """
        Build a WhoHas request.

        :param object_id: (optional) The address to send the request to, if unused object_name must be present.
        :param object_name: (optional) The address to send the request to, if unused object_id must be present.
        :param destination: (optional) The destination address, if empty local broadcast will be used.
        :param timeout: (optional) The timeout for the WhoHas.

        :returns: IAm response.

        Example::

            import BAC0
            bacnet = BAC0.lite()

            bacnet.whohas(object_name='SomeDevice')
        """
        _ihave = await self.this_application.app.who_has(
            object_identifier=object_id,
            object_name=object_name,
            low_limit=low_limit,
            high_limit=high_limit,
            address=Address(destination) if destination else None,
            timeout=timeout,
        )
        return _ihave
