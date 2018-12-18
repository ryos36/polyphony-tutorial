library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;

use iEEE.std_logic_arith.all;
use iEEE.std_logic_unsigned."-";
use iEEE.std_logic_unsigned."+";

use IEEE.std_logic_textio.all;
library std;
use std.textio.all;

entity life_tb is
end life_tb;
 
architecture behav of life_tb is

component life
    port(
        clk  : in std_logic;
        din  : in std_logic_vector(2 downto 0);
        mark_in : in std_logic;
        dout : out std_logic;
        mark_out : out std_logic
    );
end component;

    signal clk : std_logic;
    signal data0 : std_logic_vector(31 downto 0) := "01111100001010101101110110101010";
    signal data1 : std_logic_vector(31 downto 0) := "11000001111010101101110110001000";
    signal data2 : std_logic_vector(31 downto 0) := "11100000001010101101110110101111";

    signal din : std_logic_vector(2 downto 0);
    signal result : std_logic;
    signal mark_in : std_logic;
    signal mark_out : std_logic;
    signal counter : std_logic_vector(2 downto 0) := "000";
    
    constant clk_period : time := 10 ns;
begin

-------------------------------------------------------------------
din <= data0(31) & data1(31) & data2(31);

life0 : life
port map (
    clk => clk,

    din => din,
    mark_in => mark_in,
    dout => result,
    mark_out => mark_out
);

-------------------------------------------------------------------
clk_producer: process
begin
    clk <= '0';
    wait for clk_period / 2;
    clk <= '1';
    wait for clk_period / 2;
end process;
    
-------------------------------------------------------------------
kicker: process(clk)
    variable line0 : line;
begin
    if clk'event and clk = '1' then
        write( line0, String'("din:"));
        write( line0, din);
        writeline( output, line0);
        data0 <= data0(30 downto 0) & data0(31);
        data1 <= data1(30 downto 0) & data1(31);
        data2 <= data2(30 downto 0) & data2(31);
    end if;
end process;

-------------------------------------------------------------------
cnt: process(clk)
begin
    if clk'event and clk = '1' then
        counter <= counter + 1;
        if mark_in = '1' then
            mark_in <= '0';
        end if;
        if counter = "000" then 
            mark_in <= '1';
        end if;
    end if;
end process;

-------------------------------------------------------------------
data_cosumer: process(clk)
    variable line0 : line;
begin
    if clk'event and clk = '1' then
        write( line0, String'("result:"));
        write( line0, result );
        write( line0, String'(" "));
        write( line0, mark_out );
        writeline( output, line0);
    end if;
end process;

end behav;
