#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 by Christian Tremblay, P.Eng <christian.tremblay@servisys.com>
# Licensed under LGPLv3, see file LICENSE in this source tree.
#
"""
IOExceptions.py - BAC0 application level exceptions 
"""
import typing as t
from typing import Optional


class WritePropertyException(Exception):
    """
    This exception is used when trying to write a property.
    """

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class WritePropertyCastError(Exception):
    """
    This exception is used when trying to write to a property and a cast error occurs.
    """

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class UnknownPropertyError(Exception):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class UnknownObjectError(Exception):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class ReadPropertyException(ValueError):
    """
    This exception is used when trying to read a property.
    """

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class ReadPropertyMultipleException(ValueError):
    """
    This exception is used when trying to read multiple properties.
    """

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class ReadRangeException(ValueError):
    """
    This exception is used when trying to read a property.
    """

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class NoResponseFromController(Exception):
    """
    This exception is used when trying to read or write and there is not answer.
    """

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class UnrecognizedService(Exception):
    """
    This exception is used when trying to read or write and there is not answer.
    """

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class WriteAccessDenied(Exception):
    """
    This exception is used when trying to write and controller refuse it.
    """

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class APDUError(Exception):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class OutOfServiceNotSet(Exception):
    """
    This exception is used when trying to simulate a point and the out of service property is false.
    """

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class OutOfServiceSet(Exception):
    """
    This exception is used when trying to set the out of service property to
    false to release the simulation...and it doesn't work.
    """

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class NetworkInterfaceException(Exception):
    """
    This exception covers different network related exc eption (like finding IP
    or subnet mask...)
    """

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class ApplicationNotStarted(Exception):
    """
    Application not started, no communication available.
    """

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class BokehServerCantStart(Exception):
    """
    Raised if Bokeh Server can't be started automatically
    """

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class SegmentationNotSupported(Exception):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class BadDeviceDefinition(Exception):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class InitializationError(Exception):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class Timeout(Exception):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class RemovedPointException(Exception):
    """
    When defining a device from DB it may not be identical to the
    actual device.
    """

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class BufferOverflow(Exception):
    """
    Buffer capacity of device exceeded.
    """

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


# For devices
class DeviceNotConnected(Exception):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class WrongParameter(Exception):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class NumerousPingFailures(Exception):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class NotReadyError(Exception):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class DataError(Exception):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)
