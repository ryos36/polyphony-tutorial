library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

use IEEE.std_logic_arith.all;
use IEEE.std_logic_unsigned."-";
use IEEE.std_logic_unsigned."+";

use IEEE.std_logic_textio.all;
library std;
use std.textio.all;

entity space_is_the_place is
    generic
    (
        SHOW_MAX_X : integer := 70;
        SHOW_MAX_Y : integer := 23
    );
    port(
        clk  : in std_logic;

        clk_for_life : out std_logic;

        data_src : out std_logic_vector(2 downto 0);
        mark_src : out std_logic;

        data_result : in std_logic;
        mark_result : in std_logic
    );
end space_is_the_place;
 
architecture sim of space_is_the_place is
    subtype vram_line_t is std_logic_vector(255 downto 0); 
    type vram_t is array(0 to 255) of vram_line_t;
    signal vram : vram_t;

    type state_t is ( VRAM_INIT, SHOW_VRAM, PROCESS_STEP_TIME, CLOCK0, CLOCK1, CLOCK2, SHIFT_N, HALT );
    signal state : state_t := VRAM_INIT;

    signal xi : integer;
    signal yi : integer;
    signal yi1 : integer;
    signal yi2 : integer;
    signal l0, l1, l2, result_line : vram_line_t;
    signal age_count : integer := 0;

    type glider_gun_t is array(0 to 8) of std_logic_vector(46 downto 0);
    constant glider_gun : glider_gun_t :=
        ( "00000000000000000000000001000000000000000000000",
          "00000000000000000000000101000000000000000000000",
          "00000000000001100000011000000000000110000000000",
          "00000000000010001000011000000000000110000000000",
          "01100000000100000100011000000000000000000000000",
          "01100000000100010110000101000000000000000000000",
          "00000000000100000100000001000000000000000000000",
          "00000000000010001000000000000000000000000000000",
          "00000000000001100000000000000000000000000000000" );

    procedure make_blinker(
        vram : inout vram_t;
        x : integer;
        y : integer
    ) is
        variable vline : vram_line_t;
        constant blinker : std_logic_vector(2 downto 0) := "111";
    begin
        vline := vram(y);
        for i in 0 to 2 loop
            vline(xi + i) := blinker(i);
        end loop;
        
    end make_blinker;

begin

    process(clk)
        variable line0 : line;
        variable vline : vram_line_t;
        variable d0, d1, d2 : std_logic;
    begin
        if clk'event and clk = '1' then
            case state is
            when VRAM_INIT =>
                for y in 0 to 255 loop
                    vram(y) <= CONV_std_logic_vector(0, 256);
                end loop;

                -- make blinker
                for i in 0 to 2 loop
                    --vram(2)(10 + i) <= '1';
                end loop;

                for gy in 0 to 8 loop
                    for gx in 0 to 46 loop
                        vram(3 + gy)(4 + gx) <= glider_gun(gy)(46 - gx);
                    end loop;
                end loop;
                
                state <= SHOW_VRAM;
            when SHOW_VRAM =>
                age_count <= age_count + 1;

                write( line0, String'("age:"));
                write( line0, age_count );
                writeline( output, line0);
                for y in 0 to SHOW_MAX_Y - 1 loop
                    vline := vram(y);

                    for x in 0 to SHOW_MAX_X - 1 loop
                        if vline(x) = '1' then
                            write( line0, String'("*"));
                        else
                            write( line0, String'(" "));
                        end if;
                    end loop;
                    writeline(output, line0);
                end loop;
                
                yi <= 1;
                yi1 <= 2;
                yi2 <= 3;
                xi <= 0;
                l0 <= vram(0);
                l1 <= vram(1);
                l2 <= vram(2);

                state <= PROCESS_STEP_TIME;
                if age_count = 2 then
                    --state <= HALT;
                end if;

            when PROCESS_STEP_TIME =>
                if xi = 255 then
                    state <= CLOCK1;
                else
                    state <= CLOCK0;
                end if;
                
                d0 := l0(xi);
                d1 := l1(xi);
                d2 := l2(xi);

--                write( line0, String'("data_result:"));
--                write( line0, data_result );
--                write( line0, String'(" xi:"));
--                write( line0, xi );
--                write( line0, String'(" d:"));
--                write( line0, d0 );
--                write( line0, String'("-"));
--                write( line0, d1 );
--                write( line0, String'("-"));
--                write( line0, d2 );
--                writeline( output, line0);

                data_src <= d0 & d1 & d2;
                clk_for_life <= '1';

            when CLOCK0 =>
                xi <= xi + 1;
                if mark_result = '1' then
                    result_line(xi) <= '1';
                else
                    result_line(xi) <= data_result;
                end if;
                clk_for_life <= '0';
                state <= PROCESS_STEP_TIME;

            when CLOCK1 =>
                xi <= 0;
                if mark_result = '1' then
                    result_line(xi) <= '1';
                else
                    result_line(xi) <= data_result;
                end if;
                clk_for_life <= '0';
                state <= CLOCK2;

            when CLOCK2 =>
                clk_for_life <= '1';
                state <= SHIFT_N;

            when SHIFT_N =>
                if xi = 4 then
                    if yi = 255 - 2 then
                        --if age_count <= 10 then
                        state <= SHOW_VRAM;
                        --end if;
                    else
                        xi <= 0;
                        yi <= yi + 1;
                        yi1 <= yi1 + 1;
                        yi2 <= yi2 + 1;
                        l0 <= vram(yi);
                        l1 <= vram(yi1);
                        l2 <= vram(yi2);
                        vram(yi) <= result_line;
                        state <= PROCESS_STEP_TIME;
                    end if;
                else
                    xi <= xi + 1;
                    if mark_result = '1' then
                        result_line <= '1' & result_line(255 downto 1);
                    else
                        result_line <= data_result & result_line(255 downto 1);
                    end if;
                    state <= CLOCK2;
                end if;
                clk_for_life <= '0';

            when HALT =>
            end case;
        end if;
    end process;

end sim;
