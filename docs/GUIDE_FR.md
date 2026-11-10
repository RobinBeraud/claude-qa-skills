# Guide de démarrage (français)

**claude-qa-skills** est une bibliothèque de 119 compétences (« skills ») pour Claude Code dédiées à la qualité logicielle et au développement : stratégie de test, tests unitaires et de mutation, automatisation, test exploratoire, CI, mise en production, métriques DORA, Evidence-Based Management, QA à l'ère des agents IA, et logiciels de gestion (ERP, facturation électronique, SaaS).

Les skills sont rédigés en anglais, mais Claude vous **répond dans votre langue** : demandez en français, vous aurez une réponse en français.

## 1. Prérequis

- **Claude Code** installé et connecté (terminal, application de bureau ou extension VS Code / JetBrains).
- **git** sur votre poste.
- **Python 3.9 ou plus** seulement pour les scripts fournis (aucune bibliothèque à installer).

## 2. Installer en deux commandes

Dans une session Claude Code :

```text
/plugin marketplace add RobinBeraud/claude-qa-skills
/plugin install qa-test-strategy@claude-qa-skills
```

Tapez ensuite `/plugin` pour parcourir les 19 plugins et installer ceux qui vous servent.

> Pas de clé SSH GitHub sur votre poste ? Définissez la variable `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` avant d'ajouter le catalogue (PowerShell : `$env:CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`).

## 3. Quels plugins pour quel rôle ?

| Vous êtes | Installez | Essayez |
|---|---|---|
| QA / testeur | `qa-shift-left`, `qa-explore-and-report`, `qa-automation` | « Vérifie la testabilité de cette user story », « Écris des chartes de test exploratoire pour l'écran de paiement » |
| Développeur | `qa-unit-testing`, `qa-mutation-testing`, `qa-ai-era` | « Écris les tests unitaires de `facture.py` », « Relis cette PR écrite par l'IA par rapport au ticket » |
| Tech lead / responsable QA | `qa-test-strategy`, `qa-ci-insights`, `qa-release` | « Rédige notre stratégie de test sur une page », « Trouve les tests instables dans ces rapports JUnit » |
| Coach agile / manager / PO | `dora-metrics`, `evidence-based-management`, `qa-test-strategy` | « Calcule nos métriques DORA à partir de cet export », « Aide-nous à définir nos objectifs EBM » |
| Équipe ERP / finance / SaaS | `qa-business-apps` | « Vérifie cette facture Factur-X », « Génère les tests de droits depuis cette matrice de rôles » |

## 4. Utiliser un skill

- **Demandez simplement** : Claude choisit le bon skill d'après votre demande (« notre CI passe au vert en relançant, quels tests sont instables ? » déclenche `flaky-test-hunter`).
- **Ou appelez-le** : `/qa-explore-and-report:bug-report le bouton d'export plante avec des montants à 3 décimales`.
- Fournissez la matière : la story, le diff, l'export CSV, le rapport. Les skills demandent ce qui manque au lieu de l'inventer.

## 5. L'installer pour toute l'équipe

Dans le dépôt de votre projet, une seule fois, puis commitez le fichier `.claude/settings.json` créé :

```bash
claude plugin marketplace add RobinBeraud/claude-qa-skills --scope project
claude plugin install qa-ai-era@claude-qa-skills --scope project
```

Chaque collègue qui ouvre le projet (et accepte de faire confiance au dossier) obtient automatiquement le catalogue et les plugins.

## 6. Mettre à jour

`/plugin marketplace update claude-qa-skills`, ou activez la mise à jour automatique dans `/plugin` > **Marketplaces**.

## 7. Essayer les scripts tout de suite

```bash
git clone https://github.com/RobinBeraud/claude-qa-skills && cd claude-qa-skills
python plugins/qa-business-apps/skills/einvoice-consistency/scripts/cii_check.py examples/invoice-wrong-vat.xml
python plugins/evidence-based-management/skills/ebm-scorecard/scripts/ebm_scorecard.py examples/ebm.csv
```

Toutes les commandes d'exemple sont dans [GETTING_STARTED.md](GETTING_STARTED.md#5-try-the-scripts-on-the-examples-30-seconds).

## Bonnes pratiques

- Donnez le **contexte** : un skill de revue de PR a besoin du ticket, un skill de stratégie a besoin des risques.
- **Vérifiez** ce que produit Claude : les skills exigent des preuves (commandes exécutées, sorties), lisez-les.
- **Données** : n'envoyez jamais de données personnelles réelles ni de secrets ; les skills de données de test génèrent des données fictives valides.
- Une idée de skill ? Ouvrez une issue ou une pull request sur le dépôt.

## Nouveau en v1.2 : 7 plugins pour les développeurs

| Plugin | Pour | À demander par exemple |
|---|---|---|
| `dev-workflow` | la discipline avec un agent | « Explore ce module avant de modifier », « Cette branche est-elle trop grosse pour une PR ? », « Rédige la description de PR » |
| `dev-dotnet` | .NET et C# | « Fais l'inventaire de la solution », « Plan de migration vers .NET 10 », « Pourquoi cet endpoint EF Core est lent ? » |
| `dev-web` | Angular et front | « Passe ce module en standalone et signals », « Audit RGAA de cet écran » |
| `dev-data` | SQL Server et données | « Lis ce plan d'exécution », « Renomme cette colonne sans interruption », « Revue RGPD » |
| `dev-legacy` | le code ancien | « Où sont les points chauds depuis janvier ? », « Migration TFVC vers Git », « Quels correctifs manquent dans la 13.0 ? » |
| `dev-delivery` | Azure DevOps, GitLab | « Écris le pipeline YAML », « Génère les notes de version », « Trie les 90 PR ouvertes » |
| `dev-security` | sécurité | « Revue sécurité de ce diff », « Modèle de menaces STRIDE », « Scanne les secrets avant commit » |

Installation : `/plugin install dev-workflow@claude-qa-skills` (même marketplace, rien d'autre à ajouter).
