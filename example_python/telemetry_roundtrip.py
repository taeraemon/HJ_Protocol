import flatbuffers
import os
import sys
import pandas as pd

# 경로 설정
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, "..", "flatc_gen", "python"))

from HJProtocol import Telemetry
from HJProtocol import State, NAV, IMU, GPS
from HJProtocol.MaxSv import MaxSv
from HJProtocol.MaxPt import MaxPt
from HJProtocol.MaxTc import MaxTc

# ---------------------------
# 🛠️ 1. Telemetry 생성
# ---------------------------
builder = flatbuffers.Builder(4096)

# 문자열
config_str = builder.CreateString('{"log_level": "debug"}')

# IMU
IMU.IMUStart(builder)
IMU.IMUAddAccx(builder, 0.1)
IMU.IMUAddAccy(builder, 0.2)
IMU.IMUAddAccz(builder, 0.3)
IMU.IMUAddGyrx(builder, 0.4)
IMU.IMUAddGyry(builder, 0.5)
IMU.IMUAddGyrz(builder, 0.6)
imu = IMU.IMUEnd(builder)

# GPS
GPS.GPSStart(builder)
GPS.GPSAddLat(builder, 37.123)
GPS.GPSAddLon(builder, 127.456)
GPS.GPSAddAlt(builder, 123.45)
GPS.GPSAddSat(builder, 10)
GPS.GPSAddFixStatus(builder, 2)
GPS.GPSAddFixType(builder, 3)
GPS.GPSAddTime(builder, 1680000000)
gps = GPS.GPSEnd(builder)

# NAV
NAV.NAVStart(builder)
NAV.NAVAddNavStatus(builder, 3)
NAV.NAVAddNavRoll(builder, 0.0)
NAV.NAVAddNavPitch(builder, 0.1)
NAV.NAVAddNavYaw(builder, 0.2)
NAV.NAVAddNavLat(builder, 37.0)
NAV.NAVAddNavLon(builder, 127.0)
NAV.NAVAddNavAlt(builder, 123.0)
NAV.NAVAddNavQua0(builder, 1.0)
NAV.NAVAddNavQua1(builder, 0.0)
NAV.NAVAddNavQua2(builder, 0.0)
NAV.NAVAddNavQua3(builder, 0.0)
nav = NAV.NAVEnd(builder)

# State
State.StateStart(builder)
State.StateAddBootTime(builder, 100)
State.StateAddModeTime(builder, 200)
State.StateAddMode(builder, 5)
State.StateAddCountdown(builder, 10)
State.StateAddWarnCode(builder, 0)
State.StateAddErrorCode(builder, 0)
State.StateAddVoltage(builder, 12.5)
State.StateAddCurrent(builder, 1.2)
state = State.StateEnd(builder)

# 벡터 생성 함수
def to_camel_case(snake: str) -> str:
    return ''.join(part.capitalize() for part in snake.split('_'))

def create_vector(builder, values, field: str, dtype: str, expected_len_map=None):
    # 길이 자동 검증
    if expected_len_map:
        if field in expected_len_map:
            expected = expected_len_map[field]
            if len(values) != expected:
                raise ValueError(f"❌ Field '{field}' expects {expected} items, but got {len(values)}")

    # 벡터 시작 함수 가져오기
    camel_field = to_camel_case(field)
    start_func = getattr(Telemetry, f"TelemetryStart{camel_field}Vector")
    start_func(builder, len(values))

    # 데이터 유형별 프리펜드
    prepend_map = {
        "float": builder.PrependFloat32,
        "uint8": builder.PrependUint8,
        "uint16": builder.PrependUint16,
    }

    if dtype not in prepend_map:
        raise ValueError(f"Unsupported dtype: {dtype}")

    for v in reversed(values):
        prepend_map[dtype](v)

    return builder.EndVector()

expected_len = {
    "sv":     MaxSv.LEN,
    "pt":     MaxPt.LEN,
    "pt_raw": MaxPt.LEN,
    "tc":     MaxTc.LEN,
    "tc_raw": MaxTc.LEN
}

# 벡터 생성
sv     = create_vector(builder, [i % 2 for i in range(MaxSv.LEN)], "sv", "uint8", expected_len)
pt     = create_vector(builder, [100 + 10 * i for i in range(MaxPt.LEN)], "pt", "float", expected_len)
pt_raw = create_vector(builder, [10000 + 100 * i for i in range(MaxPt.LEN)], "pt_raw", "uint16", expected_len)
tc     = create_vector(builder, [200 + 10 * i for i in range(MaxTc.LEN)], "tc", "float", expected_len)
tc_raw = create_vector(builder, [20000 + 100 * i for i in range(MaxTc.LEN)], "tc_raw", "uint16", expected_len)

# Telemetry 조립
Telemetry.TelemetryStart(builder)
Telemetry.TelemetryAddState(builder, state)
Telemetry.TelemetryAddNav(builder, nav)
Telemetry.TelemetryAddImu(builder, imu)
Telemetry.TelemetryAddGps(builder, gps)
Telemetry.TelemetryAddSv(builder, sv)
Telemetry.TelemetryAddPt(builder, pt)
Telemetry.TelemetryAddPtRaw(builder, pt_raw)
Telemetry.TelemetryAddTc(builder, tc)
Telemetry.TelemetryAddTcRaw(builder, tc_raw)
Telemetry.TelemetryAddConfig(builder, config_str)
telemetry = Telemetry.TelemetryEnd(builder)

builder.Finish(telemetry)
buf = builder.Output()





# ---------------------------
# 🔍 2. 파싱 및 출력 (Python-safe 방식)
# ---------------------------
parsed = Telemetry.Telemetry.GetRootAsTelemetry(buf, 0)

data = {}

# State
state = parsed.State()
if state:
    data["State"] = {
        "boot_time": state.BootTime(),
        "mode_time": state.ModeTime(),
        "mode": state.Mode(),
        "countdown": state.Countdown(),
        "warn_code": state.WarnCode(),
        "error_code": state.ErrorCode(),
        "voltage": state.Voltage(),
        "current": state.Current()
    }

# NAV
nav = parsed.Nav()
if nav:
    data["NAV"] = {
        "status": nav.NavStatus(),
        "roll": nav.NavRoll(),
        "pitch": nav.NavPitch(),
        "yaw": nav.NavYaw(),
        "lat": nav.NavLat(),
        "lon": nav.NavLon(),
        "alt": nav.NavAlt(),
        "qua0": nav.NavQua0(),
        "qua1": nav.NavQua1(),
        "qua2": nav.NavQua2(),
        "qua3": nav.NavQua3()
    }

# IMU
imu = parsed.Imu()
if imu:
    data["IMU"] = {
        "accx": imu.Accx(),
        "accy": imu.Accy(),
        "accz": imu.Accz(),
        "gyrx": imu.Gyrx(),
        "gyry": imu.Gyry(),
        "gyrz": imu.Gyrz()
    }

# GPS
gps = parsed.Gps()
if gps:
    data["GPS"] = {
        "lat": gps.Lat(),
        "lon": gps.Lon(),
        "alt": gps.Alt(),
        "sat": gps.Sat(),
        "fix_status": gps.FixStatus(),
        "fix_type": gps.FixType(),
        "time": gps.Time()
    }

# 벡터들
if parsed.SvLength() > 0:
    data["SV"] = [parsed.Sv(i) for i in range(parsed.SvLength())]
if parsed.PtLength() > 0:
    data["PT"] = [parsed.Pt(i) for i in range(parsed.PtLength())]
if parsed.PtRawLength() > 0:
    data["PT_RAW"] = [parsed.PtRaw(i) for i in range(parsed.PtRawLength())]
if parsed.TcLength() > 0:
    data["TC"] = [parsed.Tc(i) for i in range(parsed.TcLength())]
if parsed.TcRawLength() > 0:
    data["TC_RAW"] = [parsed.TcRaw(i) for i in range(parsed.TcRawLength())]

# 문자열 (Config)
config = parsed.Config()
if config:
    data["CONFIG"] = config

# ---------------------------
# 출력
# ---------------------------
def print_telemetry_vertical(data):
    for section, values in data.items():
        print(f"\n[{section}]")
        if isinstance(values, dict):
            for k, v in values.items():
                print(f"- {k:<18}: {v}")
        elif isinstance(values, list):
            for i, v in enumerate(values):
                print(f"- {section.lower()}[{i}]{' '*(12-len(section))}: {v}")
        else:
            print(f"- {section:<18}: {values}")

print("\n📡 Telemetry 파싱 결과:")
print_telemetry_vertical(data)
print(f"\n📦 패킷 길이: {len(buf)} bytes")
