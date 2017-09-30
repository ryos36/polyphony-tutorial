#!/bin/sh
if [ -e makefile ] ; then
    echo makefile is exist!
    exit 2
fi
GHDL_FLAGS="--std=08 --ieee=standard"
#GHDL_FLAGS="--ieee=synopsys"

#ghdl -i $GHDL_FLAGS --work=unisim unisims/*.vhd
#ghdl -i $GHDL_FLAGS --work=unisim unisims/primitive/*.vhd
#ghdl -i $GHDL_FLAGS --work=unimacro unimacro/*.vhd

SOURCES="xorshift.vhdl xorshift16.vhdl xorshift8.vhdl xorshift_tb.vhdl"
for i in $SOURCES
do
        echo ghdl -a $GHDL_FLAGS $i
        ghdl -a $GHDL_FLAGS $i
        if [ $? = 1 ] ; then 
            exit 1
        fi
done

TOP_MODULE=xorshift_tb
ghdl -m $GHDL_FLAGS -fexplicit $TOP_MODULE
ghdl --gen-makefile $GHDL_FLAGS $TOP_MODULE > makefile
