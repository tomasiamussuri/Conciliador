import pandas as pd
from typing import List, Dict, Tuple

class ReconciliationEngine:
    def __init__(self):
        self.matched_blue_ids = set()
        self.matched_gama_ids = set()

    def reset_matches(self):
        """Reset matched IDs sets"""
        self.matched_blue_ids.clear()
        self.matched_gama_ids.clear()

    def apply_matching_rules(
        self, 
        base_blue: pd.DataFrame, 
        base_gama: pd.DataFrame, 
        rules: List[Dict]
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Apply matching rules in priority order"""
        self.reset_matches()
        base_blue_copy = base_blue.copy()
        base_gama_copy = base_gama.copy()

        for rule in rules:
            blue_cols = rule['blue_columns']
            gama_cols = rule['gama_columns']
            rule_name = rule['name']
            
            blue_key = base_blue_copy[blue_cols].apply(lambda x: '|'.join(x), axis=1)
            gama_key = base_gama_copy[gama_cols].apply(lambda x: '|'.join(x), axis=1)
            
            blue_unmatched = ~base_blue_copy['ID_BLUE'].isin(self.matched_blue_ids)
            gama_unmatched = ~base_gama_copy['ID_GAMA'].isin(self.matched_gama_ids)
            
            for blue_idx in blue_key[blue_unmatched].index:
                if blue_key[blue_idx] in gama_key[gama_unmatched].values:
                    gama_idx = gama_key[gama_unmatched][gama_key[gama_unmatched] == blue_key[blue_idx]].index[0]
                    
                    blue_id = base_blue_copy.loc[blue_idx, 'ID_BLUE']
                    gama_id = base_gama_copy.loc[gama_idx, 'ID_GAMA']
                    
                    base_blue_copy.loc[blue_idx, 'MATCHED_ID'] = gama_id
                    base_blue_copy.loc[blue_idx, 'MATCH_RULE'] = rule_name
                    base_gama_copy.loc[gama_idx, 'MATCHED_ID'] = blue_id
                    base_gama_copy.loc[gama_idx, 'MATCH_RULE'] = rule_name
                    
                    self.matched_blue_ids.add(blue_id)
                    self.matched_gama_ids.add(gama_id)

        return self._prepare_results(base_blue_copy, base_gama_copy)

    def _prepare_results(
        self, 
        base_blue: pd.DataFrame, 
        base_gama: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Prepare final results dataframes"""
        only_blue = base_blue[~base_blue['ID_BLUE'].isin(self.matched_blue_ids)]
        only_gama = base_gama[~base_gama['ID_GAMA'].isin(self.matched_gama_ids)]
        
        matches_blue = base_blue[base_blue['ID_BLUE'].isin(self.matched_blue_ids)]
        matches_gama = base_gama[base_gama['ID_GAMA'].isin(self.matched_gama_ids)]
        
        matches = pd.merge(
            matches_blue,
            matches_gama,
            left_on='MATCHED_ID',
            right_on='ID_GAMA',
            suffixes=('_BLUE', '_GAMA')
        )

        return matches, only_blue, only_gama
