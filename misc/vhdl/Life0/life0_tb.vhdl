library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;

use IEEE.std_logic_textio.all;
library std;
use std.textio.all;

entity life0_tb is
end life0_tb;
 
architecture behav of life0_tb is

component life0
    port(
        clk  : in std_logic;
        din  : in std_logic;
        dout : out std_logic
    );
end component;

    signal clk : std_logic;
    signal data : std_logic_vector(31 downto 0) 
     := "01110101111010101101110110101011";

    signal din : std_logic;
    signal result : std_logic;
    
    constant clk_period : time := 10 ns;
begin

-------------------------------------------------------------------
din <= data(0);

l0 : life0
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
        data <= data(0) & data(31 downto 1);
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
