#################################
######    Initialization
#################################

log		log.GRAIN
units		metal
boundary	p p p
atom_style	atomic

#################################
######    Variables
#################################

variable	V equal vol
variable	E equal pe
variable	Pr equal press
variable	T equal temp
variable	Lx equal lx
variable	Ly equal ly
variable	Lz equal lz

variable	xHalf equal xHALF
variable	yHalf equal yHALF
variable	zHalf equal zHALF
variable	latCon1 equal LAT1
variable	latCon2 equal LAT2
variable	P equal RUN
variable	Q equal RISE
variable	MoPart equal MOLY
variable	seed equal SEED
variable	Tmp equal TEMP

#################################
######    Geometry
#################################

region		jar block -${xHalf} ${xHalf} -${yHalf} ${yHalf} -${zHalf} ${zHalf}
create_box	2 jar
region		top block INF INF -0.1 ${yHalf} INF INF
lattice		bcc ${latCon1} orient x $P 0 $Q orient y 0 1 0 orient z -$Q 0 $P
create_atoms	1 region top
region		bottom block INF INF -${yHalf} 0.1 INF INF
lattice		bcc ${latCon2} orient x 1 0 0 orient y 0 1 0 orient z 0 0 1
create_atoms	1 region bottom

pair_style	adp
pair_coeff	* * /home/hasaatmj/builds/illumine/potentials/U_Mo.alloy.adp U Mo

group		up region top
group		down region bottom
delete_atoms	overlap 2.7 up down compress yes
set		region jar type/ratio 2 ${MoPart} ${seed}

group		u type 1
group		mo type 2
variable	c1 equal count(u)
variable	c2 equal count(mo)

#################################
######    Relax npt
#################################

velocity	all create ${Tmp} ${seed}

fix		cp1 all npt temp ${Tmp} ${Tmp} 0.1 iso 0 0 0.1
fix		av1 all ave/time 1 10 25 v_T v_E v_V v_Pr &
			v_Lx v_Ly v_Lz v_c1 v_c2 file relax.GRAIN

dump		1 all atom 50 dumpRel.GRAIN

thermo_style	custom step temp pe press vol v_c1 v_c2
thermo		10
run		100

unfix		cp1

#################################
######    Relax nvt 1
#################################

variable	halfX equal f_av1[5]/2
variable	halfY equal f_av1[6]/2
variable	halfZ equal f_av1[7]/2

change_box	all x final -${halfX} ${halfX} y final -${halfY} ${halfY} &
			z final -${halfZ} ${halfZ} remap units box

fix		cv1 all nvt temp ${Tmp} ${Tmp} 0.1

run		100

#################################
######    Interstitial
#################################

#variable	Rand equal random(1,100,${seed})
#variable	PercMo equal "100 * v_MoPart"
#if		"${Rand} > ${PercMo}" then "variable inType equal 1" &
#			else "variable inType equal 2"
#
#region		stitial block EDGE EDGE -2 2 EDGE EDGE side in units box
#fix		extra all deposit 1 ${inType} 1 ${seed} &
#			region stitial near 2.0 attempt 10 units box
#
#run		100
#unfix		extra

#################################
######    Vacancy
#################################

#region		cancy block EDGE EDGE -2 2 EDGE EDGE side in units box
#fix		hole all evaporate 100 1 cancy ${seed}
#
#run		100
#unfix		hole

#################################
######    Relax nvt 2
#################################

group		u type 1
group		mo type 2

run		100

unfix		av1

#################################
######    Diffusion
#################################

undump		1
reset_timestep	0
timestep	0.002
dump		2 all atom 50 dumpRun.GRAIN

fix		cent all recenter INIT INIT INIT

compute		allMsd all msd
compute		uMsd u msd
compute		moMsd mo msd

fix		mesdi1 all ave/time 1 5 100 c_uMsd[1] c_uMsd[2] c_uMsd[3] &
			c_moMsd[1] c_moMsd[2] c_moMsd[3] &
			c_allMsd[1] c_allMsd[2] c_allMsd[3] file msdxyz.GRAIN
fix		mesdi2 all ave/time 1 5 100 v_T v_E v_V v_Pr v_c1 v_c2 &
			c_uMsd[4] c_moMsd[4] c_allMsd[4] file msd.GRAIN

thermo		10
run		500
