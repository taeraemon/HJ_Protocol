

## 1. 📁 디렉토리 구조

```
HJ_Protocol/
├── schema/               # FlatBuffers .fbs 파일들
├── flatc_gen/
│   ├── python/           # Python용 generated 코드
│   └── c/                # C/C++용 generated 코드
├── example_c/            # C/C++ 테스트 예제
│   ├── telecommand_roundtrip.c
│   ├── telemetry_roundtrip.c
│   └── flatbuffers/      # FlatBuffers 헤더 포함
```
---



&nbsp;

&nbsp;

## 2. ⚙️ 의존성 설치 (Windows)

🐍 Python
```
pip install flatbuffers
```

🧰 FlatBuffers 컴파일러
- 코드 생성을 위해 flatc.exe 다운로드 (https://github.com/google/flatbuffers/releases)
- C/C++ 기반 개발을 위해 flatbuffers/include/flatbuffers 를 복사해서 활용.
---



&nbsp;

&nbsp;

## 3. 🛠️ 코드 생성 (FlatBuffers → Python/C++)

✅ Python용 코드 생성
```
.\flatc.exe --python --python-typing --gen-name-strings -o flatc_gen\python schema\telemetry.fbs schema\telecommand.fbs schema\common.fbs
```

✅ C/C++용 코드 생성
```
.\flatc.exe -c --scoped-enums --gen-object-api -o flatc_gen\c schema\common.fbs schema\telemetry.fbs schema\telecommand.fbs
```
---



&nbsp;

&nbsp;

## 4. 🧪 테스트 예제 빌드 & 실행

🚀 Telemetry 예제
```
g++ example_c/telecommand_roundtrip.c -std=c++17 -Iexample_c -Iflatc_gen/c -o telecommand_roundtrip
```
🚀 Telecommand 예제
```
g++ example_c/telemetry_roundtrip.c -std=c++17 -Iexample_c -Iflatc_gen/c -o telemetry_roundtrip
```
---