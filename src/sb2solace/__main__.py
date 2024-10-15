import os
import time
import pyrsolace
import dotenv
import orjson
from threading import Event

TEMP_DATA = {
    "FORMAT": "FSOUM01",
    "TRADE_TYPE": "50",
    "ORD_DATE": "20241015",
    "BRANCH_ID": "1300",
    "ORD_NO": "00000045",
    "MATCH_DATE": "20241015",
    "FSOUM01_7": "UC21533606",
    "MATCH_TIME": "101145",
    "ACCOUNT": "09800762",
    "EXCHANGE": "US",
    "STOCK_ID": "NVDA",
    "MATCH_QTY": "00000000001",
    "MATCH_PRICE_INT": "0000138",
    "MATCH_PRICE_DEC": "070000",
    "BROKER_ID": "80036",
    "AGENT_ID": "009611",
    "INTRODUCER": "",
    "BS": "B",
    "WEB_ID": "146",
    "ORD_SEQ": "07821652",
    "TRF_FLD": "",
    "FSOUM01_21": "10282221",
    "FILLER_1": "",
    "FILLER_2": "",
    "FILLER_3": "0",
    "FILLER": "",
    "ADD_DATE": "20241015",
    "ADD_TIME": "101145",
    "ADD_USER": "FSTI02",
    "PROCESS_FG": "",
    "MATCH_PRICE": 138.07,
}
TEMP_DATA_2 = {
    "TRACE_ID": "000173",
    "TRACE_CHANNEL": "uat",
    "FORMAT": "FSOUL01",
    "TRADE_TYPE": "01",
    "ORD_DATE": "20241015",
    "BRANCH_ID": "9A95",
    "ORD_NO": "00000000",
    "ACCOUNT": "09802634",
    "EXCHANGE": "SEHK",
    "STOCK_ID": "00001",
    "QTY": "00000005500",
    "PRICE": 42600.0,
    "BROKER_ID": "30899 ",
    "ORD_TYPE": "2",
    "ORD_TERM": "",
    "INSTRUCTION": "",
    "AGENT_ID": "      ",
    "INTRODUCER": "",
    "BS": "S",
    "PS": "",
    "MATCH_QTY": "00000000000",
    "UNMATHC_QTY": "00000000000",
    "FSOUL01_21": "20241011",
    "FSOUL01_22": "102746",
    "WEB_ID": "129",
    "ORD_SEQ": "07821658",
    "WEB_ID_O": "129",
    "ORD_SEQ_O": "07821658",
    "TRF_FLD": "",
    "ORD_STATUS": "8",
    "RTN_FROM": "1",
    "MSG_ID": "FSC0030",
    "ERR_MSG": "FSC0030 - 委託賣出數量大於客戶庫存數量",
    "FILLER": "",
    "ADD_DATE": "20241011",
    "ADD_TIME": "102746",
    "ADD_USER": "FSTI01",
    "PROCESS_FG": " ",
}


def main():
    dotenv.load_dotenv()
    host = os.environ["SOL_HOST"]
    vpn = os.environ["SOL_VPN"]
    username = os.environ["SOL_USERNAME"]
    client_name = "sb2solace_pub"
    password = os.environ["SOL_PASSWORD"]
    compression_level = int(os.environ["SOL_COMPRESSION_LEVEL"])
    pyrsolace.init_tracing_logger(pyrsolace.LogLevel.Info)
    client = pyrsolace.Client()
    client.connect(
        host,
        vpn,
        username,
        password,
        client_name,
        compression_level=compression_level,
    )
    msg = pyrsolace.Msg(
        topic="R/F/S/E/0000/0000001",
        data=orjson.dumps(TEMP_DATA),
    )
    msg.msg_type = "application/json"
    # msg.set_user_prop("ct", "application/json")

    client.send_msg(msg)
    msg = pyrsolace.Msg(
        topic="R/F/S/E/0000/0000002",
        data=orjson.dumps(TEMP_DATA_2),
    )
    msg.msg_type = "application/json"
    # msg.set_user_prop("ct", "application/json")
    client.send_msg(msg)
    del msg
    client.disconnect()


def sub():
    dotenv.load_dotenv()
    host = os.environ["SOL_HOST"]
    vpn = os.environ["SOL_VPN"]
    username = os.environ["SOL_USERNAME"]
    client_name = os.environ["SOL_CLIENT_NAME"]
    password = os.environ["SOL_PASSWORD"]
    compression_level = int(os.environ["SOL_COMPRESSION_LEVEL"])
    pyrsolace.init_tracing_logger(pyrsolace.LogLevel.Info)
    client = pyrsolace.Client()
    client.connect(
        host,
        vpn,
        username,
        password,
        client_name,
        compression_level=compression_level,
    )
    client.subscribe("R/F/S/>")
    client.set_msg_callback(
        lambda msg: print("topic:", msg.topic, "data:", orjson.loads(msg.data))
    )

    Event().wait()


if __name__ == "__main__":
    main()
