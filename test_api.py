#run as pytest command from the folder where the file is located
from fastapi.testclient import TestClient
from api import app

client=TestClient(app)

cmpds={"Mn2CoCrP2": [6.073,163,95], "Al3Pd3Y3": [2.29082, 94.7, 30.5], "Mg1Se1": [11.922,61.7,40.3]}

def test_read_main():
    response=client.get("/")
    assert response.status_code==200
    assert response.json()=={'message': 'API для предсказания решеточной теплопроводности и упругих модулей кристаллических материалов.'}
    
def test_predict():
    for cmpd, values in cmpds.items():
        response = client.post("/predict/",
            json={"cmpd": cmpd} #"Mn2CoCrP2"
        )
        assert response.status_code==200
        json_data=response.json()
        assert values[0]*0.5<=json_data['kappa=']<=values[0]*1.5, "kappa is not correct for "+cmpd #7.63
        assert values[1]*0.7<=json_data['bulk=']<=values[1]*1.3, "bulk modulus is not correct for "+cmpd
        assert values[2]*0.5<=json_data['shear=']<=values[2]*1.5, "shear modulus is not correct for "+cmpd
