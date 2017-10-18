{ print }
/.*monitor/ { 
    vcd_file = ENVIRON["VCD_FILE"]
    if ( vcd_file == "" ) vcd_file = "wave.vcd"
    print "$dumpfile(\"" vcd_file "\");"

    instance_name = ENVIRON["INSTANCE_NAME"]
    if ( instance_name == "" ) instance_name = "m"
    print "$dumpvars(0, " instance_name ");"
}
