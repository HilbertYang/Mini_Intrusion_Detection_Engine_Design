module busmerge(da, db, q);
	input [47:0]da;
	input [63:0]db;
	output [111:0]q;
	assign q = {da, db};
endmodule
