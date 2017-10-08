{ print }
/.*monitor/ { 
    vcd_file = ENVIRON["VCD_FILE"]
    if ( vcd_file == "" ) vcd_file = "wave.vcd"
    print "$dumpfile(\"" vcd_file "\");"

    module_name = ENVIRON["MODULE_NAME"]
    if ( module_name == "" ) module_name = "sbus"
    print "$dumpvars(0, " module_name ");"
}
