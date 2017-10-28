library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity life0 is
    port(
        clk  : in std_logic;
        din  : in std_logic;
        dout : out std_logic
    );
end life0;

architecture RTL of life0 is
    signal line: std_logic_vector(2 downto 0);
    signal dout_reg: std_logic;
begin
    dout <= dout_reg;

    process(clk)
    begin
        if clk'event and clk = '1' then
            line(0) <= din;
            line(1) <= line(0);
            line(2) <= line(1);
            case line is
                when "011" =>
                    dout_reg <= '1';
                when "101" =>
                    dout_reg <= '1';
                when "110" =>
                    dout_reg <= '1';
                when others => 
                    dout_reg <= '0';
            end case;
        end if;
    end process;

end RTL;
