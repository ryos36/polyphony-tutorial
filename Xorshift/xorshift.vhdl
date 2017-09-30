library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity xorshift is
    port(
        clk    : in std_logic;
        rst_n  : in std_logic;
        kick_n : in std_logic;
        d_en_n : out std_logic; 
        data   : out std_logic_vector(3 downto 0)
    );
end xorshift;

architecture RTL of xorshift is
    signal y: std_logic_vector(31 downto 0) := X"92d68ca2";
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
                                (y((31 - 13) downto 0)  & "0000000000000");
                            state <= "0001";
                        end if;
                    when "0001" =>
                        y <= y xor 
                            ("00000000000000000" & y(31 downto 17));
                        state <= "0011";
                    when "0011" =>
                        y <= y xor 
                            (y((31 - 5) downto 0)  & "00000");
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
                        state <= "1100";
                        data <= y(19 downto 16);
                    when "1100" =>
                        state <= "1101";
                        data <= y(23 downto 20);
                    when "1101" =>
                        state <= "1111";
                        data <= y(27 downto 24);
                    when "1111" =>
                        state <= "1110";
                        data <= y(31 downto 28);
                    when "1110" =>
                        state <= "1010";
                        d_en_n <= '1';
                    when "1010" =>
                        state <= "1000";
                    when "1000" =>
                        state <= "0000";
                    when others => 
                        null;
                end case;
            end if;
        end if;
    end process;

end RTL;
