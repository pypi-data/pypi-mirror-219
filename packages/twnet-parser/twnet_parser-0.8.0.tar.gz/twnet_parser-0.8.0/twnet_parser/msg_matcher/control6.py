from typing import Optional

import twnet_parser.msg6
from twnet_parser.ctrl_message import CtrlMessage

import twnet_parser.messages6.control.keep_alive as keep_alive6
import twnet_parser.messages6.control.connect as connect6
import twnet_parser.messages6.control.connect_accept as connect_accept6
import twnet_parser.messages6.control.accept as accept6
import twnet_parser.messages6.control.close as close6

def match_control6(msg_id: int, data: bytes, client: bool) -> CtrlMessage:
    msg: Optional[CtrlMessage] = None

    if msg_id == twnet_parser.msg6.CTRL_KEEPALIVE:
        msg = keep_alive6.CtrlKeepAlive()
    elif msg_id == twnet_parser.msg6.CTRL_CONNECT:
        msg = connect6.CtrlConnect()
    elif msg_id == twnet_parser.msg6.CTRL_CONNECT_ACCEPT:
        msg = connect_accept6.CtrlConnectAccept()
    elif msg_id == twnet_parser.msg6.CTRL_ACCEPT:
        msg = accept6.CtrlAccept()
    elif msg_id == twnet_parser.msg6.CTRL_CLOSE:
        msg = close6.CtrlClose()

    if msg is None:
        raise ValueError(f"Error: unknown control message id={msg_id} data={data[0]}")

    msg.unpack(data, client)
    return msg
