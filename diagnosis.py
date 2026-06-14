class Diagnosis:
      def __init__(self,session_id,patient_id,doctor_id,symptoms,disease,prevention,medication):
      self.session_id=session_id
      self.patient_id=patient_id
      self.doctor_id=doctor_id

      #tHIS WILL DO THE INPUTS
      self.symptoms=""
      self.disease=""
      self.prevention=""
      self.medication=""
      
      #This is where when the doctor inputs symptoms to triggr the search
      def enter_symptoms(self,storage_engine):
        symptom=input("Enter symptom to search: ")
        self.symptoms = symptom # This saves the string into your class attribute!
        matches=storage_engine.search_diseases_by_symptom(self.symptoms)
        print("\nMatching Diseases Found")
        if not matches:
            print("[!] No matching diseases found for that symptom.Please try again")
            return False

        for index, disease in enumerate(matches, start=1):
            print(f"{index}. {disease['name']}")
        try:
            choice = int(input("\nSelect the matching disease number: "))
            if choice 1<=choice<=len(matches):
                self.disease= selected_disease["name"]
                self.prevention=selected_disease["prevention"]
                self.medication= selected_disease["medication"]
                selected_disease=matches[choice -1]
                print(f"[tick]Diagnosis confirm: {self.disease}")
                return True
            else:
                print(F"[!]Invalid selection number.")
                return False
        except ValueError:
            print("[!] Invalid Please eneter a valid number.")
            return False                

      # To show what has been tracked  
      def display_symptoms(self):
        """Display a summary of the current session details"""
        print("\n"+"="*40)
        print(f"DIAGNOSIS SUMMARY (Session: {self.session_id})")
        print(f""="*40) 
        print(f"Patient ID: {self.patient_id}") 
        print(f"Doctor ID: {self.doctor_id}") 
        print(f"Symptom: {self.symptoms}") 
        print(f"Condition: {self.disease}") 
        print(f"Prevention: {self.prevention}") 
        print(f"Medication: {self.medication}")        
      
      # To format everything cleanly into a dictionary and sen it to the StorageEngine.save_diagnosis()  
      def save_diagnosis(self, storage_engine):
        """Bundles the session details into a dict and pushes to storage.py""""
        if not self.disease:
            print("[!] Cannot save an incomplete diagnosis session.")
            return False
        diagnosis_data={
            "session_id": self.session_id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "symptoms": self.symptoms,
            "disease": self.disease,
            "prevention": self.prevention,
            "medication": self.medication
        }    
        return storage_engine.save_diagnosis(diagnosis_data)