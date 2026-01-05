from app.ai.gemini_service import GeminiService

# Singleton instance for backward compatibility
_ai_service = GeminiService()

def analyze_xray(image_data):
    """
    Analyse une image radiographique dentaire via Gemini Pro Vision.
    Utilise le nouveau service GeminiService.
    """
    return _ai_service.analyze_xray(image_data)