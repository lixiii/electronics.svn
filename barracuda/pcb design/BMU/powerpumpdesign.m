

function answer = InductorCharge(t,ton,toff,V1, V2, Vf, rds, rpcb,L)
	if(t <= ton)
		answer = (V2 / rds) * (1 - exp(-t * (rds / L)));
	elseif (t <= toff)
		ipeak = (V2/ rds) * (1 - exp(-ton * (rds / L)));
		answer = (ipeak + (V1+ Vf)/rpcb)*(exp((ton-t)*rpcb/L) - (V1+Vf)/rpcb);
	endif
		answer = 0;
endfunction
		

