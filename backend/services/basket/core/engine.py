from typing import Dict, Any, List
import json
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate('firebase-adminsdk.json')
    firebase_admin.initialize_app(cred, options={'projectId': 'nourient-38381'})

# Daily Recommended Limits (Generic adult)
LIMITS = {
    "sugar": 50,    # grams (added sugar)
    "sodium": 2300, # mg
    "calories": 2000
}

class BasketEngine:
    def __init__(self):
        self.db = firestore.client()
        self.collection_name = 'user_baskets'

    def add_to_basket(self, user_id: str, product: Dict[str, Any]) -> None:
        doc_ref = self.db.collection(self.collection_name).document(user_id)
        # We append to an array of items in the user's basket document
        doc_ref.set({
            'items': firestore.firestore.ArrayUnion([{
                "added_at": datetime.utcnow().isoformat(),
                "product_data": product
            }])
        }, merge=True)

    def clear_basket(self, user_id: str) -> None:
        doc_ref = self.db.collection(self.collection_name).document(user_id)
        doc_ref.delete()

    def remove_item(self, user_id: str, index: int) -> None:
        doc_ref = self.db.collection(self.collection_name).document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            items = data.get('items', [])
            items.sort(key=lambda x: x.get('added_at', ''), reverse=True)
            if 0 <= index < len(items):
                del items[index]
                doc_ref.set({'items': items})

    def get_basket(self, user_id: str) -> List[Dict[str, Any]]:
        doc_ref = self.db.collection(self.collection_name).document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            items = data.get('items', [])
            # Sort by added_at descending
            items.sort(key=lambda x: x.get('added_at', ''), reverse=True)
            return [item['product_data'] for item in items]
        return []

    def analyze_basket(self, user_id: str) -> Dict[str, Any]:
        items = self.get_basket(user_id)
        
        totals = {
            "sugar": 0.0,
            "sodium": 0.0,
            "protein": 0.0,
            "calories": 0.0
        }
        
        for item in items:
            nutrition = item.get("nutrition", {})
            totals["sugar"] += float(nutrition.get("sugar", {}).get("amount", 0) or 0)
            totals["sodium"] += float(nutrition.get("sodium", {}).get("amount", 0) or 0)
            totals["protein"] += float(nutrition.get("protein", {}).get("amount", 0) or 0)
            totals["calories"] += float(nutrition.get("calories", {}).get("amount", 0) or 0)

        warnings = []
        if totals["sugar"] > LIMITS["sugar"]:
            warnings.append(f"WARNING: Your basket contains {totals['sugar']}g of sugar, exceeding the daily limit of {LIMITS['sugar']}g.")
        if totals["sodium"] > LIMITS["sodium"]:
            warnings.append(f"WARNING: Your basket contains {totals['sodium']}mg of sodium, exceeding the daily limit of {LIMITS['sodium']}mg.")

        return {
            "item_count": len(items),
            "totals": totals,
            "warnings": warnings,
            "items": items
        }
