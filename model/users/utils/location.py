import requests

class Location:
    def __init__(self, cep):
        self.cep = cep
        self.data = None
    
    def fetch_data(self):
        # Format the CEP (remove any non-numeric characters)
        formatted_cep = self.cep.replace("-", "").strip()
        
        # Query the ViaCEP API
        url = f"https://viacep.com.br/ws/{formatted_cep}/json/"
        response = requests.get(url)
        
        if response.status_code == 200:
            self.data = response.json()
            if "error" in self.data:
                raise ValueError("CEP not found")
        else:
            raise Exception("Error in API request")
    
    def get_address(self):
        if not self.data:
            return "Information not available."
        
        # Return formatted address information
        return {
            "cep": self.data.get("cep"),
            "logradouro": self.data.get("logradouro"),
            "bairro": self.data.get("bairro"),
            "cidade": self.data.get("localidade"),
            "estado": self.data.get("uf")
        }