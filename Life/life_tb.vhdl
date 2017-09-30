library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;

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
        dout : out std_logic
    );
end component;

    signal clk : std_logic;
    signal data0 : std_logic_vector(31 downto 0) 
     := "01110101111010101101110110101011";
    signal data1 : std_logic_vector(31 downto 0) 
     := "01110101111010101101110110101011";
    signal data2 : std_logic_vector(31 downto 0) 
     := "01110101111010101101110110101011";

    signal din : std_logic_vector(2 downto 0);
    signal result : std_logic;
    
    constant clk_period : time := 10 ns;
begin

-------------------------------------------------------------------
din <= data0(31) & data1(31) & data2(31);

life0 : life
port map (
    clk => clk,

    din => din,
    dout => result
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
begin
    if clk'event and clk = '1' then
        data0 <= data0(30 downto 0) & data0(31);
        data1 <= data1(30 downto 0) & data1(31);
        data2 <= data2(30 downto 0) & data2(31);
    end if;
end process;

-------------------------------------------------------------------
data_cosumer: process(clk)
    variable line0 : line;
begin
    if clk'event and clk = '1' then
        write( line0, String'("result:"));
        write( line0, result );
        writeline( output, line0);
    end if;
end process;

end behav;
