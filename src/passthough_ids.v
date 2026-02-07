///////////////////////////////////////////////////////////////////////////////
// vim:set shiftwidth=3 softtabstop=3 expandtab:
// $Id: passthough_ids.v 2026-2-7
///////////////////////////////////////////////////////////////////////////////
`timescale 1ns/1ps

module ids
   #(
      parameter DATA_WIDTH = 64,
      parameter CTRL_WIDTH = DATA_WIDTH/8,
      parameter UDP_REG_SRC_WIDTH = 2
   )
   (
      input  [DATA_WIDTH-1:0]             in_data,
      input  [CTRL_WIDTH-1:0]             in_ctrl,
      input                               in_wr,
      output                              in_rdy,

      output [DATA_WIDTH-1:0]             out_data,
      output [CTRL_WIDTH-1:0]             out_ctrl,
      output                              out_wr,
      input                               out_rdy,

      // --- Register interface
      input                               reg_req_in,
      input                               reg_ack_in,
      input                               reg_rd_wr_L_in,
      input  [`UDP_REG_ADDR_WIDTH-1:0]    reg_addr_in,
      input  [`CPCI_NF2_DATA_WIDTH-1:0]   reg_data_in,
      input  [UDP_REG_SRC_WIDTH-1:0]      reg_src_in,

      output                              reg_req_out,
      output                              reg_ack_out,
      output                              reg_rd_wr_L_out,
      output  [`UDP_REG_ADDR_WIDTH-1:0]   reg_addr_out,
      output  [`CPCI_NF2_DATA_WIDTH-1:0]  reg_data_out,
      output  [UDP_REG_SRC_WIDTH-1:0]     reg_src_out,

      // misc
      input                               reset,
      input                               clk
   );

   //------------------------- Signals -------------------------------

   wire [DATA_WIDTH-1:0]  in_fifo_data;
   wire [CTRL_WIDTH-1:0]  in_fifo_ctrl;
   wire                   in_fifo_nearly_full;
   wire                   in_fifo_empty;

   wire                   in_fifo_rd_en;

   // software registers 
   wire [31:0]            pattern_high;
   wire [31:0]            pattern_low;
   wire [31:0]            ids_cmd;

   // hardware register
   reg  [31:0]            matches;

   //------------------------- Local assignments -------------------------------

   assign in_rdy = !in_fifo_nearly_full;
   assign out_data      = in_fifo_data;
   assign out_ctrl      = in_fifo_ctrl;
   assign out_wr        = !in_fifo_empty;
   assign in_fifo_rd_en = (!in_fifo_empty) && out_rdy;

   //------------------------- Modules -------------------------------

   fallthrough_small_fifo #(
      .WIDTH(CTRL_WIDTH+DATA_WIDTH),
      .MAX_DEPTH_BITS(2)
   ) input_fifo (
      .din           ({in_ctrl, in_data}),   // Data in
      .wr_en         (in_wr),                // Write enable
      .rd_en         (in_fifo_rd_en),        // Read the next word 
      .dout          ({in_fifo_ctrl, in_fifo_data}),
      .full          (),
      .nearly_full   (in_fifo_nearly_full),
      .empty         (in_fifo_empty),
      .reset         (reset),
      .clk           (clk)
   );
   generic_regs
   #(
      .UDP_REG_SRC_WIDTH   (UDP_REG_SRC_WIDTH),
      .TAG                 (`IDS_BLOCK_ADDR),          // Tag -- eg. MODULE_TAG
      .REG_ADDR_WIDTH      (`IDS_REG_ADDR_WIDTH),     // Width of block addresses -- eg. MODULE_REG_ADDR_WIDTH
      .NUM_COUNTERS        (0),                 // Number of counters
      .NUM_SOFTWARE_REGS   (3),                 // Number of sw regs
      .NUM_HARDWARE_REGS   (1)                  // Number of hw regs
   ) module_regs (
      .reg_req_in       (reg_req_in),
      .reg_ack_in       (reg_ack_in),
      .reg_rd_wr_L_in   (reg_rd_wr_L_in),
      .reg_addr_in      (reg_addr_in),
      .reg_data_in      (reg_data_in),
      .reg_src_in       (reg_src_in),

      .reg_req_out      (reg_req_out),
      .reg_ack_out      (reg_ack_out),
      .reg_rd_wr_L_out  (reg_rd_wr_L_out),
      .reg_addr_out     (reg_addr_out),
      .reg_data_out     (reg_data_out),
      .reg_src_out      (reg_src_out),

      // --- counters interface
      .counter_updates  (),
      .counter_decrement(),

      // --- SW regs interface
      .software_regs    ({ids_cmd, pattern_low, pattern_high}),

      // --- HW regs interface
      .hardware_regs    (matches),

      .clk              (clk),
      .reset            (reset)
   );

   //------------------------- Logic -------------------------------
   always @(posedge clk) begin
      if (reset) begin
         matches <= 32'd0;
      end
      else if (ids_cmd[0]) begin
         matches <= 32'd0;
      end
      else begin
         matches <= matches; 
      end
   end

endmodule
