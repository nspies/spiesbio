import box
import requests

class Gene(box.Box):
    def __repr__(self):
        return repr(self.to_dict())
    def __str__(self):
        import json
        temp = json.dumps(self.to_dict(),sort_keys=True, indent=4)
        return str(temp)
    def _repr_pretty_(self, p, cycle):
        if cycle:
            p.text("Gene()")
        p.text(str(self))

def get_coordinates(gene_symbol, canonical=True, box=True): 
    server = "https://rest.ensembl.org"
    ext = f"/lookup/symbol/homo_sapiens/{gene_symbol}?expand=1"
    
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
    
    if not r.ok:
        r.raise_for_status()
    
    decoded = r.json()

    if canonical:
        selected_tx = [tx for tx in decoded["Transcript"] if tx["is_canonical"]]
        if len(selected_tx):
            decoded["Transcript"] = selected_tx[0]
        else:
            raise Exception(f"No canonical transcript found for {gene_symbol}")
    
    if box:
        import box
        decoded = Gene(decoded)

    return decoded
    