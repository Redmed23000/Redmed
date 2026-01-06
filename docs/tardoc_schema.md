# Schéma TARDOC

## Tables principales
- `codes`: codes officiels et unités de temps.
- `exclusions`: codes incompatibles explicites.
- `incompatibilities`: incompatibilités bidirectionnelles.
- `conditions`: règles conditionnelles déclaratives.
- `limits`: limites d'utilisation (périodes, occurrences).
- `tardoc_updates`: journal des mises à jour.

## Notes
- Les champs `effective_date` / `expiry_date` gèrent la validité dans le temps.
- Les règles doivent être chargées via `scripts/update_rules.py`.
