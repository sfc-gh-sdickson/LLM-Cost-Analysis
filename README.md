<img src="Snowflake_Logo.svg" width="200">

# Honor Health Intelligence Agent Solution

**Social Determinants of Health and Value-Based Care Intelligence Platform**

This solution provides a complete Snowflake Intelligence Agent implementation for Honor Health, enabling natural language queries over patient data, SDOH factors, and value-based care metrics with ML-powered insights.

---

##  What This Solution Provides

- **Natural Language Queries**: Ask questions about patients, SDOH, and care quality in plain English
- **ML-Powered Predictions**: 3 trained models for readmission risk, health outcomes, and social risk stratification
- **Unstructured Data Search**: Cortex Search over clinical notes, care plans, and policies
- **Semantic Layer**: Cortex Analyst with semantic views for accurate text-to-SQL conversion

---

##  Data Model

### Core Entities
1. **PATIENTS** - Patient demographics and enrollment (50,000)
2. **SOCIAL_DETERMINANTS** - SDOH assessments and risk factors (40,000)
3. **PROVIDERS** - Healthcare providers and care teams (500)
4. **ENCOUNTERS** - Patient visits and hospitalizations (80,000)
5. **QUALITY_METRICS** - HEDIS and quality measures (60,000)
6. **HEALTH_OUTCOMES** - Patient outcomes and improvements (50,000)
7. **CLINICAL_NOTES** - Unstructured clinical documentation (30,000)
8. **CARE_PLANS** - Treatment plans and SDOH interventions (25,000)
9. **HEALTH_POLICIES** - Clinical guidelines and protocols (100)

### ML Models
1. **READMISSION_RISK_PREDICTOR** - Predicts 30-day readmission risk (2 classes)
2. **HEALTH_OUTCOME_PREDICTOR** - Predicts health outcomes (3 classes)
3. **SOCIAL_RISK_STRATIFICATION** - Stratifies social risk (3 classes)

---

##  Setup Instructions

### Prerequisites
- Snowflake account with ACCOUNTADMIN access
- Warehouse (recommended: MEDIUM or larger for data generation)
- Snowflake Notebook environment (for ML models)

### Quick Start

```bash
# Step 1: Database and Schema Setup
snow sql -f sql/setup/honorhealth_01_database_and_schema.sql

# Step 2: Create Tables
snow sql -f sql/setup/honorhealth_02_create_tables.sql

# Step 3: Generate Synthetic Data (10-15 minutes)
snow sql -f sql/data/honorhealth_03_generate_synthetic_data.sql

# Step 4: Create Views
snow sql -f sql/views/honorhealth_04_create_views.sql

# Step 5: Create Semantic Views
snow sql -f sql/views/honorhealth_05_create_semantic_views.sql

# Step 6: Create Cortex Search Services
snow sql -f sql/search/honorhealth_06_create_cortex_search.sql

# Step 7: Train ML Models (upload notebook to Snowflake)
# Upload notebooks/honorhealth_ml_models.ipynb to Snowsight

# Step 8: Create ML Functions
snow sql -f sql/ml/honorhealth_07_ml_model_functions.sql

# Step 9: Create Intelligence Agent
snow sql -f sql/agent/honorhealth_08_intelligence_agent.sql
```

For detailed instructions, see [HONORHEALTH_SETUP_GUIDE.md](docs/HONORHEALTH_SETUP_GUIDE.md)

---

##  Sample Questions

### Simple Questions
1. How many patients do we have in our system?
2. What is the average SDOH risk score for our patients?
3. Show me the readmission rate for this month
4. Which insurance types have the most patients?
5. What percentage of patients have food insecurity?

### Complex Questions
6. How do social determinants impact hospital readmissions?
7. Compare healthcare costs between patients with and without social risk factors
8. Which providers have the best quality scores and lowest readmission rates?
9. Show me the relationship between care plan adherence and health outcomes
10. What is the trend in emergency department utilization by county?

### ML Model Questions
11. Predict readmission risk for patients currently hospitalized
12. Which patients are most likely to show health outcome improvement?
13. Identify patients with high social risk who need intervention
14. What is the predicted readmission rate for diabetic patients?
15. Show me patients with declining health outcomes despite active care plans

For complete question details, see [honorhealth_questions.md](docs/honorhealth_questions.md)

---

## Architecture Diagrams

### System Architecture
<img src="docs/architecture_diagram.svg" width="800">

*The Honor Health Intelligence Agent connects clinical users to structured data (via semantic views), ML predictions (via 3 models), and unstructured data (via Cortex Search), all powered by the Snowflake Data Platform.*

### Setup Flow
<img src="docs/setup_flow_diagram.svg" width="900">

*Complete setup process from database creation to production-ready agent in 9 steps, taking approximately 45-60 minutes.*

---

##  Important Notes

1. **Semantic View Syntax**: All semantic view DDL has been verified against official Snowflake documentation
2. **ML Models**: Require `snowflake-ml-python` package in notebook environment (NO version pinning)
3. **Cortex Search**: Requires change tracking enabled on source tables (automatically configured)
4. **Agent Tools**: All 3 ML models are registered as tools in the Intelligence Agent
5. **Data Volume**: Synthetic data generation creates ~335,600 rows across all tables

---

##  Security & Compliance

- All data is synthetic and for demonstration purposes
- Role-based access control (RBAC) configured
- Semantic models respect underlying table permissions
- Cortex Search uses owner's rights security model
- Patient privacy considerations built into agent instructions

---

##  Cost Considerations

- **Warehouse Compute**: Data generation ~10 credits (MEDIUM warehouse)
- **ML Training**: ~5-10 credits (depends on data volume)
- **Cortex Search**: Per-query cost + storage
- **Intelligence Agent**: Per-message cost

---

##  Troubleshooting

### Semantic View Errors
- Verify all column names match table definitions exactly
- Check that feature views exist before referencing in metrics
- Use lowercase table aliases consistently

### ML Model Errors
- Ensure models are registered with `target_platforms=['WAREHOUSE']` for SQL inference
- Verify feature view column names match model training columns exactly
- Do NOT pin package versions in environment.yml

### Cortex Search Errors
- Confirm change tracking is enabled on source tables
- Verify warehouse has sufficient capacity for indexing

---

##  Support

For questions or issues:
1. Check the HONORHEALTH_SETUP_GUIDE.md for detailed instructions
2. Review Snowflake documentation for syntax validation
3. Verify all prerequisites are met

---

**Created for**: Honor Health (Arizona Healthcare System)  
**Purpose**: Demonstrating Snowflake Intelligence Agent capabilities for SDOH and Value-Based Care  
**Version**: 1.0.0  
**Last Updated**: December 2025

