# Physical AI & Humanoid Robotics

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-16%2B-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-red.svg)](https://fastapi.tiangolo.com/)

*A cutting-edge platform for embodied intelligence and humanoid robotics research*

</div>

---

## 🤖 Overview

Welcome to the **Physical AI & Humanoid Robotics** project - an advanced platform designed to bridge the gap between artificial intelligence and physical embodiment. Our system combines state-of-the-art machine learning algorithms with sophisticated robotics control to create intelligent, adaptive humanoid systems capable of complex physical interactions and cognitive tasks.

### ✨ Key Features

- **Advanced RAG Engine**: Retrieval-Augmented Generation for contextual understanding
- **Gemini Integration**: Cutting-edge multimodal AI capabilities
- **Real-time Control**: Low-latency humanoid robotics control systems
- **Embodied Intelligence**: AI that learns and adapts through physical interaction
- **Modular Architecture**: Scalable and extensible system design
- **Modern UI/UX**: Intuitive interface with dark purple aesthetic

---

## 🏗️ Project Structure

```
humanoid_robotics_ai/
├── backend/
│   ├── src/
│   │   └── main.py (FastAPI, RAG Engine, Gemini Integration)
│   ├── .env (API Keys)
│   └── requirements.txt
├── docs/
│   ├── module1-embodied-intelligence/
│   ├── ... (Modules 2-9)
│   └── module10-capstone-ethics/
├── src/
│   ├── components/ (Chatbot.js, etc.)
│   ├── css/ (custom.css - Dark Purple Theme)
│   └── pages/ (index.js - Redesigned Homepage)
├── static/
│   └── img/ (robot-hero.png)
├── docusaurus.config.js
└── sidebars.js
```

---

## 🚀 Installation

Follow these steps to set up the project locally:

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm package manager

### Backend Setup

```bash
# Navigate to the backend directory
cd backend/

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Frontend Setup

```bash
# Navigate to the project root
cd ..

# Install Node.js dependencies
npm install

# Or if using yarn:
yarn install
```

---

## 🛠️ Running the Application

### Backend (API Server)

```bash
# Ensure you're in the backend directory with venv activated
cd backend/

# Start the FastAPI server with Uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be accessible at `http://localhost:8000`.

### Frontend (Docusaurus Site)

```bash
# From the project root directory
npm start
# Or if using yarn:
yarn start
```

The frontend will be accessible at `http://localhost:3000`.

---

## 🎨 Modern Dark Purple Aesthetic

Our interface features a sophisticated **Dark Purple** theme designed for optimal viewing during extended development and research sessions:

- **Primary Color**: Deep Purple (#4B0082)
- **Secondary Colors**: Royal Blue (#4169E1), Lavender (#E6E6FA)
- **Background**: Midnight (#121212) with Charcoal (#1E1E1E) accents
- **Text**: Crystal White (#F8F8F8) with Silver (#CCCCCC) secondary text

This color scheme reduces eye strain while maintaining excellent contrast and readability.

---

## 📚 Documentation Modules

Our comprehensive curriculum covers 10 essential modules:

1. **Module 1**: Embodied Intelligence Fundamentals
2. **Module 2**: Sensorimotor Learning and Control
3. **Module 3**: Human-Robot Interaction Design
4. **Module 4**: Advanced Locomotion Systems
5. **Module 5**: Cognitive Architecture for Robots
6. **Module 6**: Multi-Modal Perception Systems
7. **Module 7**: Adaptive Behavior Learning
8. **Module 8**: Social Robotics and Ethics
9. **Module 9**: Real-World Deployment Strategies
10. **Module 10**: Capstone Ethics and Future Implications

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

```env
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://user:password@localhost/dbname
JWT_SECRET_KEY=your_jwt_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Custom Styling

The dark purple theme is implemented in `src/css/custom.css`. You can customize colors, fonts, and spacing by modifying this file.

---

## 🐛 Troubleshooting

### Common Issues

#### CORS Errors
If you encounter CORS issues between frontend and backend:
- Ensure your backend is configured with the correct origins in `src/main.py`
- Check that `ALLOWED_ORIGINS` includes `http://localhost:3000`

#### MDX Rendering Issues
For problems with MDX content in Docusaurus:
- Verify all MDX files have proper syntax
- Check that all imported components are correctly referenced
- Run `npm run build` to test production build

#### Python Dependencies
If you encounter import errors:
- Ensure your virtual environment is activated
- Reinstall dependencies with `pip install -r requirements.txt`
- Check for conflicting package versions

#### Frontend Build Failures
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check for TypeScript compilation errors

---

## 🧪 Testing

Run backend tests:
```bash
cd backend/
python -m pytest tests/
```

Run frontend tests:
```bash
npm test
# Or if using yarn:
yarn test
```

---

## 🤝 Contributing

We welcome contributions to the Physical AI & Humanoid Robotics project! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Run linting and tests
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

### Maintainers

- **Project Lead**: [Your Name]
- **Development Team**: [Team Members]

---

<div align="center">

**Physical AI & Humanoid Robotics** © 2025
*Advancing the frontier of embodied artificial intelligence*

</div>