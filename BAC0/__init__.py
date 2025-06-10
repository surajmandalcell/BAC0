#!/usr/bin/python
# -*- coding: utf-8 -*-
import importlib.util
import os

if importlib.util.find_spec("bacpypes3") is not None:
    import bacpypes3  # noqa: F401

else:
    # Using print here or setup.py will fail
    print("=" * 80)
    print(
        'BACpypes3 module missing, please install latest version using \n    $ "pip install BACpypes3"'
    )
    print("\nDiscard this message if you are actually installing BAC0.")
    print("=" * 80)

if importlib.util.find_spec("dotenv") is not None:
    from dotenv import load_dotenv

    load_dotenv(os.path.join(os.getcwd(), ".env"))
else:
    print("You need to pip install python-dotenv to use your .env file")

try:
    import typing as t
    from . import core, tasks  # noqa: F401
    from .core.devices.Device import DeviceLoad as load  # noqa: F401
    from .core.devices.Device import device  # noqa: F401
    from .core.devices.Trends import TrendLog as TrendLog  # noqa: F401
    from .core.utils.notes import update_log_level as log_level  # noqa: F401
    from .infos import __version__ as version  # noqa: F401
    from .scripts.Base import Base  # noqa: F401
    from .scripts.Lite import Lite
    from .tasks.Devices import AddDevice as add_device  # noqa: F401
    from .tasks.Match import Match as match  # noqa: F401
    from .tasks.Poll import SimplePoll as poll  # noqa: F401

    # Type-safe wrapper functions that preserve autocomplete
    def start(
        ip: t.Optional[str] = None,
        port: t.Optional[int] = None,
        mask: t.Optional[int] = None,
        bbmdAddress: t.Optional[str] = None,
        bbmdTTL: int = 0,
        bdtable: t.Optional[t.List[str]] = None,
        ping: bool = True,
        ping_delay: int = 300,
        db_params: t.Optional[t.Dict[str, t.Union[str, int, bool]]] = None,
        **params,
    ) -> Lite:
        """
        Create a BACnet application for building automation system communication.
        
        BAC0.start() is the main entry point for creating a BACnet/IP application that can
        discover, read from, and write to BACnet devices on the network.
        
        Args:
            ip: IP address and subnet mask for the BACnet interface
            port: UDP port for BACnet communication (default: 47808)  
            mask: Subnet mask bits (alternative to ip/mask format)
            bbmdAddress: BBMD (BACnet Broadcast Management Device) IP address
            bbmdTTL: Time-to-live for BBMD registration (seconds)
            bdtable: List of BBMD addresses for broadcast distribution
            ping: Enable automatic device ping to detect disconnections
            ping_delay: Interval between ping attempts (seconds)
            db_params: Database connection parameters for data logging
            
        Returns:
            BAC0 application instance ready for BACnet communication
            
        Examples:
            Basic usage:
            >>> import BAC0
            >>> bacnet = BAC0.start()  # Uses default 127.0.0.1/24
            >>> devices = bacnet.whois()  # Discover devices
            
            Specify network interface:
            >>> bacnet = BAC0.start(ip="192.168.1.100/24")
            
            With database logging:
            >>> db_config = {
            ...     "host": "localhost",
            ...     "database": "bacnet_data",
            ...     "user": "bacnet_user",
            ...     "password": "secret"
            ... }
            >>> bacnet = BAC0.start(ip="192.168.1.100/24", db_params=db_config)
            
            As async context manager:
            >>> async with BAC0.start(ip="192.168.1.100/24") as bacnet:
            ...     devices = bacnet.whois()
            ...     device = await BAC0.device("192.168.1.50", 1001, bacnet)
            
            With BBMD for remote networks:
            >>> bacnet = BAC0.start(
            ...     ip="192.168.1.100/24",
            ...     bbmdAddress="192.168.10.5",
            ...     bbmdTTL=300
            ... )
        """
        return Lite(
            ip=ip,
            port=port,
            mask=mask,
            bbmdAddress=bbmdAddress,
            bbmdTTL=bbmdTTL,
            bdtable=bdtable,
            ping=ping,
            ping_delay=ping_delay,
            db_params=db_params,
            **params
        )

    # Kept for compatibility - these also get proper type hints
    def connect(
        ip: t.Optional[str] = None,
        port: t.Optional[int] = None,
        mask: t.Optional[int] = None,
        bbmdAddress: t.Optional[str] = None,
        bbmdTTL: int = 0,
        bdtable: t.Optional[t.List[str]] = None,
        ping: bool = True,
        ping_delay: int = 300,
        db_params: t.Optional[t.Dict[str, t.Union[str, int, bool]]] = None,
        **params,
    ) -> Lite:
        """Legacy alias for start(). Use BAC0.start() instead."""
        return start(ip, port, mask, bbmdAddress, bbmdTTL, bdtable, ping, ping_delay, db_params, **params)

    def lite(
        ip: t.Optional[str] = None,
        port: t.Optional[int] = None,
        mask: t.Optional[int] = None,
        bbmdAddress: t.Optional[str] = None,
        bbmdTTL: int = 0,
        bdtable: t.Optional[t.List[str]] = None,
        ping: bool = True,
        ping_delay: int = 300,
        db_params: t.Optional[t.Dict[str, t.Union[str, int, bool]]] = None,
        **params,
    ) -> Lite:
        """Legacy alias for start(). Use BAC0.start() instead."""
        return start(ip, port, mask, bbmdAddress, bbmdTTL, bdtable, ping, ping_delay, db_params, **params)

except ImportError as error:
    print("=" * 80)
    print(
        'Import Error, refer to documentation or reinstall using \n    $ "pip install BAC0"\n {}'.format(
            error
        )
    )
    print("\nDiscard this message if you are actually installing BAC0.")
    print("=" * 80)
    # Probably installing the app...
