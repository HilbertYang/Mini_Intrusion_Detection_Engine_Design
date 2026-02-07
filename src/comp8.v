////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 1995-2008 Xilinx, Inc.  All rights reserved.
////////////////////////////////////////////////////////////////////////////////
//   ____  ____ 
//  /   /\/   / 
// /___/  \  /    Vendor: Xilinx 
// \   \   \/     Version : 10.1
//  \   \         Application : sch2verilog
//  /   /         Filename : comp8.vf
// /___/   /\     Timestamp : 01/28/2026 11:24:01
// \   \  /  \ 
//  \___\/\___\ 
//
//Command: C:\Xilinx\10.1\ISE\bin\nt\unwrapped\sch2verilog.exe -intstyle ise -family virtex2p -w C:/lab3/ise/comp8.sch comp8.vf
//Design Name: comp8
//Device: virtex2p
//Purpose:
//    This verilog netlist is translated from an ECS schematic.It can be 
//    synthesized and simulated, but it should not be modified. 
//
`timescale 1ns / 1ps

module comp8(A, 
             B, 
             EQ);

    input [7:0] A;
    input [7:0] B;
   output EQ;
   
   wire AB0;
   wire AB1;
   wire AB2;
   wire AB3;
   wire AB4;
   wire AB5;
   wire AB6;
   wire AB7;
   wire AB03;
   wire AB47;
   
   XNOR2 XLXI_2 (.I0(B[0]), 
                 .I1(A[0]), 
                 .O(AB0));
   XNOR2 XLXI_3 (.I0(B[1]), 
                 .I1(A[1]), 
                 .O(AB1));
   XNOR2 XLXI_4 (.I0(B[2]), 
                 .I1(A[2]), 
                 .O(AB2));
   XNOR2 XLXI_5 (.I0(B[3]), 
                 .I1(A[3]), 
                 .O(AB3));
   XNOR2 XLXI_6 (.I0(B[4]), 
                 .I1(A[4]), 
                 .O(AB4));
   XNOR2 XLXI_7 (.I0(B[6]), 
                 .I1(A[6]), 
                 .O(AB6));
   XNOR2 XLXI_8 (.I0(B[7]), 
                 .I1(A[7]), 
                 .O(AB7));
   XNOR2 XLXI_9 (.I0(B[5]), 
                 .I1(A[5]), 
                 .O(AB5));
   AND4 XLXI_10 (.I0(AB3), 
                 .I1(AB2), 
                 .I2(AB1), 
                 .I3(AB0), 
                 .O(AB03));
   AND4 XLXI_11 (.I0(AB7), 
                 .I1(AB6), 
                 .I2(AB5), 
                 .I3(AB4), 
                 .O(AB47));
   AND2 XLXI_12 (.I0(AB47), 
                 .I1(AB03), 
                 .O(EQ));
endmodule
