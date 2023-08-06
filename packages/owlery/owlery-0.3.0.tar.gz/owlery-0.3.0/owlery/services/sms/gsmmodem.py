import pathlib
import typing as t

from gsmmodem.modem import CommandError, GsmModem, SentSms, TimeoutException

from . import SMS, SMSMessage


class GsmModemSms(SMS):
    """Send SMS messages with GSM modem.

    :param account_sid: Twilio Account SID.
    :param auth_token: Twilio Authentication Token.
    :param region: Region to parse phone numbers in.
    :param sender_id: Your SMS Sender ID.

    """

    name = "twilio_sms"

    def __init__(
        self,
        port: t.Union[bytes, str, pathlib.PosixPath],
        baudrate: int = 115200,
        pin_code: t.Optional[str] = None,
        **kwargs,
    ):
        self.port = port
        self.baudrate = baudrate
        self.pin_code = pin_code

        self.modem = GsmModem(self.port, self.baudrate)

        super().__init__(**kwargs)

    def close(self):
        self.modem.close()

    def open(self):
        self.modem.connect(self.pin_code)
        self.modem.waitForNetworkCoverage(10.0)

    def receive(self, limit: int = 100, **kwargs):
        messages = self.client.messages.stream(
            to=self.sender_id,
            date_sent_after=date_sent_after,
            limit=limit,
        )

        for message in messages:
            to = message.to
            from_ = message.from_

            yield SMSMessage(
                to=to,
                body=message.body,
                from_=from_,
            )

    def receive_webhook(self, request):
        validator = RequestValidator(self.auth_token)
        if not validator.validate(
            request.url,
            request.form,
            request.headers.get("X-Twilio-Signature"),
        ):
            raise ValueError("Invalid signature")

        to = request.form["To"]
        body = request.form["Body"]
        from_ = request.form["From"]

        message = SMSMessage(
            to=to,
            body=body,
            from_=from_,
            id=request.form["MessageSid"],
            reply_id=request.form.get("OriginalRepliedMessageSid"),
            raw=request.form,
            service=self,
        )

        return message

    def send(self, to, body, from_=None, **kwargs):
        if not from_:
            from_ = self.sender_id
        if from_:
            from_ = self.format_number(from_)

        to = self.format_number(to)

        message = SMSMessage(
            to=to,
            body=body,
            from_=from_,
            raw=kwargs,
            service=self,
        )

        try:
            result = self.modem.sendSms(
                to, body, sendFlash=kwargs.get("flash", False)
            )
        except Exception as e:
            message.exc = e
            message.status = "error"
        else:
            message.id = result.reference
            message.raw = result

            if result.status == result.ENROUTE:
                message.status = "sent"
            elif result.status == result.DELIVERED:
                message.status = "received"
            else:
                message.status = "error"

        return message
