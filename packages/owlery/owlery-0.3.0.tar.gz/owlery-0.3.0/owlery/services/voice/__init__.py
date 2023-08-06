import dataclasses
import typing as t

import phonenumbers

from .. import Message, Service, ServiceManager


@dataclasses.dataclass
class VoiceCall(Message):
    """A representation of a voice call.

    :param to: The recipient number.
    :param from_: The sender number.
    :param id: The message unique identifier.
    :param reply_id: The message identifier this message is replied to.
    :param raw: The raw data response from service.
    :param service: Service to use for sending, replies and fowarding.

    """

    to: t.Optional[str] = None
    from_: t.Optional[str] = None


@dataclasses.dataclass
class VoiceMessage(Message):
    """A representation of a voice message.

    :param to: The recipient number.
    :param from_: The sender number.
    :param id: The message unique identifier.
    :param reply_id: The message identifier this message is replied to.
    :param raw: The raw data response from service.
    :param service: Service to use for sending, replies and fowarding.

    """

    to: t.Optional[str] = None
    from_: t.Optional[str] = None


class Voice(Service):
    """Base class for an voice calling or messaging service."""

    name = "voice"

    def __init__(
        self,
        region: t.Optional[str] = None,
        sender_id: t.Optional[str] = None,
        **kwargs,
    ):
        self.region = region
        self.sender_id = sender_id

        super().__init__(**kwargs)

    def format_number(self, number):
        number = phonenumbers.parse(number, self.region)
        number = phonenumbers.format_number(
            number,
            phonenumbers.PhoneNumberFormat.E164,
        )

        return number


import serial


class GsmVoice(Voice):
    name = "gsm_voice"

    def __init__(self, port: str, baudrate: int = 112500, **kwargs):
        self.phone = serial.Serial(port, baudrate, timeout=5)

        super().__init__(**kwargs)

    def open(self):
        self.phone.write(b"AT\r\n")

        # set audio mode 8
        self.phone.write(b"AT+FCLASS=8\r\n")

        # set audio encoding 0, 8000hz
        self.phone.write(b"AT+VSM=0,8000\r\n")

        # dial 555
        self.phone.write(b"ATDT" + "555".encode() + b"\r\n")


class VoiceManager(Voice, ServiceManager):
    """Service manager for voice calling and messaging services."""

    def register(self, service_cls, **kwargs):
        kwargs.setdefault("region", self.region)
        return super().register(service_cls, **kwargs)
