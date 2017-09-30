library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use IEEE.std_logic_textio.all;
library std;
use std.textio.all;

entity life is
    port(
        clk  : in std_logic;
        din  : in std_logic_vector(2 downto 0);
        dout : out std_logic
    );
end life;

architecture RTL of life is
    signal me : std_logic_vector(1 downto 0);
    signal din_d_sum : std_logic_vector( 1 downto 0 );
    signal d101_d : std_logic_vector( 1 downto 0 );

    signal sum0: std_logic_vector(1 downto 0);
    signal sum01: std_logic_vector(2 downto 0);
    signal dout_reg : std_logic;
begin
    dout <= dout_reg;
    process(clk)
    variable line0 : line;
    begin
        if clk'event and clk = '1' then
            me(0) <= din(1);
            me(1) <= me(0);
            d101_d <= din(2) & din(0);

            case din is
                when "000" =>
                    din_d_sum <= "00";
                when "001" =>
                    din_d_sum <= "01";
                when "010" =>
                    din_d_sum <= "01";
                when "100" =>
                    din_d_sum <= "01";
                when "111" =>
                    din_d_sum <= "11";
                when others => 
                    din_d_sum <= "10";
            end case;
            sum0 <= din_d_sum;

            if sum01(2) = '1' then
                dout_reg <= '0';
            else
                case sum01(1 downto 0) is
                    when "00" =>
                        case din_d_sum is
                            when "10" =>
                                dout_reg <= me(1);
                            when "11" =>
                                dout_reg <= '1';
                            when others => 
                                dout_reg <= '0';
                        end case;
                    when "01" =>
                        case din_d_sum is
                            when "01" =>
                                dout_reg <= me(1);
                            when "10" =>
                                dout_reg <= '1';
                            when others => 
                                dout_reg <= '0';
                        end case;
                    when "10" =>
                        case din_d_sum is
                            when "00" =>
                                dout_reg <= me(1);
                            when "01" =>
                                dout_reg <= '1';
                            when others => 
                                dout_reg <= '0';
                        end case;
                    when others => 
                        case din_d_sum is
                            when "00" =>
                                dout_reg <= '1';
                            when others => 
                                dout_reg <= '0';
                        end case;
                end case;
            end if;

            case sum0 is
                when "00" => 
                    sum01 <= "0" & (d101_d(1) and d101_d(0)) & (d101_d(1) xor d101_d(0));
                when "01" => 
                    case d101_d is
                        when "00" =>
                            sum01 <= "001";
                        when "11" =>
                            sum01 <= "100";
                        when others => 
                            sum01 <= "010";
                    end case;
                when "10" => 
                    case d101_d is
                        when "00" =>
                            sum01 <= "010";
                        when "11" =>
                            sum01 <= "100";
                        when others => 
                            sum01 <= "011";
                    end case;
                when others =>
                    case din_d_sum is
                        when "00" =>
                            sum01 <= "011";
                        when others => 
                            sum01 <= "100";
                    end case;
            end case;
        end if;
    end process;
end RTL;
