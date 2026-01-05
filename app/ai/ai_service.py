from abc import ABC, abstractmethod

class AIAnalysisService(ABC):
    @abstractmethod
    def analyze_xray(self, image_data: bytes) -> dict:
        """
        Analyze dental X-ray image and return structured results.
        
        Args:
            image_data (bytes): Raw image data
            
        Returns:
            dict: Structured analysis results with keys:
                  - summary (str)
                  - cavity_detected (bool)
                  - bone_loss_detected (bool)
                  - urgent_attention_needed (bool)
                  - error (str, optional)
        """
        pass
