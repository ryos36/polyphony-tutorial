module spi_top (
    input  wire clk,        // 27M clock

    inout  wire SPI_MISO, 
    inout  wire SPI_MOSI, 
    inout  wire SPI_SCLK, 
    output wire SPI_CS_N, 

    output wire REDn,
    output wire GREEN_N,
    output wire BLUE_N);

    //----------------------------------------------------------------
    wire sbus_ack;
    wire sbus_stb; 
    wire sbus_rw; 
    wire [7:0] sbus_addr;
    wire [7:0] sbus_data_in;
    wire [7:0] sbus_data_out;
    wire sbus_led;

    wire sbus_rst;
    wire sbus_ipdone;
    wire sbus_ipdone;

    wire SPIIRQ_not_used;
    wire SPIWKUP_not_sued;

    wire SO_not_used; 
    wire SOE_not_used;

    wire SPI_MO ; 
    wire SPI_MOoe ; 

    //assign sbus_ack = 1'b0;
    //assign sbus_stb = 1'b0;
    //assign sbus_rw = 1'b0;

    wire SPI_SCKo ; 
    wire SPI_SCKoe ; 
    wire SPI_SCLKi;

    wire [3:0] SPI_MCSNo; 
    wire [3:0] SPI_MCSNoe; 
    wire [3:0] SPI_MCSN;

    assign SPI_SCLK = (SPI_SCKoe ? SPI_SCKo : 1'bz) ; 

    //----------------------------------------------------------------
    wire red_wire;
    wire green_wire_0;
    wire green_wire_1;
    wire green_wire;
    wire  blue_wire;
    wire [2:0] debug_wire;

    assign red_wire = debug_wire[2];
    assign green_wire_0 = debug_wire[1];
    assign blue_wire = debug_wire[0];
    //assign green_wire = green_wire_0 & green_wire_1;
    assign green_wire = green_wire_0;

    //assign SPI_SCLK = 1'b0;
    //assign SPI_MOSI = green_wire_1;
    //assign SPI_CS_N = green_wire_1;

//    always @(posedge clk) begin
//        if (sbus_stb) begin
//            sbus_ack <= 1'b1;
//        end 
//        if (sbus_ack) begin
//            sbus_ack <= 1'b0;
//        end 
//    end

    //----------------------------------------------------------------
    Blink_blink U0 (
      .clk(clk),
      .rst(0),
      .led(green_wire_1)
    );

    //----------------------------------------------------------------
    system_bus_sbus sbus(
        .clk(clk),
        .rst(0),
        .ack(sbus_ack),
        .data_in(sbus_data_in),
        .debug(debug_wire),
        .stb(sbus_stb),
        .rw(sbus_rw),
        .addr(sbus_addr),
        .data_out(sbus_data_out),
        .led(sbus_led),

        .sbus_reset(sbus_rst),
        .sbus_ipload(sbus_ipload),
        .sbus_ipdone(sbus_ipdone)
    );

    wire spi_miso_wire;
    wire spi_mosi_wire;
    wire spi_mclk_wire;

    spi_primitive spi_prim(
        .SPI2_MISO(SPI_MISO), 
        .SPI2_MOSI(SPI_MOSI), 
        .SPI2_SCK(SPI_SCLK), 
        .SPI2_SCSN(1'b1), 
        .SPI2_MCSN(SPI_MCSN),

        .RST(sbus_rst), 
        .IPLOAD(sbus_ipload), 
        .IPDONE(sbus_ipdone), 
        .SBCLKi(clk), 

    // System bus interface to all 4 Hard IP blocks
        .SBWRi(sbus_rw), 
        .SBSTBi(sbus_stb), 
        .SBADRi(sbus_addr), 
        .SBDATi(sbus_data_out), 
        .SBDATo(sbus_data_in), 
        .SBACKo(sbus_ack)
        
    //output wire [1:0] I2CPIRQ, 
    //output wire [1:0] I2CPWKUP, 
    //output wire [1:0] SPIPIRQ, 
    //output wire [1:0] SPIPWKUP
    );

    //----------------------------------------------------------------
//    SB_SPI #(.BUS_ADDR74("0b0000"))
//      SB_SPI_INST_LT 
//       (.SBCLKI(clk),
//        .SBRWI(sbus_rw),
//        .SBSTBI(sbus_stb),
//        .SBADRI7(sbus_addr[7]),
//        .SBADRI6(sbus_addr[6]),
//        .SBADRI5(sbus_addr[5]),
//        .SBADRI4(sbus_addr[4]),
//        .SBADRI3(sbus_addr[3]),
//        .SBADRI2(sbus_addr[2]),
//        .SBADRI1(sbus_addr[1]),
//        .SBADRI0(sbus_addr[0]),
//        .SBDATI7(sbus_data_out[7]),
//        .SBDATI6(sbus_data_out[6]),
//        .SBDATI5(sbus_data_out[5]),
//        .SBDATI4(sbus_data_out[4]),
//        .SBDATI3(sbus_data_out[3]),
//        .SBDATI2(sbus_data_out[2]),
//        .SBDATI1(sbus_data_out[1]),
//        .SBDATI0(sbus_data_out[0]),
//        
//        .MI(SPI_MISO),
//
//        .SI(1'b0),
//        .SCKI(1'b0),
//        .SCSNI(1'b1),
//
//        .SBDATO7(sbus_data_in[7]),
//        .SBDATO6(sbus_data_in[6]),
//        .SBDATO5(sbus_data_in[5]),
//        .SBDATO4(sbus_data_in[4]),
//        .SBDATO3(sbus_data_in[3]),
//        .SBDATO2(sbus_data_in[2]),
//        .SBDATO1(sbus_data_in[1]),
//        .SBDATO0(sbus_data_in[0]),
//        .SBACKO(sbus_ack),
//
//        .SPIIRQ(SPIIRQ_not_used),
//        .SPIWKUP(SPIWKUP_not_sued),
//
//        .SO(SO_not_used),
//        .SOE(SOE_not_used),
//        .MO(SPI_MO),
//        .MOE(SPI_MOoe),
//
//        .SCKO(SPI_SCKo),
//        .SCKOE(SPI_SCKoe),
//
//        .MCSNO3(SPI_MCSNo[3]),
//        .MCSNO2(SPI_MCSNo[2]),
//        .MCSNO1(SPI_MCSNo[1]),
//        .MCSNO0(SPI_MCSNo[0]),
//        .MCSNOE3(SPI_MCSNoe[3]),
//        .MCSNOE2(SPI_MCSNoe[2]),
//        .MCSNOE1(SPI_MCSNoe[1]),
//        .MCSNOE0(SPI_MCSNoe[0]));

    //assign SPI_MOSI = (SPI_MOoe ? SPI_MO : 1'bz) ; 
    //assign SPI_MOSI = SPI_MO; 
    //assign SPI_MCSN[3] = (SPI_MCSNoe[3] ? SPI_MCSNo[3] : 1'bz) ; 
    //assign SPI_MCSN[2] = (SPI_MCSNoe[2] ? SPI_MCSNo[2] : 1'bz) ; 
    //assign SPI_MCSN[1] = (SPI_MCSNoe[1] ? SPI_MCSNo[1] : 1'bz) ; 
    //assign SPI_MCSN[0] = (SPI_MCSNoe[0] ? SPI_MCSNo[0] : 1'bz) ; 

    assign SPI_CS_N = SPI_MCSN[0] | SPI_MCSN[1] | SPI_MCSN[2] | SPI_MCSN[3];
    //assign SPI_CS_N = 1'b0;

    //------------------------------
    // Instantiate RGB primitives
    //------------------------------
    SB_RGBA_DRV RGB_DRIVER (
      .RGBLEDEN (1'b1),
      .RGB0PWM  (red_wire),
      .RGB1PWM  (green_wire),
      .RGB2PWM  (blue_wire),
      .CURREN   (1'b1), 
      .RGB0     (REDn),		//Actual Hardware connection
      .RGB1     (GREEN_N),
      .RGB2     (BLUE_N)
    );

    defparam RGB_DRIVER.RGB0_CURRENT = "0b000001";
    defparam RGB_DRIVER.RGB1_CURRENT = "0b000001";
    defparam RGB_DRIVER.RGB2_CURRENT = "0b000001";
endmodule


