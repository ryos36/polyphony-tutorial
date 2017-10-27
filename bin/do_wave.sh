#!/bin/sh
if [ $# -ne 1 ]; then
    echo Usage: $0 '<python file>.py'
    exit 1
fi
BIN_FILE_DIR=`dirname $0`

MODULE_NAME=`basename $1 .py`
FILE_NAME=${MODULE_NAME}.py
if [ ! -e $FILE_NAME ]; then
    echo $FILE_NAME is not exist
    exit 2
fi
WORK_DIR=.tmp
TEST_V=test.v
VCD_TEST_V=vcd_${TEST_V}

#${BIN_FILE_DIR}/compile.py ${MODULE_NAME}.py
./c.py ${MODULE_NAME}.py

export INSTANCE_NAME=`awk -f ${BIN_FILE_DIR}/get_module.awk ${WORK_DIR}/${TEST_V}`
awk -f ${BIN_FILE_DIR}/add_vcd.awk ${WORK_DIR}/${TEST_V} > ${WORK_DIR}/${VCD_TEST_V}
( cd ${WORK_DIR} ; iverilog -o $MODULE_NAME $VCD_TEST_V $MODULE_NAME.v )
mv ${WORK_DIR}/${MODULE_NAME} ${MODULE_NAME}
./${MODULE_NAME}

exit 0
