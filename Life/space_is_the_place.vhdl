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

    type state_t is ( VRAM_INIT, SHOW_VRAM, PROCESS_STEP_TIME, SHIFT_N );
    signal state : state_t := VRAM_INIT;

    signal xi : integer;
    signal yi : integer;
    signal yi1 : integer;
    signal yi2 : integer;
    signal l0, l1, l2 : vram_line_t;
    signal age_count : integer := 0;
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
                    vram(0) <= CONV_std_logic_vector(0, 256);
                end loop;
                state <= SHOW_VRAM;
            when SHOW_VRAM =>
                age_count <= age_count + 1;

                write( line0, String'("age:"));
                write( line0, age_count );
                writeline( output, line0);
                for y in 0 to SHOW_MAX_Y - 1 loop
                    vline := vram(0);
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

            when PROCESS_STEP_TIME =>
                if xi = 255 then
                    xi <= 0;
                    state <= SHIFT_N;
                else
                    xi <= xi + 1;
                end if;
                
                d0 := l0(xi);
                d1 := l1(xi);
                d2 := l2(xi);

                l1(xi) <= data_result;
                data_src <= d0 & d1 & d2;

            when SHIFT_N =>
                if xi = 3 then
                    if yi = 255 - 2 then
                        if age_count <= 10 then
                            state <= SHOW_VRAM;
                        end if;
                    else
                        xi <= 0;
                        yi <= yi + 1;
                        yi1 <= yi1 + 1;
                        yi2 <= yi2 + 1;
                        l0 <= vram(yi);
                        l1 <= vram(yi1);
                        l2 <= vram(yi2);
                        state <= PROCESS_STEP_TIME;
                    end if;
                else
                    xi <= xi + 1;
                    l1 <= data_result & l1(255 downto 1);
                end if;
                

            end case;
        end if;
    end process;

end sim;


