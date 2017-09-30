library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity life is
    port(
        clk  : in std_logic;
        din  : in std_logic_vector(2 downto 0);
        dout : out std_logic
    );
end life;

architecture RTL of life is
    signal me : std_logic_vector(1 downto 0);
    signal sum: std_logic_vector(1 downto 0);
    signal din_d  : std_logic_vector(2 downto 0);
    signal din_d_sum : std_logic_vector( 1 downto 0 );

    signal sum0: std_logic_vector(2 downto 0);
    signal sum1: std_logic_vector(1 downto 0);
    signal sum2: std_logic_vector(2 downto 0);
    signal me_sum2: std_logic_vector(3 downto 0);
    signal dout_reg : std_logic;
begin
    me_sum2 <= me(1) & sum2;
    process(clk)
    begin
        if clk'event and clk = '1' then
            din_d <= din;
            me(0) <= din(1);
            me(1) <= me(0);

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

            if sum2(2) = '1' then
                dout_reg <= '0';
            else
                case sum2(1 downto 0) is
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
        end if;
    end process;
end RTL;
