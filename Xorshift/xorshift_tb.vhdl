library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;

use IEEE.std_logic_textio.all;
library std;
use std.textio.all;

entity xorshift_tb is
end xorshift_tb;
 
architecture behav of xorshift_tb is

component xorshift
    port(
        clk    : in std_logic;
        rst_n  : in std_logic;
        kick_n : in std_logic;
        d_en_n : out std_logic; 
        data   : out std_logic_vector(3 downto 0)
    );
end component;

component xorshift16
    port(
        clk    : in std_logic;
        rst_n  : in std_logic;
        kick_n : in std_logic;
        d_en_n : out std_logic; 
        data   : out std_logic_vector(3 downto 0)
    );
end component;

component xorshift8
    port(
        clk    : in std_logic;
        kick_n : in std_logic;
        d_en_n : out std_logic; 
        data   : out std_logic_vector(7 downto 0)
    );
end component;

    signal clk : std_logic;
    signal rst_n : std_logic;
    signal kick_n : std_logic;
    signal d_en_n : std_logic;
    signal data : std_logic_vector(3 downto 0);
    signal data8 : std_logic_vector(7 downto 0);

    signal d_en_n_d : std_logic;

    signal result : std_logic_vector(31 downto 0);
    signal result_done : std_logic;
    constant clk_period : time := 10 ns;
begin

-------------------------------------------------------------------
xorshift0 : xorshift8
port map (
    clk => clk,

    kick_n  => kick_n,

    d_en_n => d_en_n,
    data => data8
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
reset_sequence: process
begin
    rst_n <= '1';
    wait for clk_period * 2;

    rst_n <= '0';
    wait for clk_period * 8;

    rst_n <= '1';
    wait;
end process;

-------------------------------------------------------------------
kicker: process
    variable line0 : line;
begin
    kick_n <= '1';
    wait for clk_period * 16;

    kick_n <= '0';
    wait for clk_period * 3;
    write( line0, String'("kick it!"));
    writeline( output, line0);

    kick_n <= '1';

    while( result_done = '0') loop
        wait for clk_period / 2;
    end loop;
    wait for clk_period * 160000;

end process;

-------------------------------------------------------------------
data_cosumer: process(clk)
    variable line0 : line;
begin
    if rst_n = '0' then
        result_done <= '0';
    end if;
    
    if clk'event and clk = '1' then
        d_en_n_d <= d_en_n;
        if d_en_n = '1' then
            result <= ( others => '0' );
            if d_en_n_d = '0' then
                write( line0, String'("result:"));
                write( line0, result );
                writeline( output, line0);
            end if;
        else
            result(7 downto 0) <= data8;
            --result(31 downto 28) <= data;
            --result(27 downto 0) <= result(31 downto 4);
            --  write( line0, String'("now get data:"));
            --  write( line0, result );
            --  writeline( output, line0);
        end if;

        if result_done = '1' then
            result_done <= '0';
        end if;

        if d_en_n_d = '0' and d_en_n = '1' then
            result_done <= '1';
        end if;
    end if;
end process;

end behav;
