import os
import pandas as pd
from fastapi import FastAPI, Query
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from typing import Optional

# Init FastAPI app
app = FastAPI()

# model
model_name = "google/flan-t5-large" 
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
nlp = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

# Load sales data from CSV
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Load sales data once at startup
sales_data = load_data("sales_data.csv")

# Helper function to generate insights using the open-source model
def generate_insight(prompt):
    response = nlp(prompt, max_length=100, num_return_sequences=1)
    return response[0]['generated_text']

# Endpoint to get individual sales representative performance
@app.get("/api/rep_performance")
async def rep_performance(rep_id: int):
    rep_data = sales_data[sales_data["employee_id"] == rep_id]

    if rep_data.empty:
        return {"error": "Sales representative not found"}

    # Calculate key performance metrics
    total_leads = rep_data["lead_taken"].sum()
    total_tours = rep_data["tours_booked"].sum()
    total_apps = rep_data["applications"].sum()
    total_revenue_confirmed = rep_data["revenue_confirmed"].sum()
    total_revenue_pending = rep_data["revenue_pending"].sum()
    
    prompt = f"Analyze the performance of sales representative with ID {rep_id}. They took {total_leads} leads, booked {total_tours} tours, and confirmed {total_revenue_confirmed} revenue. Provide detailed performance feedback and suggestions."

    insight = generate_insight(prompt)
    return {"rep_id": rep_id, "insight": insight}

# Endpoint to get overall team performance
@app.get("/api/team_performance")
async def team_performance():
    total_leads = sales_data["lead_taken"].sum()
    total_tours = sales_data["tours_booked"].sum()
    total_apps = sales_data["applications"].sum()
    total_revenue_confirmed = sales_data["revenue_confirmed"].sum()
    total_revenue_pending = sales_data["revenue_pending"].sum()
    
    prompt = f"Analyze the overall team performance. The team took {total_leads} leads, booked {total_tours} tours, and confirmed {total_revenue_confirmed} revenue. Provide a summary and feedback on the team's performance."

    insight = generate_insight(prompt)
    return {"team_performance": insight}

# Endpoint to get sales trends and forecasting
@app.get("/api/performance_trends")
async def performance_trends(time_period: Optional[str] = "monthly"):
    sales_data["created"] = pd.to_datetime(sales_data["created"])

    if time_period == "monthly":
        trends = sales_data.resample('M', on="created").sum()
    elif time_period == "quarterly":
        trends = sales_data.resample('Q', on="created").sum()
    else:
        return {"error": "Invalid time period. Choose 'monthly' or 'quarterly'."}

    trend_summary = trends[["lead_taken", "tours_booked", "applications", "revenue_confirmed"]].describe().to_dict()
    
    prompt = f"Analyze sales performance trends based on {time_period} data. The data shows these metrics: {trend_summary}. Forecast future performance and provide insights."

    insight = generate_insight(prompt)
    return {"trend_insights": insight}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
