#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 by Christian Tremblay, P.Eng <christian.tremblay@servisys.com>
# Licensed under LGPLv3, see file LICENSE in this source tree.
#
"""
Simulate.py - simulate the value of controller I/O values
"""
import typing as t

from bacpypes3.app import Application

from ..app.asyncApp import BAC0Application
from .IOExceptions import (
    ApplicationNotStarted,
    NoResponseFromController,
    OutOfServiceNotSet,
    OutOfServiceSet,
)

# Type aliases for better type safety
# BACnet simulation command string format: "<address> <object_type> <instance> <property> <value>"
# Examples: "192.168.1.100 analogOutput 1 presentValue 75.5"
BACnetSimulateCommandString = str  # Structured string format for BACnet simulation operations

# --- standard Python modules ---
# --- 3rd party modules ---
# --- this application's modules ---
from .Write import WriteProperty

# ------------------------------------------------------------------------------


class Simulation:
    """
    Global informations regarding simulation
    """

    async def sim(self, args: BACnetSimulateCommandString) -> None:
        """
        Simulate I/O points by setting the Out_Of_Service property, then doing a
        WriteProperty to the point's Present_Value.

        :param args: String with <addr> <type> <inst> <prop> <value> [ <indx> ] [ <priority> ]

        """
        if not self._started:
            raise ApplicationNotStarted("BACnet stack not running - use startApp()")
        _this_application: BAC0Application = self.this_application
        _app: Application = _this_application.app
        (
            address,
            obj_type,
            obj_inst,
            prop_id,
            value,
            priority,
            indx,
        ) = WriteProperty._parse_wp_args(args)

        if await self.is_out_of_service(args):
            await self._write(args)
        else:
            try:
                await self.out_of_service(args)
            except NoResponseFromController as e:
                self.log(
                    f"Failed to write to OutOfService property ({e})", level="warning"
                )

            try:
                if await self.is_out_of_service(args):
                    await self._write(
                        f"{address} {obj_type} {obj_inst} {prop_id} {value}"
                    )
                else:
                    raise OutOfServiceNotSet()
            except NoResponseFromController as e:
                self.log(
                    f"Failed to write to OutOfService property ({e})", level="warning"
                )

    async def is_out_of_service(self, args: BACnetSimulateCommandString) -> bool:
        if not self._started:
            raise ApplicationNotStarted("BACnet stack not running - use startApp()")
        _this_application: BAC0Application = self.this_application
        _app: Application = _this_application.app
        (
            address,
            obj_type,
            obj_inst,
            prop_id,
            value,
            priority,
            indx,
        ) = WriteProperty._parse_wp_args(args)

        oos = await self.read(f"{address} {obj_type} {obj_inst} outOfService")

        return True if oos else False

    async def out_of_service(self, args: BACnetSimulateCommandString) -> None:
        """
        Set the Out_Of_Service property so the Present_Value of an I/O may be written.

        :param args: String with <addr> <type> <inst> <prop> <value> [ <indx> ] [ <priority> ]

        """
        if not self._started:
            raise ApplicationNotStarted("BACnet stack not running - use startApp()")
        (
            address,
            obj_type,
            obj_inst,
            prop_id,
            value,
            priority,
            indx,
        ) = WriteProperty._parse_wp_args(args)
        try:
            await self._write(f"{address} {obj_type} {obj_inst} outOfService True")
        except NoResponseFromController as e:
            self.log(f"Failed to write to OutOfService property ({e})", level="warning")

    async def release(self, args: BACnetSimulateCommandString) -> None:
        """
        Set the Out_Of_Service property to False - to release the I/O point back to
        the controller's control.

        :param args: String with <addr> <type> <inst>

        """
        if not self._started:
            raise ApplicationNotStarted("BACnet stack not running - use startApp()")

        (
            address,
            obj_type,
            obj_inst,
            prop_id,
            value,
            priority,
            indx,
        ) = WriteProperty._parse_wp_args(args)
        try:
            await self._write(f"{address} {obj_type} {obj_inst} outOfService False")
        except NoResponseFromController as e:
            self.log(f"Failed to write to OutOfService property ({e})", level="warning")

        try:
            if await self.is_out_of_service(args) is True:
                raise OutOfServiceSet()
            else:
                pass  # Everything is ok"
        except NoResponseFromController as e:
            self.log(f"Failed to read OutOfService property ({e})", level="warning")
