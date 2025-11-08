def get_user_profile_from():
    """
    Returns a structured dummy user profile for internal testing.

    Returns:
        dict: A dictionary containing user data with the following keys:
              - 'education'
              - 'certifications'
              - 'projects'
              - 'skills'
              - 'experience'
    """

    # Skills
    skills = [
        'Agentic AI', 'Retrieval Augmented Generation (RAG)', 'Large Language Models (LLMs)',
        'LangChain', 'Django', 'LSTM', 'Flask', 'Transformers', 'RNN', 'TensorFlow',
        'Supervised Learning', 'Unsupervised Learning', 'Pytorch', 'CNN', 'DBMS', 'DSA',
        'Statistics', 'SQL', 'AI', 'Linear Algebra', 'Calculus', 'PCA', 'Python',
        'Seaborn', 'Pandas', 'Numpy', 'Matplotlib', 'Scikit-learn', 'Data Analytics',
        'Data Science', 'Machine Learning', 'Jupyter Notebook', 'Git'
    ]

    # Certifications
    certifications = [
        {'name': 'Google Advanced Data Analytics', 'organization': 'Google'},
        {'name': 'IBM Data Science Professional Certificate', 'organization': 'IBM'},
        {'name': 'IBM RAG and Agentic AI: Build Next-Gen AI Systems', 'organization': 'IBM'},
        {'name': 'Deep Learning', 'organization': 'DeepLearningAI'},
        {'name': 'Machine Learning', 'organization': 'DeepLearningAI'},
        {'name': 'Mathematics for Machine Learning Specialization', 'organization': 'Imperial College London'},
        {'name': 'Mathematics for Machine Learning and Data Science', 'organization': 'DeepLearning.AI'},
        {'name': 'Python for Everybody Specialization', 'organization': 'University of Michigan'}
    ]

    # Projects
    projects = [
        {
            'name': 'BiasBusterAI: Text Bias Detection System',
            'start_date': 'October 2025',
            'end_date': 'October 2025',
            'description': (
                'Developed AI web app detecting biases (race, gender, profession, religion) '
                'with Bidirectional LSTM + Self Attention, achieving ~98% accuracy via TensorFlow. '
                'Created Flask interface with Plotly for real-time visualization of bias probabilities '
                'and attention weights. https://github.com/sheb1lmsp/BiasBusterAI'
            )
        },
        {
            'name': 'SmartAttend: An Automated Attendance Management System',
            'start_date': 'May 2025',
            'end_date': 'August 2025',
            'description': (
                'Developed a smart attendance management system using facial recognition to automate '
                'classroom attendance tracking. Leveraged PyTorch, MTCNN, and InceptionResNetV1 for '
                'face detection and recognition. Integrated with a Django web application featuring '
                'role-based dashboards. Streamlined attendance via group photo analysis. '
                'https://github.com/sheb1lmsp/smart_attend'
            )
        }
    ]

    # Education
    education = [
        {
            'degree': 'Bachelor of Computer Applications',
            'university': 'Bangalore University',
            'start_date': 'August 2022',
            'end_date': 'June 2025',
            'cgpa': '8.82'
        }
    ]

    # Experience (Empty Placeholder)
    experience = [
        {
            'title': '',
            'employment_type': '',
            'company': '',
            'start_date': '',
            'end_date': '',
            'location': '',
            'description': ''
        }
    ]

    # Return Unified Profile
    return {
        'education': education,
        'certifications': certifications,
        'projects': projects,
        'skills': skills,
        'experience': experience
    }
