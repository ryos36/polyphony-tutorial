library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity xorshift8 is
    port(
        clk    : in std_logic;
        kick_n : in std_logic;
        d_en_n : out std_logic; 
        data   : out std_logic_vector(7 downto 0)
    );
end xorshift8;

architecture RTL of xorshift8 is
    signal y: std_logic_vector(7 downto 0) := X"a2";
    signal state: std_logic_vector(1 downto 0) := "00";
begin
    data <= y(7 downto 0);

    process(clk)
    begin
        if clk'event and clk = '1' then
            case state is
                when "00" =>
                    d_en_n <= '1';
                    if kick_n = '0' then
                        y <= y xor 
                            (y((7 - 3) downto 0)  & "000");
                        state <= "01";
                    end if;
                when "01" =>
                    y <= y xor 
                        ("00000" & y(7 downto 5));
                    state <= "11";
                when "11" =>
                    y <= y xor 
                        (y((7 - 1) downto 0)  & "0");
                    state <= "10";
                when "10" =>
                    state <= "00";
                    d_en_n <= '0';
                when others => 
                    null;
            end case;
        end if;
    end process;

end RTL;
