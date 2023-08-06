import requests

def get_transferability_courses(institutionId, academicYearId, listType):
    url = "https://assist.org/api/transferability/courses"
    params = {
        "institutionId": institutionId,
        "academicYearId": academicYearId,
        "listType": listType
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.text
    else:
        return None

def get_transferability_categories(institutionId, academicYearId, listType):
    url = "https://assist.org/api/transferability/categories"
    params = {
        "institutionId": institutionId,
        "academicYearId": academicYearId,
        "listType": listType
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.text
    else:
        return None
