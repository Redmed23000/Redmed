# Redmed

Moteur de règles TARDOC prêt à l'emploi : ingestion des sources officielles, stockage structuré, validation de combinaisons, et mécanisme de mise à jour.

## Démarrage rapide

```bash
python scripts/init_db.py
python scripts/update_rules.py --rules data/tardoc/sample_rules.json --version 2024.1
python -c "from src.rules_engine.engine import TardocRulesEngine; print(TardocRulesEngine('data/tardoc/tardoc.db').validate_combination(['A100','B200']).violations)"
```

## Ingestion des sources officielles

```bash
python scripts/ingest_tardoc.py --source /chemin/vers/tardoc_officiel.pdf --version 2024.1
```

## Structure

- `migrations/001_create_tardoc_tables.sql`: schéma SQL des tables.
- `scripts/init_db.py`: initialisation de la base SQLite.
- `scripts/update_rules.py`: chargement des règles depuis un JSON.
- `src/rules_engine/engine.py`: moteur de règles.
- `docs/`: documentation technique.

## Mise à jour des règles

1. Placer la nouvelle version officielle dans `data/tardoc/raw`.
2. Convertir au format JSON (voir `data/tardoc/sample_rules.json`).
3. Lancer `scripts/update_rules.py` avec le numéro de version.
4. Consulter `tardoc_updates` pour l'historique.

## Prototype de protocoles de soins (assistantes médicales)

Le dépôt inclut un premier lot de contenus pour une future application Windows de protocoles :

- `docs/protocoles_soins_suisse.md` : trame opérationnelle et protocoles initiaux (plaies, urgences, douleur, pyélonéphrite).
- `data/protocols/protocols_seed.fr-CH.json` : seed JSON structuré exploitable côté application.

Ces contenus sont des **bases de travail** et nécessitent une validation médicale locale/cantonale avant déploiement.

## Application exécutable Windows (protocoles de soins)

### Lancer localement (dev)

```bash
python app_protocoles.py
```

### Vérifier les données sans lancer l'UI

```bash
python app_protocoles.py --check
```

### Générer un `.exe` Windows

Depuis PowerShell:

```powershell
./scripts/build_protocols_exe.ps1
```

L'exécutable sera produit dans `dist/ProtocolesSoins/ProtocolesSoins.exe`.
