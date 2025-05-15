#include <stdio.h>
#include <string.h>
#include "flatbuffers/flatbuffers.h"
#include "telecommand_generated.h"
#include "common_generated.h"

int main() {
    // FlatBuffer 빌더 초기화
    flatbuffers::FlatBufferBuilder builder(1024);

    // 문자열 생성
    auto cmd_config = builder.CreateString("{\"target\": \"orbit\"}");

    // Telecommand 생성
    auto telecommand = HJProtocol::CreateTelecommand(
        builder,
        HJProtocol::OperationMode::FLIGHT,  // enum 값
        cmd_config,
        true                                // cmd_nav
    );

    // Telecommand 버퍼 종료
    builder.Finish(telecommand, HJProtocol::TelecommandIdentifier());

    // 버퍼 가져오기
    uint8_t *buf = builder.GetBufferPointer();
    int size = builder.GetSize();

    printf("📦 생성된 Telecommand 패킷 크기: %d bytes\n", size);

    // ---------------------
    // Telecommand 파싱하기
    // ---------------------
    if (!HJProtocol::TelecommandBufferHasIdentifier(buf)) {
        printf("❌ 유효하지 않은 Telecommand 패킷입니다.\n");
        return 1;
    }

    const HJProtocol::Telecommand *parsed = HJProtocol::GetTelecommand(buf);

    printf("\n📡 파싱된 Telecommand 정보:\n");
    printf("- cmd_mode   : %s\n", HJProtocol::EnumNameOperationMode(parsed->cmd_mode()));
    printf("- cmd_config : %s\n", parsed->cmd_config()->c_str());
    printf("- cmd_nav    : %s\n", parsed->cmd_nav() ? "true" : "false");

    return 0;
}
