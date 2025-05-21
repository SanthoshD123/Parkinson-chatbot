# PD TreatmentAssist 🧠💊

![PD TreatmentAssist](https://img.shields.io/badge/PD%20TreatmentAssist-v1.0-4958b8)
![Flask](https://img.shields.io/badge/Flask-2.0.1-green)
![License](https://img.shields.io/badge/License-MIT-blue)
[![Groq LLM](https://img.shields.io/badge/Powered%20by-Groq%20LLM-purple)](https://groq.com)

A specialized AI-powered web application designed to provide comprehensive information about Parkinson's disease medications, their side effects, and management strategies.

![PD TreatmentAssist Screenshot](https://via.placeholder.com/800x450?text=PD+TreatmentAssist+Screenshot)

## 🌟 Features

- **Interactive AI Chat**: Get detailed, medically-informed responses about Parkinson's disease treatments
- **Medication Database**: Access information on common Parkinson's medications
- **Side Effect Highlighting**: Visual identification of common vs. severe side effects
- **Resource Integration**: Automatic linking to relevant medical resources and case studies
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **User-Friendly Interface**: Clean, intuitive design for easy navigation

## 🔧 Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI Integration**: Groq API with Llama 3 (70B model)
- **Styling**: CSS with Font Awesome icons

## 📋 Project Structure

```
pd-treatmentassist/
├── app.py                 # Main Flask application
├── static/               
│   └── script.js          # Frontend JavaScript
├── templates/            
│   └── index.html         # HTML template with embedded CSS
├── conversation_logs/     # Directory for storing conversation logs
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/pd-treatmentassist.git
   cd pd-treatmentassist
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser** and navigate to `http://127.0.0.1:5000`

## 🔒 Environment Variables

- `GROQ_API_KEY`: Your API key from Groq (required for AI functionality)

## 💻 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application page |
| `/chat` | POST | Send user messages to AI |
| `/drug_list` | GET | Get list of all medications in the database |
| `/drug_info` | GET | Get information about a specific medication |

## 📱 Usage Examples

### Getting Information About a Medication

Ask specific questions about Parkinson's medications:

```
Tell me about the side effects of Levodopa and how to manage them.
```

### Understanding Treatment Options

Inquire about different treatment approaches:

```
What are the main differences between dopamine agonists and levodopa?
```

### Managing Side Effects

Get advice on dealing with treatment challenges:

```
How can I reduce dyskinesia symptoms while on Parkinson's medication?
```

## 🌱 Future Enhancements

- **Personalized Treatment Insights**: Allow users to input their current medications for personalized information
- **Medication Interaction Checker**: Alert users to potential drug interactions
- **Symptom Tracker**: Enable users to track symptoms and their correlation with medications
- **Healthcare Provider Mode**: Specialized interface for medical professionals
- **Export Functionality**: Allow users to export conversation data for sharing with healthcare providers

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

PD TreatmentAssist is designed as an informational resource only and should not replace professional medical advice. Always consult with your healthcare provider before making any changes to your treatment plan.

## 👏 Acknowledgements

- [Groq](https://groq.com) for providing the AI infrastructure
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Font Awesome](https://fontawesome.com/) for the icons
- Medical resources and research papers referenced in the application
