import sys
import os

# 경로 설정
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, "..", "flatc_gen", "python"))

import flatbuffers
from HJProtocol import Telecommand
from HJProtocol.OperationMode import OperationMode


# ---------------------------
# 🛠️ 1. Telecommand 생성
# ---------------------------
builder = flatbuffers.Builder(1024)
config_str = builder.CreateString('{"gain": 1.5, "alt": 120}')

Telecommand.TelecommandStart(builder)
Telecommand.TelecommandAddCmdMode(builder, OperationMode.FLIGHT)
Telecommand.TelecommandAddCmdConfig(builder, config_str)
Telecommand.TelecommandAddCmdNav(builder, True)
cmd = Telecommand.TelecommandEnd(builder)

builder.Finish(cmd)
buf = builder.Output()

print("✅ Telecommand 패킷 생성 완료")

# ---------------------------
# 🔍 2. Telecommand 파싱
# ---------------------------
cmd_parsed = Telecommand.Telecommand.GetRootAsTelecommand(buf, 0)

print("\n🛰️ Telecommand 파싱 결과:")
print(f"- Mode:              {cmd_parsed.CmdMode()}")
print(f"- Nav:               {cmd_parsed.CmdNav()}")
print(f"- Config(JSON str):  {cmd_parsed.CmdConfig()}")
