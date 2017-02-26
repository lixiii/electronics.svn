`timescale 1ns / 1ps

module top(
    input nRST,
	 
	 output BATT_1_EN,
	 output BATT_2_EN,
	 output nBATT_BOTH_EN,
	 
	 input MCU_IN_BATT_1_EN,
	 input MCU_IN_BATT_2_EN,
	 input MCU_IN_BATT_BOTH_EN,
	 
	 output PWR_OUT_EN_1,
	 output PWR_OUT_EN_2,
	 output PWR_OUT_EN_3,
	 output PWR_OUT_EN_4,
	 output PWR_OUT_EN_5,
	 output PWR_OUT_EN_6,
	 output PWR_OUT_EN_7,
	 output nPWR_OUT_EN_8,
	 output nPWR_OUT_EN_9,
	 
	 input MCU_IN_EN_1,
	 input MCU_IN_EN_2,
	 input MCU_IN_EN_3,
	 input MCU_IN_EN_4,
	 input MCU_IN_EN_5,
	 input MCU_IN_EN_6,
	 input MCU_IN_EN_7,
	 input MCU_IN_EN_8,
	 input MCU_IN_EN_9,
	 
	 input KILLSWITCH_RED,
	 output MCU_OUT_KILLSWITCH_ACTIVE,
	 
	 input MCU_CLK_IN
    );

// standard reset assignment
wire rst;
assign rst = ~nRST;

// killswitch management
wire killswitch_active;
assign killswitch_active = KILLSWITCH_RED;
assign MCU_OUT_KILLSWITCH_ACTIVE = killswitch_active;

// logic simplification
wire batt_both_en;
assign nBATT_BOTH_EN = ~batt_both_en;

wire pwr_out_en_8;
assign nPWR_OUT_EN_8 = ~pwr_out_en_8;
wire pwr_out_en_9;
assign nPWR_OUT_EN_9 = ~pwr_out_en_9;


// battery enable states
reg BATT_1_EN_s;
reg BATT_2_EN_s;
reg batt_both_en_s;
assign BATT_1_EN = BATT_1_EN_s;
assign BATT_2_EN = BATT_2_EN_s;
assign batt_both_en = batt_both_en_s; // not capitalised, because (see above lines)

// FET output states
reg pwr_out_1_s;
reg pwr_out_2_s;
reg pwr_out_3_s;
reg pwr_out_4_s;
reg pwr_out_5_s;
reg pwr_out_6_s;
reg pwr_out_7_s;
reg pwr_out_8_s;
reg pwr_out_9_s;

// make FET outputs mirror our internal state, but be overidden by the kill switch
assign PWR_OUT_EN_1 = pwr_out_1_s & !killswitch_active;
assign PWR_OUT_EN_2 = pwr_out_2_s;
assign PWR_OUT_EN_3 = pwr_out_3_s;
assign PWR_OUT_EN_4 = pwr_out_4_s;
assign PWR_OUT_EN_5 = pwr_out_5_s;
assign PWR_OUT_EN_6 = pwr_out_6_s;
assign PWR_OUT_EN_7 = pwr_out_7_s;
assign pwr_out_en_8 = pwr_out_8_s;
assign pwr_out_en_9 = pwr_out_9_s;

always @ (posedge rst, negedge MCU_CLK_IN)
begin
	if (rst == 1) begin
		BATT_1_EN_s <= 0;
		BATT_2_EN_s <= 0;
		batt_both_en_s <= 0;
	
		pwr_out_1_s <= 0;
		pwr_out_2_s <= 0;
		pwr_out_3_s <= 0;
		pwr_out_4_s <= 0;
		pwr_out_5_s <= 0;
		pwr_out_6_s <= 0;
		pwr_out_7_s <= 0;
		pwr_out_8_s <= 0;
		pwr_out_9_s <= 0;
	end else begin
		BATT_1_EN_s <= MCU_IN_BATT_1_EN;
		BATT_2_EN_s <= MCU_IN_BATT_2_EN;
		batt_both_en_s <= MCU_IN_BATT_BOTH_EN;
		
		pwr_out_1_s <= MCU_IN_EN_1;
		pwr_out_2_s <= MCU_IN_EN_2;
		pwr_out_3_s <= MCU_IN_EN_3;
		pwr_out_4_s <= MCU_IN_EN_4;
		pwr_out_5_s <= MCU_IN_EN_5;
		pwr_out_6_s <= MCU_IN_EN_6;
		pwr_out_7_s <= MCU_IN_EN_7;
		pwr_out_8_s <= MCU_IN_EN_8;
		pwr_out_9_s <= MCU_IN_EN_9;
	end
end

endmodule
