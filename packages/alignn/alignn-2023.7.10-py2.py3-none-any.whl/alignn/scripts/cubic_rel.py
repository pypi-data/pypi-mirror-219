from jarvis.core.atoms import Atoms
import pandas as pd
# from jarvis.core.graphs import Graph
from alignn.ff.ff import (
    default_path,
    ev_curve,
    surface_energy,
    vacancy_formation,
    ForceField,
    fd_path,
    get_interface_energy,
)

from jarvis.db.figshare import data
dft_3d=pd.DataFrame(data('dft_3d'))
model_path = "/wrk/knc6/ALINN_FC/FD_mult/temp_new"
model_path=fd_path() #default_path()
model_path=default_path()
def relax(csv_path='ES-SinglePropertyPrediction-cubic_lattice_param_a-dft_3d-test-mae.csv',model_path=[]):
    df=pd.read_csv(csv_path)
    for i,ii in df.iterrows():
        jid=ii['id']
        filt=(dft_3d[dft_3d['jid']==jid])['atoms'].values[0]
        print(ii)
        atoms=Atoms.from_dict(filt)  
        atoms_cvn = atoms.get_conventional_atoms
        print('atoms_cvn',atoms_cvn)
        new_atoms=Atoms(lattice_mat=[[5,0,0],[0,5,0],[0,0,5]],elements=atoms_cvn.elements,coords=atoms_cvn.cart_coords,cartesian=True)
      
        ff = ForceField(
            jarvis_atoms=new_atoms,
            model_path=model_path,
            stress_wt=0.1,
            #stress_wt=480,
            force_multiplier=1,
            #force_multiplier=25,
            force_mult_natoms=False,
        )
        opt, en, fs = ff.optimize_atoms()#logfile=None)

relax(model_path=model_path) 
