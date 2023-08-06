import requests

def get_agremeents(receivingInstitutionId, sendingInstitutionId, academicYearId, categoryCode):
    url = "https://assist.org/api/agreements"
    params = {
        "receivingInstitutionId": receivingInstitutionId,
        "sendingInstitutionId": sendingInstitutionId,
        "academicYearId": academicYearId,
        "categoryCode": categoryCode
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response
    else:
        return None

def get_agreements_categories(receivingInstitutionId, sendingInstitutionId, academicYearId):
    url = "https://assist.org/api/agreements/categories"
    params = {
        "receivingInstitutionId": receivingInstitutionId,
        "sendingInstitutionId": sendingInstitutionId,
        "academicYearId": academicYearId
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.text
    else:
        return None
