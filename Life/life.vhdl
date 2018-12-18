library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity life is
    port(
        clk  : in std_logic;
        din  : in std_logic_vector(2 downto 0);
        mark_in : in std_logic;
        dout : out std_logic;
        mark_out : out std_logic
    );
end life;

architecture RTL of life is
    signal me : std_logic_vector(1 downto 0);
    signal din_d_sum : std_logic_vector( 1 downto 0 );
    signal d101_d : std_logic_vector( 1 downto 0 );

    signal mark_shift : std_logic_vector(2 downto 0);

    signal sum0: std_logic_vector(1 downto 0);
    signal sum01: std_logic_vector(2 downto 0);
    signal dout_reg : std_logic;
begin
    dout <= dout_reg;
    mark_out <= mark_shift(2);
    process(clk)
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
                        if din_d_sum(1) = '1' then
                            if din_d_sum(0) = '0' then
                                dout_reg <= me(1);
                            else
                                dout_reg <= '0';
                            end if;
                        else
                            dout_reg <= '0';
                        end if;
                    when "01" =>
                        if (din_d_sum(1) xor din_d_sum(0)) = '1' then
                            if din_d_sum(0) = '1' then
                                dout_reg <= me(1);
                            else
                                dout_reg <= '1';
                            end if;
                        else
                            dout_reg <= '0';
                        end if;
                    when "10" =>
                        if din_d_sum(1) = '0' then
                            if din_d_sum(0) = '0' then
                                dout_reg <= me(1);
                            else
                                dout_reg <= '1';
                            end if;
                        else
                            dout_reg <= '0';
                        end if;
                    when others => 
                        if din_d_sum = "00" then
                            dout_reg <= '1';
                        else
                            dout_reg <= '0';
                        end if;
                end case;
            end if;

            case sum0 is
                when "00" => 
                    sum01 <= "0" & (d101_d(1) and d101_d(0)) & (d101_d(1) xor d101_d(0));
                when "01" => 
                    if (d101_d(1) xor d101_d(0)) = '0' then
                        if d101_d(0) = '0' then
                            sum01 <= "001";
                        else
                            sum01 <= "100";
                        end if;
                    else
                            sum01 <= "010";
                    end if;
                when "10" => 
                    if (d101_d(1) xor d101_d(0)) = '0' then
                        if d101_d(0) = '0' then
                            sum01 <= "010";
                        else
                            sum01 <= "100";
                        end if;
                    else
                            sum01 <= "011";
                    end if;
                when others =>
                    if d101_d = "00" then
                        sum01 <= "011";
                    else
                        sum01 <= "100";
                    end if;
            end case;
        end if;
    end process;

    process(clk)
    begin
        if clk'event and clk = '1' then
            mark_shift(2) <= mark_shift(1);
            mark_shift(1) <= mark_shift(0);
            mark_shift(0) <= mark_in;
        end if;
    end process;
end RTL;
