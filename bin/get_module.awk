( flag == 1 ) { 
    if ( match($0, / [^ ]*\(/ ))
        print substr($0, RSTART + 1, RLENGTH - 2);
    flag = 0
}
/\/\/.*instance/ { 
    flag = 1
}
