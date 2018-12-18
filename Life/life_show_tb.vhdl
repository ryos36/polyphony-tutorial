library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;

use iEEE.std_logic_arith.all;
use iEEE.std_logic_unsigned."-";
use iEEE.std_logic_unsigned."+";

use IEEE.std_logic_textio.all;
library std;
use std.textio.all;

entity life_show_tb is
end life_show_tb;
 
architecture sim of life_show_tb is

----------------------------------------------------------------
component space_is_the_place
    port(
        clk  : in std_logic;

        clk_for_life : out std_logic;

        data_src : out std_logic_vector(2 downto 0);
        mark_src : out std_logic;

        data_result : in std_logic;
        mark_result : in std_logic
    );
end component;

----------------------------------------------------------------
component pattern_detector
    port(
        clk  : in std_logic;
        din  : in std_logic_vector(2 downto 0);
        dout  : out std_logic_vector(2 downto 0);
        
        mark_src : out std_logic
    );
end component;

----------------------------------------------------------------
component life
    port(
        clk  : in std_logic;
        din  : in std_logic_vector(2 downto 0);
        mark_in : in std_logic;
        dout : out std_logic;
        mark_out : out std_logic
    );
end component;

----------------------------------------------------------------
    signal clk : std_logic;

    signal clk_for_life : std_logic;
    signal data_src : std_logic_vector(2 downto 0);
    signal delayed_data_src : std_logic_vector(2 downto 0);
    signal mark_src : std_logic;

    signal data_result : std_logic;
    signal mark_result : std_logic;

    constant clk_period : time := 10 ns;
begin

-------------------------------------------------------------------
space_is_the_place0 : space_is_the_place
port map ( 
    clk => clk,

    clk_for_life => clk_for_life,

    data_src => data_src,
    --mark_src => mark_src,

    data_result => data_result,
    mark_result => mark_result
);

-------------------------------------------------------------------
pattern_detector0 : pattern_detector
port map (
    clk => clk_for_life,

    din => data_src,
    dout => delayed_data_src,

    mark_src => mark_src
);

-------------------------------------------------------------------
life0 : life
port map (
    clk => clk_for_life,

    din => delayed_data_src,
    mark_in => mark_src,
    dout => data_result,
    mark_out => mark_result
);

-------------------------------------------------------------------
clk_producer: process
begin
    clk <= '0';
    wait for clk_period / 2;
    clk <= '1';
    wait for clk_period / 2;
end process;
    
end sim;
