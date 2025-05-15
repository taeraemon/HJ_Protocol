
pip install flatbuffers

.\flatc.exe --python --python-typing --gen-name-strings -o flatc_gen\python schema\telemetry.fbs schema\telecommand.fbs schema\common.fbs

.\flatc.exe -c --scoped-enums --gen-object-api -o flatc_gen\c schema\common.fbs schema\telemetry.fbs schema\telecommand.fbs
