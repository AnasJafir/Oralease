import google.generativeai as genai
from PIL import Image
import io
import os
from .ai_service import AIAnalysisService

class GeminiService(AIAnalysisService):
    def __init__(self):
        self.api_key = os.environ.get('GOOGLE_API_KEY')
        self.model = None
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro-vision')

    def analyze_xray(self, image_data: bytes) -> dict:
        if not self.model:
            return {"error": "Service IA non configuré (Clé API manquante)"}

        try:
            image = Image.open(io.BytesIO(image_data)).convert('RGB')
            
            prompt = (
                "Analyze this dental X-ray strictly as a dental professional. "
                "Identify any signs of: 1. Cavities (Caries) 2. Bone loss 3. Infections. "
                "Format the output as a structured summary focusing on these three points. "
                "If no issues are found, state 'No obvious anomalies detected'."
            )
            
            response = self.model.generate_content([prompt, image])
            
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                return {
                    "error": "Analyse bloquée par le filtre de sécurité", 
                    "reason": str(response.prompt_feedback.block_reason)
                }

            return self._interpret_response(response.text)

        except Exception as e:
            return {"error": f"Echec de l'analyse IA: {str(e)}"}

    def _interpret_response(self, text_response: str) -> dict:
        return {
            "summary": text_response,
            "cavity_detected": "cavities" in text_response.lower() or "caries" in text_response.lower(),
            "bone_loss_detected": "bone loss" in text_response.lower(),
            "urgent_attention_needed": "infection" in text_response.lower() or "abscess" in text_response.lower()
        }
