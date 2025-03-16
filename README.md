# Personalized Diabetes Nutrition Application

A sophisticated AI-powered application that creates personalized nutrition plans for individuals with diabetes, taking into account health metrics, socioeconomic factors, cultural preferences, and literacy levels.

## 🚀 Live Application

**The application is deployed and accessible at: [https://diabetes-nutrition.streamlit.app/](https://diabetes-nutrition.streamlit.app/)**

Try it out to generate your own personalized diabetes nutrition plan!

## 🌟 Project Overview

This application aims to improve healthcare accessibility for individuals with diabetes by providing tailored nutrition guidance that considers not just medical factors, but also socioeconomic realities, cultural contexts, and literacy levels. It was designed specifically to support underserved populations and make diabetes management more accessible across diverse communities.

## ✨ Key Features

- **Personalized Nutrition Plans**: Generate detailed nutrition recommendations based on individual health metrics, including diabetes type, blood glucose levels, and other health conditions
- **Socioeconomic Adaptation**: Accommodate different income levels, food accessibility, cooking facilities, and time constraints
- **Cultural Context Integration**: Adapt recommendations to various cultural food preferences and regional food availability
- **Literacy-Level Adjustment**: Provide content with appropriate complexity based on education and literacy levels
- **Visual Communication**: Create visual aids to enhance understanding, especially for users with limited literacy
- **Practical Recipe Suggestions**: Offer simple, affordable recipes suitable for various cooking environments

## 🔧 Technology Stack

- **Frontend**: Streamlit for the user interface
- **Backend**: Python with various data processing libraries
- **AI/ML**: OpenAI API (GPT-4) for personalized content generation
- **Data Visualization**: Matplotlib and other Python visualization libraries
- **Deployment**: Streamlit Cloud for hosting the application

## 📋 Prerequisites

- Python 3.9+
- OpenAI API key

## 🚀 Installation and Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/diabetes-nutrition-app.git
   cd diabetes-nutrition-app
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your OpenAI API key**:

   Create a `.streamlit` directory and add a `secrets.toml` file:

   ```bash
   mkdir -p .streamlit
   ```

   Add your API key to `.streamlit/secrets.toml`:

   ```toml
   OPENAI_API_KEY = "your_openai_api_key_here"
   ```

5. **Run the application locally**:
   ```bash
   streamlit run app.py
   ```

## 💻 Usage

1. **Input Health Information**: Enter personal health data including diabetes type, glucose levels, weight, height, and dietary restrictions
2. **Add Socioeconomic Context**: Provide information about location, income level, food accessibility, cooking facilities, etc.
3. **Generate Plan**: Create a personalized nutrition plan based on the provided information
4. **View and Download**: Review the generated plan and download it for future reference

## 📊 Application Structure

```
diabetes-nutrition-app/
├── app.py                       # Main Streamlit application
├── utils/
│   ├── data_processing.py       # Data preprocessing functions
│   ├── llm_integration.py       # LLM integration functions
│   └── visualization.py         # Visual component generation
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

## 🔍 Key Components

- **Data Collection Module**: Gathers health metrics and socioeconomic factors
- **Analysis Engine**: Processes input data to determine nutritional needs
- **Adaptation System**: Tailors content based on literacy and cultural context
- **Visual Component Generator**: Creates visual aids appropriate to user needs
- **Plan Generation**: Produces comprehensive, personalized nutrition guidance

## 👨‍⚕️ Healthcare Applications

This application can support:

- Primary care providers in creating personalized nutrition guidance
- Diabetes educators in developing accessible education materials
- Community health workers in rural and underserved areas
- International healthcare initiatives addressing diabetes management

## 🌍 Cultural Adaptation

The application includes specific adaptations for various cultural contexts, including:

- African cuisine and food traditions
- South Asian dietary patterns
- Latin American food practices
- Middle Eastern culinary traditions
- East Asian food systems

## 🧠 Development Roadmap

Future enhancements planned:

- [ ] User accounts and data persistence
- [ ] Mobile application development
- [ ] Offline mode for areas with limited connectivity
- [ ] Integration with blood glucose monitoring devices
- [ ] Expanded language support
- [ ] Community features for support and recipe sharing

## 🔒 Privacy Considerations

This application handles sensitive health information. In a production environment, ensure:

- Proper data encryption
- Secure authentication
- Compliance with healthcare data regulations
- Clear privacy policies and data usage terms

## 🤝 Contributing

Contributions to improve the application are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature-branch`)
6. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- World Health Organization for diabetes management guidelines
- OpenAI for providing the AI capabilities
- Streamlit for the application framework and hosting
- Contributors and testers from diverse backgrounds who helped refine the cultural adaptations

## 📞 Contact

For questions or support, please open an issue on this repository or contact [senthilcaesar@gmail.com].

---

_This application is intended to provide nutritional guidance only and is not a substitute for professional medical advice. Always consult healthcare providers for medical decisions._
