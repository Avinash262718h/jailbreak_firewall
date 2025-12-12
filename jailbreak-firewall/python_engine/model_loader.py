import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityEngine:
    def __init__(self):
        logger.info("⏳ Loading AI Model (all-MiniLM-L6-v2)...")
        # 'all-MiniLM-L6-v2' is fast (lightweight) and accurate for semantic similarity
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Thresholds (Tweak these based on testing)
        self.jailbreak_threshold = 0.70
        self.harm_threshold = 0.70
        
        # Load Databases
        self.jailbreak_db = self._load_dataset('datasets/jailbreak_patterns.csv')
        self.harmful_db = self._load_dataset('datasets/restricted_topics.csv')
        
        logger.info("✅ Engine Initialization Complete.")

    def _load_dataset(self, filepath):
        """Loads CSV and pre-computes embeddings for speed."""
        try:
            df = pd.read_csv(filepath)
            # Ensure the CSV has a 'text' column and 'category' column
            if 'text' not in df.columns or 'category' not in df.columns:
                logger.warning(f"⚠️ {filepath} missing 'text' or 'category' columns.")
                return None
            
            logger.info(f"📊 Encoding {len(df)} patterns from {filepath}...")
            # Convert all text patterns to Vectors (Embeddings) immediately
            embeddings = self.model.encode(df['text'].tolist(), convert_to_tensor=True)
            return {'df': df, 'embeddings': embeddings}
        except Exception as e:
            logger.error(f"❌ Failed to load {filepath}: {e}")
            return None

    def get_best_match(self, prompt_embedding, db_data):
        """Finds the most similar pattern in the database."""
        if not db_data:
            return 0.0, "Unknown"
        
        # Calculate Cosine Similarity between Prompt and ALL Database patterns
        # This is extremely fast using PyTorch
        cosine_scores = util.cos_sim(prompt_embedding, db_data['embeddings'])[0]
        
        # Find the highest score
        best_score_tensor = torch.max(cosine_scores)
        best_score = float(best_score_tensor.item())
        
        # Find the category of the best match
        best_idx = torch.argmax(cosine_scores).item()
        category = db_data['df'].iloc[best_idx]['category']
        
        return best_score, category

    def analyze(self, prompt):
        """Main Logic: Dual Mechanism Analysis."""
        
        # 1. Convert User Prompt to Vector
        prompt_embedding = self.model.encode(prompt, convert_to_tensor=True)
        
        # 2. Mechanism A: Jailbreak Analysis (Style/Intent)
        jb_score, jb_category = self.get_best_match(prompt_embedding, self.jailbreak_db)
        
        # 3. Mechanism B: Harmfulness Analysis (Topic/Content)
        harm_score, harm_category = self.get_best_match(prompt_embedding, self.harmful_db)
        
        # 4. Final Verdict Logic
        verdict = "SAFE"
        recommendation = "Prompt appears safe to process."
        
        # Logic: If Harm is high OR Jailbreak is high -> BLOCK
        if harm_score > self.harm_threshold:
            verdict = "BLOCKED"
            recommendation = f"Flagged as harmful content ({harm_category}). Do not process."
        elif jb_score > self.jailbreak_threshold:
            verdict = "BLOCKED"
            recommendation = f"Potential Jailbreak attempt detected ({jb_category}). Reset conversation context."
        elif harm_score > 0.5 or jb_score > 0.5:
             # Edge case: Not high enough to block, but suspicious
             verdict = "FLAGGED"
             recommendation = "Review required. Content is borderline."

        return {
            "jailbreak_score": round(jb_score, 4),
            "jailbreak_category": jb_category if jb_score > 0.3 else "None",
            "harmfulness_score": round(harm_score, 4),
            "harmfulness_category": harm_category if harm_score > 0.3 else "None",
            "verdict": verdict,
            "recommendation": recommendation
        }