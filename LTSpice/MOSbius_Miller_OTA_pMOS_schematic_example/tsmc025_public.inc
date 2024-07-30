* //
* // Downloaded from https://www.ee.iitm.ac.in/~nagendra/cadinfo.html on Nov. 16, 2022
* //
* // commented out rsc and rdc parameters in cmosp since it created an error
* //
* //  *****************************************************************************************
* // simulator lang=spectre insensitive=yes
* //        TSMC  0.25um 2.5v/3.3v
* //	Model Name 'cmosn'
* //            *
* //  ****************************************************************************************
*  
.model cmosn nmos ( level=49
+ version=3.1000e+00        binunit=1.0000e+00        mobmod=1
+ capmod=2                  nqsmod=0.0000e+00         
+ tox=5.6000e-09                                      toxm=4.2000e-09
+ xj=1.0000e-07             nch=2.3549e+17            rsh=3.7
+ ngate=1.0000e+23          vth0=3.735974e-01
+ k1=0.4635102              k2=4.718072e-6            k3=1e-3
+ k3b=2.0769452             w0=1.054626e-7            nlx=1.726119e-7
+ dvt0=0.4258639            dvt1=0.5888547            dvt2=-0.5
+ dvt0w=0                   dvt1w=0                   dvt2w=0
+ lint=0                    wint=0                    dwg=-1.159694e-8
+ dwb=4.405364e-9           u0=313.1284363
+ ua=-1.154825e-9           ub=2.488257e-18           uc=4.639032e-11
+ vsat=1.179169e5           a0=1.8431107              ags=0.3610511
+ b0=-1.170902e-8           b1=-1e-7                  keta=-0.0105538
+ a1=1.388205E-5            a2=0.5950094              voff=-0.1065063
+ nfactor=1.350479          cit=0                     cdsc=2.4e-4
+ cdscd=0                   cdscb=0                   eta0=5.051114e-3
+ etab=2.26013e-4           dsub=0.0309897            pclm=1.5782549
+ pdiblc1=0.9806647         pdiblc2=2.853636e-3       pdiblcb=0.0234708
+ drout=1                   pscbe1=7.006084e8         pscbe2=2.434927e-4
+ pvag=0.0203524            rdsw=200                  prwg=0.2470761
+ prwb=-0.2                 wr=1                      alpha0=0.0000e+00
+ alpha1=0.0000e+00         beta0=3.0000e+01          xpart=0.5
+ cgso=4.82e-10                     
+ cgdo=4.82e-10                                       cgbo=1e-12
+ cgsl=0.0000e+00           cgdl=0.0000e+00           ckappa=6.0000e-01
+ cf=0                      clc=1.0000e-07            cle=6.0000e-01
+ dlc=2.9000e-08            dwc=0.0000e+00            vfbcv=-1.0000e+00
+ noff=1.0000e+00           voffcv=0.0000e+00         acde=1.0000e+00
+ moin=1.5000e+01           lmin=1.8000e-07           lmax=5.0000e-05
+ wmin=2.4000e-07           wmax=1.0000e-04           
+ xl= 0                      
+ xw=-4e-8                                            js=1.0000e-06
+ jsw=7.0000e-11            cj=1.776115e-3 
+ mj=0.4693375              pb=0.99             
+ cjsw=3.648461e-10                                   mjsw=0.287856
+ tnom=2.7000e+01           ute=-1.5                  kt1=-0.11
+ kt1l=0                    kt2=0.022                 ua1=4.31e-9
+ ub1=-7.61e-18             uc1=-5.6e-11              at=3.3e4
+ prt=0                     xti=3.0000e+00            wl=0
+ wln=1                     ww=0                      wwn=1
+ wwl=0                     ll=0                      lln=1
+ lw=0                      lwn=1                     lwl=0
+ llc=-2.1400e-15           lwc=0.0000e+00            lwlc=0.0000e+00
+ wlc=0.0000e+00            wwc=0.0000e+00            wwlc=0.0000e+00
+ lvth0= - 1.0000e-03                
+ wvth0=6.027e-02                                     pvth0=-6.500944e-3
+ lnlx=-2.8540e-08          wnlx=0.0000e+00           pnlx=0.0000e+00
+ wua=-1.8800e-11           wu0=5.4000e-01
+ pub=3.8000e-20            pw0=1.3000e-09            wrdsw=0.0000e+00
+ weta0=0.0000e+00          wetab=0.0000e+00          leta0=1.5740e-03
+ letab=0.0000e+00          peta0=0.0000e+00          petab=0.0000e+00
+ wpclm=0.0000e+00          wvoff=-4.0780e-04         lvoff=-4.2080e-03
+ pvoff=-3.7880e-04         wa0=-4.7310e-02           la0=-4.6670e-01
+ pa0=-2.6490e-02           wags=4.2420e-03           lags=3.0280e-01
+ pags=0.0000e+00           wketa=8.520551e-3         lketa=1.861161e-3
+ pketa=0.0000e+00          wute=6.3730e-02           lute=0.0000e+00
+ pute=0.0000e+00           wvsat=5.0660e+03          lvsat=0.0000e+00
+ pvsat=0.0000e+00                                    lpdiblc2=-4.7520e-03
+ wat=7.0670e+03            wprt=0.0000e+00           ldif=8.0000e-08
+ hdif=2.6000e-07           n=1.0000e+00              pbsw=0.8254928
+ cjswg=3.29e-10                                      ctp=9.1400e-04
+ ptp=9.2400e-04            cta=9.1900e-04            pta=1.5800e-03
+ elm=5.0000e+00            tlevc=1.0000e+00          
+ noimod=2.0e+00	        noia=1.3182567385564e+19		noib=144543.977074592
+ noic=-1.24515784572817e-12	ef=0.92					em=41000000 )
* 
* 
*  
* //  ****************************************************************************************
* //        TSMC  0.25um 2.5v/3.3v
* //	Model Name 'cmosp'  
* //            *
* //  ****************************************************************************************
*  
.model cmosp pmos ( level=49
+ mobmod=1                  version=3.1               capmod=2
+ binunit=1.0000e+00        nqsmod=0.0000e+00         
+ tox=5.6e-9                                          toxm=4.2000e-09
+ xj=1e-7                   nch=4.1589e17             ngate=1.0000e+23
+ vth0= -0.5129563                                    k1=0.6134729
+ k2=-2.899398e-3           k3=0.0986814              k3b=9.0540104
+ w0=1e-6                   nlx=1e-9                  dvt0=2.0012281
+ dvt1=0.8322765            dvt2=-0.2148411           dvt0w=0
+ dvt1w=0                   dvt2w=0                   lint=2.87185e-8
+ wint=0                    dwg=-2.939346e-8          dwb=6.28262e-10
+ u0=105.850112                                       ua=1.149276e-9
+ ub=1.771755e-21           uc=-1e-10                 vsat=1.605184e5
+ a0=0.9295806              ags=0.17071               b0=1.118672e-6
+ b1=5e-6                   keta=0.010786             a1=0.0258091
+ a2=0.3                    voff=-0.1368868           nfactor=1.0881345
+ cit=0                     cdsc=2.4e-4               cdscd=0
+ cdscb=0                   eta0=0.5919789            etab=-0.1522258
+ dsub=1.2865437            pclm=1.2888687            pdiblc1=5.658541e-3
+ pdiblc2=3.303251e-11      pdiblcb=-1e-3             drout=0.0594889
+ pscbe1=7.527625e10        pscbe2=1.740511e-8        pvag=3.357622e-3
+ rdsw=1.392936e3           prwg=6.801752e-4          prwb=-0.1810639
+ alpha0=0.0000e+00         alpha1=0.0000e+00         beta0=3.0000e+01
+ cgdo=5.71e-10                                       cgbo=1e-12
+ cgso=5.71e-10                                       xpart=0.5
+ cf=0                      dlc=5.6000e-08            cgsl=0.0000e+00
+ cgdl=0.0000e+00           ckappa=6.0000e-01         clc=1.0000e-07
+ cle=6.0000e-01            dwc=0.0000e+00            vfbcv=-1.0000e+00
+ noff=1.0000e+00           voffcv=0.0000e+00         acde=1.0000e+00
+ moin=1.5000e+01           lmin=1.8000e-07           lmax=5.0000e-05
+ wmin=2.4000e-07           wmax=1.0000e-04           
+ xl= 0                     
+ xw=-4e-8                                            js=3.0000e-06
+ jsw=4.1200e-11            cj=1.893734e-3
+ mj=0.4705132              pb=0.9889579             
+ cjsw=3.124347e-10                                   mjsw=0.2786992
+ tnom=27                   ute=-1.5                  kt1=-0.11
+ kt1l=0                    kt2=0.022                 ua1=4.31e-9
+ ub1=-7.61e-18             uc1=-5.6e-11              at=3.3e4
+ prt=0                     xti=3.0000e+00            ww=0
+ lw=0                      ll=0                      wl=0
+ wln=1                     wwn=1                     wwl=0
+ lln=1                     lwn=1                     lwl=0
+ llc=-7.4500e-15           lwc=0.0000e+00            lwlc=0.0000e+00
+ wlc=0.0000e+00            wwc=0.0000e+00            wwlc=0.0000e+00
+ lvth0=4.4000e-03                   
+ wvth0= - 1.4800e-02                
+ pvth0=2.90746e-3                                    lnlx=-1.5840e-08
+ wrdsw=1.0070e+01          weta0=0.0000e+00          wetab=0.0000e+00
+ wpclm=0.0000e+00          wua=2.6300e-09            lua=-8.1530e-11
+ pua=5.8550e-11            wub=0.0000e+00            lub=0.0000e+00
+ pub=0.0000e+00            wuc=0.0000e+00            luc=0.0000e+00
+ puc=0.0000e+00            wvoff=-9.8160e-03         lvoff=-9.8710e-04
+ pvoff=-9.8330e-05         wa0=-4.8070e-02           la0=-2.8100e-01
+ pa0=8.6610e-02            wags=-4.1770e-02          lags=4.4540e-02
+ pags=-4.0760e-02          wketa=0.0228473           lketa=-7.555134e-3
+ pketa=0.0000e+00          wute=-2.6820e-01          lute=0.0000e+00
+ pute=0.0000e+00           wvsat=-1.4200e+04         lvsat=0.0000e+00
+ pvsat= - 4.3400e+02                                 lpdiblc2=3.0120e-03
+ cjswg=2.5e-10                                       wat=-6.4050e+03
+ wprt=2.1660e+02           n=1.0000e+00              pbsw=0.8
+ cta=1.0000e-03            ctp=7.5300e-04            pta=1.5500e-03
+ ptp=1.2400e-03            ldif=8.0000e-08           rsh=2.9
+ rd=0.0000e+00             * rsc=0.0000e+00            rdc=0.0000e+00
+ hdif=2.6000e-07           rs=0.0000e+00             
+ noimod=2.0e+00		noia=3.57456993317604e+18		noib=2500
+ noic=2.61260020285845e-11	ef=1.1388				em=41000000 )