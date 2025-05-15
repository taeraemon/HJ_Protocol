#include <stdio.h>
#include "flatbuffers/flatbuffers.h"
#include "telemetry_generated.h"
#include "common_generated.h"

int main() {
    flatbuffers::FlatBufferBuilder builder(1024);

    // config 문자열
    auto config = builder.CreateString("{\"log_level\":\"debug\"}");

    // 필수 필드: state
    HJProtocol::StateBuilder state_builder(builder);
    state_builder.add_boot_time(1234);
    state_builder.add_mode(HJProtocol::OperationMode::ARMED);
    state_builder.add_voltage(12.3f);
    state_builder.add_current(1.1f);
    auto state = state_builder.Finish();

    // Telemetry 빌드
    HJProtocol::TelemetryBuilder tele_builder(builder);
    tele_builder.add_state(state);
    tele_builder.add_config(config);
    auto telemetry = tele_builder.Finish();

    builder.Finish(telemetry);

    // 패킷 길이
    uint8_t* buf = builder.GetBufferPointer();
    int size = builder.GetSize();

    printf("📦 Telemetry 패킷 길이: %d bytes\n", size);

    // 파싱
    auto parsed = HJProtocol::GetTelemetry(buf);
    auto parsed_state = parsed->state();

    printf("\n📡 파싱 결과:\n");
    printf("- mode: %s\n", HJProtocol::EnumNameOperationMode(parsed_state->mode()));
    printf("- voltage: %.2f\n", parsed_state->voltage());
    printf("- current: %.2f\n", parsed_state->current());
    printf("- config: %s\n", parsed->config()->c_str());

    return 0;
}
