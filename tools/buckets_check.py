import json, subprocess
R="/Users/rkievit/Projects/rr_lvvn_subsidies"
law=open(f"{R}/app/public/lvv.yaml").read().replace("accepted: false","accepted: true")
vf=json.load(open(f"{R}/app/public/vragenflow.json"))
GATES=[g for g in ["1","3","4","5","6","8","9","Bijlage I"] if g in vf["artikelen"]]

def basis(target, mode, override=None):
    params={}
    order=[n for n in vf["artikelen"] if n not in GATES and n!=target]+GATES+([target] if target in vf["artikelen"] else [])
    for n in order:
        for p,spec in vf["artikelen"][n]["params"].items():
            if spec["ambigu"]: params[p]=spec["neutraal"]
            else: params[p]=spec["gunstig" if mode=="opt" else "ongunstig"]
    if override: params.update(override)
    return {k:v for k,v in params.items() if v is not None}

def evalueer(ep, params):
    payload={"law_yaml":law,"output_name":ep,"params":params,"date":"2024-06-01","extra_laws":[]}
    r=subprocess.run(["/Users/rkievit/Projects/regelrecht/packages/target/release/evaluate"],input=json.dumps(payload),capture_output=True,text=True)
    out=json.loads(r.stdout)
    return out.get("outputs",{}).get(ep), (out.get("error") or "")[:60] or None

def optimistisch(target, answers):
    """basisrun + kandidaat-retries voor conflict-params in de keten"""
    ep=vf["artikelen"][target]["endpoint"]
    p0=basis(target,"opt"); p0.update(answers)
    got,err=evalueer(ep,p0)
    if got is True: return True,err
    keten=GATES+[target]
    for n in keten:
        for p,spec in vf["artikelen"][n]["params"].items():
            if p in answers or spec["ambigu"]: continue
            for kand in spec.get("gunstig_kandidaten",[])[1:]:
                p1=dict(p0); p1[p]=kand
                got,err=evalueer(ep,p1)
                if got is True: return True,err
    return False,err

if __name__=="__main__":
    print("1) art15 optimistisch, geen antwoorden:", optimistisch("15",{}))
    ans={"is_onderneming_in_moeilijkheden":True}
    print("2) moeilijkheden: art15", optimistisch("15",ans), "| art14", optimistisch("14",ans))
    stal=json.load(open(f"{R}/docs/verrijking/golden_route_3.json"))["params"]
    ep14=vf["artikelen"]["14"]["endpoint"]
    print("3) art14 pessimistisch + stal-casus:", evalueer(ep14, basis("14","pess",stal)))
    levend=[]; dood=[]
    for n in vf["artikelen"]:
        if n in GATES: continue
        ok,_=optimistisch(n,{})
        (levend if ok else dood).append(n)
    print(f"4) levend zonder antwoorden: {len(levend)}; dood: {dood}")
