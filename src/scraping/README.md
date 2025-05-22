# Script Usage Examples

## Basic Usage
```bash
# Récupérer les données de la ligue par défaut
python -m main
```

## Specific League
```bash
# Récupérer les données d'une ligue spécifique
python -m main --league premier_league
```

## Multiple Leagues
```bash
# Récupérer les données de toutes les ligues configurées
python -m main --all
```

## Historical Data
```bash
# Récupérer les données historiques (si activé dans la config)
python -m main --historical
```

## Custom URL
```bash
# Utiliser une URL personnalisée
python -m main --url "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
```

## Testing (No Save)
```bash
# Ne pas sauvegarder les données (juste les récupérer)
python -m main --all --no-save
```