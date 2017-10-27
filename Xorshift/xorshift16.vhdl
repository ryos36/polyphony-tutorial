library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity xorshift16 is
    port(
        clk    : in std_logic;
        rst_n  : in std_logic;
        kick_n : in std_logic;
        d_en_n : out std_logic; 
        data   : out std_logic_vector(3 downto 0)
    );
end xorshift16;

architecture RTL of xorshift16 is
    signal y: std_logic_vector(15 downto 0) := X"8ca2";
    signal state: std_logic_vector(3 downto 0) := "0000";
begin
    process(clk)
    begin
        if clk'event and clk = '1' then
            if rst_n = '0' then
                d_en_n <= '1';
                state <= "0000";
            else
                case state is
                    when "0000" =>
                        if kick_n = '0' then
                            y <= y xor 
                                (y((15 - 2) downto 0)  & "00");
                            state <= "0001";
                        end if;
                    when "0001" =>
                        y <= y xor 
                            ("00000" & y(15 downto 5));
                        state <= "0011";
                    when "0011" =>
                        y <= y xor 
                            (y((15 - 8) downto 0)  & "00000000");
                        state <= "0010";
                    when "0010" =>
                        state <= "0110";
                        d_en_n <= '0';
                        data <= y(3 downto 0);
                    when "0110" =>
                        state <= "0111";
                        data <= y(7 downto 4);
                    when "0111" =>
                        state <= "0101";
                        data <= y(11 downto 8);
                    when "0101" =>
                        state <= "0100";
                        data <= y(15 downto 12);
                    when "0100" =>
                        d_en_n <= '1';
                        state <= "0000";
                    when others => 
                        null;
                end case;
            end if;
        end if;
    end process;

end RTL;
