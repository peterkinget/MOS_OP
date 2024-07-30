*
* Subckt wrappers around for the transistors on the Mobius chip
*
* a unit nMOS device has W/L of 16 or 2 x 4u/0.5u fingers
* a unit pMOS device has W/L of 48 or 6 x 4u/0.5u fingers
*

.subckt NMOS_mobius D G S B M='M'
.param W=4u L=0.5u LDIF=0.5u AD = {W*LDIF} AS = AD PS = {W+LDIF} PD = PS
MN D G S B cmosn W=W L=L AD=AD AS=AD PD=PD PS=PS M={2*M}
.ends

.subckt PMOS_mobius D G S B M='M'
.param W=4u L=0.5u LDIF=0.5u AD = {W*LDIF} AS = AD PS = {W+LDIF} PD = PS
MP D G S B cmosp W=W L=L AD=AD AS=AD PD=PD PS=PS M={6*M}
.ends

.inc ./tsmc025_public.inc