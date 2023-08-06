from alignn.ff.ff import default_path,ForceField,get_interface_energy
from jarvis.db.figshare import data
from jarvis.core.atoms import Atoms
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from jarvis.analysis.structure.neighbors import NeighborsAnalysis
from matplotlib.gridspec import GridSpec
from sklearn.metrics import r2_score
from ase.io.trajectory import Trajectory
from alignn.ff.ff import AlignnAtomwiseCalculator,ase_to_atoms
from alignn.ff.ff import (
    default_path,
    ev_curve,
    surface_energy,
    vacancy_formation,
    ForceField,
    get_interface_energy,
)
def get_atoms(jid=""):
    dft_2d = data("dft_2d")
    for i in dft_2d:
        if i["jid"] == jid:
            atoms = Atoms.from_dict(i["atoms"])
            return atoms
    dft_3d = data("dft_3d")
    for i in dft_3d:
        if i["jid"] == jid:
            atoms = Atoms.from_dict(i["atoms"])
            return atoms

model_path=default_path()
jid_film='JVASP-867'
jid_subs='JVASP-14741'
#jid_film='JVASP-816'
#jid_subs='JVASP-32'
miller_film=[1,1,1]
miller_subs=[1,1,1]
film_atoms = get_atoms(jid_film)
subs_atoms = get_atoms(jid_subs)
intf_dat = get_interface_energy(
    film_atoms=film_atoms,
    subs_atoms=subs_atoms,
    film_index=miller_film,
    subs_index=miller_subs,
    seperation=4.5,
    model_path=model_path
)
Wad = intf_dat['interface_energy']
print(Wad)
opt_intf=Atoms.from_dict(intf_dat['optimized_interface'])
timestep=0.1
steps=100
temperature_K=300
initial_temperature_K=10
model_path=default_path()
ff = ForceField(
    jarvis_atoms=opt_intf,
    model_path=model_path,
    timestep=timestep,
)
lang = ff.run_nvt_berendsen(
    steps=steps,
    filename='cutin',
    temperature_K=temperature_K,
    initial_temperature_K=initial_temperature_K,
)
print("final struct:")
print(lang)

traj =  Trajectory('cutin.traj')
f=open('alignn_ff.log','r')
lines=f.read().splitlines()
f.close()
temps=[]
pes=[]
kes=[]
tes=[]
for i in lines:
    if 'Etot' not in i:
        tmp=i.split()
        #print (tmp)
        temps.append(float(tmp[-1]))
        pes.append(float(tmp[1]))
        kes.append(float(tmp[2]))
        tes.append(float(tmp[0]))
the_grid = GridSpec(1,2)
plt.rcParams.update({'font.size': 18})
plt.figure(figsize=(12,5))
plt.subplot(the_grid[0])
timestep=0.1

tim=np.arange(len(temps))*timestep
plt.plot(tim,temps,'.')
plt.title('(d)')
plt.ylabel('Temperature (K)')
plt.xlabel('Time(fs)')

plt.savefig('md.png')
plt.close()

# plt.subplot(the_grid[1])


# #plt.plot(tim,tes)
# # plt.title('(c)')
# nb = NeighborsAnalysis(ase_to_atoms(traj[0]),max_cut=5)
# bins_rdf, rdf, nbs = nb.get_rdf()
# plt.plot(bins_rdf, rdf,label='Intial')
# nb = NeighborsAnalysis(ase_to_atoms(traj[-1]),max_cut=5)
# bins_rdf, rdf, nbs = nb.get_rdf()
# plt.plot(bins_rdf, rdf,label='Final')
# plt.xlabel(r'Distance bins ($\AA$)')
# plt.legend()
# plt.ylabel('RDF')
