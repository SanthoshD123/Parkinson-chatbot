from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# Environment variables would be better for production
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Database of common Parkinson's drugs and their known side effects
# This could be moved to a separate JSON file or database in production
PARKINSONS_DRUGS = {
    "levodopa": {
        "common_side_effects": ["Nausea", "Dizziness", "Headache", "Dry mouth"],
        "severe_side_effects": ["Dyskinesia", "On-off phenomenon", "Hallucinations"],
        "resources": [
            {"name": "Mayo Clinic - Levodopa",
             "url": "https://www.mayoclinic.org/drugs-supplements/levodopa-oral-route/side-effects/drg-20064498"},
            {"name": "NIH Study on Levodopa", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5517545/"}
        ],
        "case_studies": [
            {"title": "Long-term Levodopa Treatment", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6693388/"}
        ]
    },
    "pramipexole": {
        "common_side_effects": ["Nausea", "Drowsiness", "Insomnia", "Constipation"],
        "severe_side_effects": ["Impulse control disorders", "Hallucinations", "Sudden sleep episodes"],
        "resources": [
            {"name": "Medline Plus - Pramipexole", "url": "https://medlineplus.gov/druginfo/meds/a697029.html"},
            {"name": "NIH Research on Pramipexole", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5040537/"}
        ],
        "case_studies": [
            {"title": "Pramipexole and Impulse Control Disorders",
             "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5874453/"}
        ]
    },
    "ropinirole": {
        "common_side_effects": ["Nausea", "Dizziness", "Fatigue", "Headache"],
        "severe_side_effects": ["Impulse control disorders", "Hypotension", "Hallucinations"],
        "resources": [
            {"name": "RxList - Ropinirole", "url": "https://www.rxlist.com/requip-side-effects-drug-center.htm"},
            {"name": "NIH Ropinirole Study", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3662253/"}
        ],
        "case_studies": [
            {"title": "Ropinirole Extended Release Study",
             "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4847268/"}
        ]
    },
    "amantadine": {
        "common_side_effects": ["Nausea", "Dizziness", "Insomnia", "Purple mottling of skin"],
        "severe_side_effects": ["Hallucinations", "Edema", "Heart rhythm problems"],
        "resources": [
            {"name": "Drugs.com - Amantadine", "url": "https://www.drugs.com/mtm/amantadine.html"},
            {"name": "NIH Amantadine Review", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5015353/"}
        ],
        "case_studies": [
            {"title": "Amantadine for Dyskinesia", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5447072/"}
        ]
    },
    "selegiline": {
        "common_side_effects": ["Nausea", "Dizziness", "Insomnia", "Dry mouth"],
        "severe_side_effects": ["Hypertensive crisis (with tyramine-rich foods)", "Hallucinations", "Confusion"],
        "resources": [
            {"name": "WebMD - Selegiline", "url": "https://www.webmd.com/drugs/2/drug-8885/selegiline-oral/details"},
            {"name": "NIH Selegiline Research", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5382063/"}
        ],
        "case_studies": [
            {"title": "Selegiline as Early Treatment", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6287681/"}
        ]
    },
    "entacapone": {
        "common_side_effects": ["Nausea", "Urine discoloration", "Diarrhea", "Abdominal pain"],
        "severe_side_effects": ["Severe diarrhea", "Hallucinations", "Dyskinesia"],
        "resources": [
            {"name": "MedlinePlus - Entacapone", "url": "https://medlineplus.gov/druginfo/meds/a699017.html"},
            {"name": "NIH Entacapone Study", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5367617/"}
        ],
        "case_studies": [
            {"title": "Entacapone with Levodopa Study", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4764999/"}
        ]
    }
}

# Add more specialized resources
GENERAL_RESOURCES = [
    {"name": "Parkinson's Foundation", "url": "https://www.parkinson.org/"},
    {"name": "Michael J. Fox Foundation", "url": "https://www.michaeljfox.org/"},
    {"name": "American Parkinson Disease Association", "url": "https://www.apdaparkinson.org/"},
    {"name": "NIH Parkinson's Disease Information",
     "url": "https://www.ninds.nih.gov/Disorders/All-Disorders/Parkinsons-Disease-Information-Page"},
    {"name": "World Parkinson Coalition", "url": "https://www.worldpdcoalition.org/"}
]


# Log conversations for improvement
def log_conversation(user_input, bot_response):
    log_dir = "conversation_logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"{log_dir}/conversation_{timestamp}.json"

    log_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_input": user_input,
        "bot_response": bot_response
    }

    with open(log_file, "w") as f:
        json.dump(log_data, f, indent=2)


def get_drug_info(drug_name):
    """Get information about a specific drug if it exists in our database"""
    # Convert to lowercase and remove extra spaces for comparison
    drug_name = drug_name.lower().strip()

    # Look for the drug in our database
    for drug, info in PARKINSONS_DRUGS.items():
        if drug_name == drug or drug_name in drug:
            return {"name": drug.capitalize(), **info}

    return None


def enhance_response_with_resources(response, user_message):
    """Add relevant resources and case studies based on mentioned drugs"""

    # Check if any known drugs are mentioned in the user message or response
    mentioned_drugs = []
    for drug in PARKINSONS_DRUGS.keys():
        if drug in user_message.lower() or drug in response.lower():
            drug_info = get_drug_info(drug)
            if drug_info and drug_info["name"].lower() not in [d["name"].lower() for d in mentioned_drugs]:
                mentioned_drugs.append({"name": drug_info["name"], "info": drug_info})

    # If drugs were mentioned, add their resources and case studies
    if mentioned_drugs:
        response += "\n\n<div class='resources-section'>"
        response += "\n<h3>📚 Relevant Resources:</h3>"
        response += "\n<ul>"

        for drug_mention in mentioned_drugs:
            drug_name = drug_mention["name"]
            drug_info = drug_mention["info"]

            # Add drug-specific resources
            for resource in drug_info.get("resources", []):
                response += f"\n<li><a href='{resource['url']}' target='_blank'>{resource['name']}</a></li>"

            # Add drug-specific case studies
            for case_study in drug_info.get("case_studies", []):
                response += f"\n<li><a href='{case_study['url']}' target='_blank'>Case Study: {case_study['title']}</a></li>"

        response += "\n</ul>"
        response += "\n</div>"

    # Always add general resources section
    response += "\n\n<div class='general-resources'>"
    response += "\n<h3>🌐 General Parkinson's Disease Resources:</h3>"
    response += "\n<ul>"
    for resource in GENERAL_RESOURCES:
        response += f"\n<li><a href='{resource['url']}' target='_blank'>{resource['name']}</a></li>"
    response += "\n</ul>"
    response += "\n</div>"

    return response


def query_groq_api(user_message):
    """Query the Groq API with enhanced system prompt"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    # Enhanced system prompt
    system_prompt = """You are an expert medical chatbot specializing in Parkinson's disease treatments and their adverse effects. 
    Provide clear, structured, and readable responses with these guidelines:

    1. Present information in an organized manner with headings and bullet points
    2. Emphasize both common and severe side effects of medications
    3. Discuss management strategies for adverse effects
    4. Always mention the importance of consulting healthcare providers
    5. Include information about drug interactions when relevant
    6. Explain mechanisms of action briefly to help understanding
    7. Use patient-friendly language while maintaining medical accuracy
    8. Structure your response with clear headings using <h3> tags
    9. Format lists using <ul> and <li> tags for better display
    10. Use <strong> tags to emphasize important warnings

    If specific medications are mentioned, provide detailed information about them.
    """

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.3,  # Lower temperature for more factual responses
        "max_tokens": 1500
    }

    try:
        response = requests.post(GROQ_API_URL, json=data, headers=headers)
        response_json = response.json()
        raw_text = response_json.get("choices", [{}])[0].get("message", {}).get("content", "No response.")

        # Enhanced text already has HTML formatting from the system prompt
        enhanced_text = enhance_response_with_resources(raw_text, user_message)

        return enhanced_text
    except Exception as e:
        print(f"Error querying Groq API: {e}")
        return f"<h3>Error</h3>I'm sorry, but I encountered an error while retrieving information. Please try again or rephrase your question."


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    bot_response = query_groq_api(user_input)

    # Log conversation for future improvements
    log_conversation(user_input, bot_response)

    return jsonify({"response": bot_response})


@app.route("/drug_info", methods=["GET"])
def drug_info():
    """API endpoint to get information about a specific drug"""
    drug_name = request.args.get("name", "").lower()

    if not drug_name:
        return jsonify({"error": "No drug name provided"}), 400

    drug_info = get_drug_info(drug_name)

    if not drug_info:
        return jsonify({"error": f"Information about {drug_name} not found"}), 404

    return jsonify({"drug": drug_info})


@app.route("/drug_list", methods=["GET"])
def drug_list():
    """API endpoint to get a list of all drugs in the database"""
    drugs = [{"name": drug.capitalize()} for drug in PARKINSONS_DRUGS.keys()]
    return jsonify({"drugs": drugs})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)