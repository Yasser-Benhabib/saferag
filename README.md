# SafeRAG
Détecteur d'injections de prompt dans les documents d'un RAG.

## Résultats

| Version | Exemples | Rappel | Précision |
|---|---|---|---|
| Regex « ignore previous » (référence) | 40 | 0.25 | 0.86 |
| + changement de rôle | 44 | 0.33 | 0.89 |
| Référence avant faux messages système | 50 | 0.33 | 0.82 |
| + faux messages système | 50 | 0.44 | 0.86 |