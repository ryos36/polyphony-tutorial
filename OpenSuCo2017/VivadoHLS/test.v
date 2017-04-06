module test
  (
    
  );

  //localparams
  localparam CLK_PERIOD = 10;
  localparam CLK_HALF_PERIOD = 5;
  localparam INITIAL_RESET_SPAN = 100;
  localparam test_b1_INIT = 0;
  localparam test_b1_S1 = 1;
  localparam test_b1_S2 = 2;
  localparam test_b1_S3 = 3;
  localparam test_b1_S4 = 4;
  localparam test_forelse5_S0 = 5;
  localparam test_forelse5_FINISH = 6;
  localparam test_L1_fortest3_S0 = 7;
  localparam test_L1_forbody4_S0 = 8;
  localparam test_L1_forbody4_S1 = 9;
  localparam test_L1_forbody4_S2 = 10;
  localparam test_L1_forbody4_S3 = 11;
  localparam test_L1_forbody4_S4 = 12;
  localparam test_L1_forbody4_S5 = 13;
  localparam test_L1_forbody4_S6 = 14;
  localparam test_L1_forbody4_S7 = 15;
  localparam test_L1_forbody4_S8 = 16;
  localparam test_L1_continue6_S0 = 17;
  localparam test_L1_continue6_S1 = 18;
  
  //signals: 
  wire cond1189;
  reg clk;

  reg ap_start;
  wire ap_done;
  wire ap_ready;
  wire ap_idle;

  reg rst;
  reg        [4:0] test_state;
  reg signed [63:0] golden_result2;
  reg signed [63:0] i2;
  reg signed [63:0] i3;
  reg signed [63:0] n2;
  reg signed [63:0] result2;
  //signals: golden_results1
  wire        [2:0] golden_results1_len;
  wire        [63:0] golden_results1_q;
  reg        [2:0] golden_results1_addr;
  reg        [63:0] golden_results1_d;
  reg golden_results1_req;
  reg golden_results1_we;
  //signals: in_n
  reg        [63:0] fib_0_in_n;
  //signals: out_0
  wire        [63:0] fib_0_out_0;
  //signals: ram
  wire        [2:0] array1186_ram_addr;
  wire        [63:0] array1186_ram_d;
  wire        [2:0] array1186_ram_len;
  wire        [63:0] array1186_ram_q;
  wire array1186_ram_we;
  wire        [2:0] array1187_ram_addr;
  wire        [63:0] array1187_ram_d;
  wire        [2:0] array1187_ram_len;
  wire        [63:0] array1187_ram_q;
  wire array1187_ram_we;
  //signals: test_n1
  wire        [2:0] test_n1_len;
  wire        [63:0] test_n1_q;
  reg        [2:0] test_n1_addr;
  reg        [63:0] test_n1_d;
  reg test_n1_req;
  reg test_n1_we;
  //combinations: 
  assign cond1189 = (i2 < 4);
  //combinations: array1186
  assign array1186_ram_addr = test_n1_addr;
  assign array1186_ram_d = test_n1_d;
  assign array1186_ram_we = test_n1_we;
  assign test_n1_len = array1186_ram_len;
  assign test_n1_q = array1186_ram_q;
  //combinations: array1187
  assign array1187_ram_addr = golden_results1_addr;
  assign array1187_ram_d = golden_results1_d;
  assign array1187_ram_we = golden_results1_we;
  assign golden_results1_len = array1187_ram_len;
  assign golden_results1_q = array1187_ram_q;
  //sub modules
  //array1186 instance
  BidirectionalSinglePortRam#(
    .DATA_WIDTH(64),
    .ADDR_WIDTH(3),
    .RAM_LENGTH(4)
    )
    array1186(
      .clk(clk),
      .rst(rst),
      .ram_addr(array1186_ram_addr),
      .ram_d(array1186_ram_d),
      .ram_we(array1186_ram_we),
      .ram_q(array1186_ram_q),
      .ram_len(array1186_ram_len)
    );
  //array1187 instance
  BidirectionalSinglePortRam#(
    .DATA_WIDTH(64),
    .ADDR_WIDTH(3),
    .RAM_LENGTH(4)
    )
    array1187(
      .clk(clk),
      .rst(rst),
      .ram_addr(array1187_ram_addr),
      .ram_d(array1187_ram_d),
      .ram_we(array1187_ram_we),
      .ram_q(array1187_ram_q),
      .ram_len(array1187_ram_len)
    );
  //fib_0 instance
  fib fib_0(
    .ap_clk(clk),
    .ap_rst(rst),
    .ap_start(ap_start),
    .ap_done(ap_done),
    .ap_idle(ap_idle),
    .ap_ready(ap_ready),
    .n(fib_0_in_n[31:0]),
    .ap_return(fib_0_out_0)
  );

  
  initial begin
    //$monitor("%5t:fib_0_in_n=%4d, fib_0_out_0=%4d", $time, fib_0_in_n, fib_0_out_0);
  end
  initial begin
    clk = 0;
    #CLK_HALF_PERIOD
    forever #CLK_HALF_PERIOD clk = ~clk;
  end
  initial begin
    rst <= 1;
    #INITIAL_RESET_SPAN
    rst <= 0;
  end
  

  always @(posedge clk) begin
    if (rst) begin
      ap_start <= 0;
      golden_result2 <= 0;
      i2 <= 0;
      i3 <= 0;
      n2 <= 0;
      test_state <= test_b1_INIT;
    end else begin //if (rst)
      case(test_state)
      test_b1_INIT: begin
        golden_results1_addr <= 0;
        golden_results1_we <= 1;
        golden_results1_req <= 1;
        golden_results1_d <= 0;
        test_n1_addr <= 0;
        test_n1_we <= 1;
        test_n1_req <= 1;
        test_n1_d <= 0;
        i2 <= 0;
        test_state <= test_b1_S1;
      end
      test_b1_S1: begin
        golden_results1_addr <= 1;
        golden_results1_we <= 1;
        golden_results1_req <= 1;
        golden_results1_d <= 1836311903;
        test_n1_addr <= 1;
        test_n1_we <= 1;
        test_n1_req <= 1;
        test_n1_d <= 46;
        test_state <= test_b1_S2;
      end
      test_b1_S2: begin
        golden_results1_addr <= 2;
        golden_results1_we <= 1;
        golden_results1_req <= 1;
        golden_results1_d <= 2971215073;
        test_n1_addr <= 2;
        test_n1_we <= 1;
        test_n1_req <= 1;
        test_n1_d <= 47;
        test_state <= test_b1_S3;
      end
      test_b1_S3: begin
        golden_results1_addr <= 3;
        golden_results1_we <= 1;
        golden_results1_req <= 1;
        golden_results1_d <= 7540113804746346429;
        test_n1_addr <= 3;
        test_n1_we <= 1;
        test_n1_req <= 1;
        test_n1_d <= 92;
        test_state <= test_b1_S4;
      end
      test_b1_S4: begin
        golden_results1_req <= 0;
        test_n1_req <= 0;
        test_state <= test_L1_fortest3_S0;
      end
      test_forelse5_FINISH: begin
        $display("%5t:finish", $time);
        $finish();
      end
      test_L1_fortest3_S0: begin
        /* cond1189 <= (i2 < 4); */
        if (cond1189) begin
          golden_results1_addr <= i2;
          golden_results1_we <= 0;
          golden_results1_req <= 1;
          test_n1_addr <= i2;
          test_n1_we <= 0;
          test_n1_req <= 1;
          $display("%s %t", "time:", $time);
          test_state <= test_L1_forbody4_S1;
        end else begin
          test_state <= test_forelse5_FINISH;
        end
      end
      test_L1_forbody4_S1: begin
        /*wait for output of golden_results1*/
        /*wait for output of test_n1*/
        test_state <= test_L1_forbody4_S2;
      end
      test_L1_forbody4_S2: begin
        golden_result2 <= golden_results1_q;
        golden_results1_req <= 0;
        n2 <= test_n1_q;
        test_n1_req <= 0;
        test_state <= test_L1_forbody4_S3;
      end
      test_L1_forbody4_S3: begin
        ap_start <= 1;
        fib_0_in_n <= n2;
        test_state <= test_L1_forbody4_S4;
      end
      test_L1_forbody4_S4: begin
        test_state <= test_L1_forbody4_S5;
      end
      test_L1_forbody4_S5: begin
        if (ap_done == 1) begin
          result2 <= fib_0_out_0;
          ap_start = 0;
          test_state <= test_L1_forbody4_S7;
        end
      end
      test_L1_forbody4_S7: begin
        test_state <= test_L1_forbody4_S8;
      end
      test_L1_forbody4_S8: begin
        $display("%s %t %s %1d %s %1d", "time:", $time, " ", i2, "=>", result2);
        test_state <= test_L1_continue6_S0;
      end
      test_L1_continue6_S0: begin
        i3 <= (i2 + 1);
        test_state <= test_L1_continue6_S1;
      end
      test_L1_continue6_S1: begin
        i2 <= i3;
        test_state <= test_L1_fortest3_S0;
      end
      endcase
    end
  end
  

endmodule

