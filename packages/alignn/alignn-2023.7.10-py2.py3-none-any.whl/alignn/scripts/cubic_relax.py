import pandas as pd
from jarvis.db.figshare import data
from jarvis.core.atoms import Atoms
from jarvis.core.composition import Composition
from jarvis.db.jsonutils import dumpjson
import json

dat3d = pd.DataFrame(data("dft_3d"))


def get_atoms(formula=""):
    df = dat3d[dat3d["formula"] == formula]
    df1 = df[
        [
            "jid",
            "spg_number",
            "atoms",
            "spg_symbol",
            "formula",
            "crys",
            "formation_energy_peratom",
            "ehull",
        ]
    ]
    df1 = df1[df1["crys"] == "cubic"]
    x = Atoms.from_dict(
        df1.iloc[df1["formation_energy_peratom"].argmin()]["atoms"]
    ).get_conventional_atoms  # df1[df1['ehull']==0]
    jid = df1.iloc[df1["formation_energy_peratom"].argmin()][
        "jid"
    ]  # df1[df1['ehull']==0]
    return x, jid


data = pd.read_html("http://en.wikipedia.org/wiki/Lattice_constant")[0]
data = data[
    ~data["Crystal structure"].isin(
        [
            "Hexagonal",
            "Wurtzite",
            "Wurtzite (HCP)",
            "Orthorhombic",
            "Tetragonal perovskite",
            "Orthorhombic perovskite",
        ]
    )
]
data.rename(columns={"Lattice constant (Å)": "a (Å)"}, inplace=True)

data["a (Å)"] = data["a (Å)"].map(float)
print(data[0:60])
f=open('ES-SinglePropertyPrediction-cubic_lattice_param_a-dft_3d-test-mae.csv','w')
f.write('id,target,prediction,formula\n')
mem={}
mem['train']={}
tmp={}
for i, ii in data.iterrows():
    try:
        formula = (
            Composition.from_string(ii["Material"].split("(")[0])
        ).reduced_formula
        atoms, jid = get_atoms(formula)
        print(formula, jid, ii["a (Å)"], atoms.lattice.abc[0])
        tmp[jid]=float(ii["a (Å)"])
        
        line=jid+','+str(ii["a (Å)"])+','+str(atoms.lattice.abc[0])+','+str(formula)+'\n'
        f.write(line)
    except:
        pass
f.close()
mem['test']=tmp
f=open('dft_3d_cubic_lattice_param_a.json','w')
f.write(json.dumps(mem,indent=4))
f.close()
